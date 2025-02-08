import re           # For pattern matching
import os           # For file operations
import json         # For JSON output
import pandas as pd # For data manipulation
from collections import defaultdict

# Regular expressions for parsing instruction definitions
INSTRUCTION_PATTERN = r'(?P<instruction>\w+)\s+.*?(?P<bit_ranges>(\d+\.\.\d+|\d+)\s*=\s*(0x[0-9A-Fa-f]+|0b[01]+|\d+)(\s+(\d+\.\.\d+|\d+)\s*=\s*(0x[0-9A-Fa-f]+|0b[01]+|\d+))*)'
PSEUDO_OP_PATTERN = r'\$pseudo_op\s+(?P<extension>[\w.]+)::(?P<base_instruction>\w+)\s+(?P<instruction>\w+)\s+(?P<args>.*?)\s+(?P<bit_ranges>((\d+\.\.\d+|\d+)\s*=\s*(0x[0-9A-Fa-f]+|0b[01]+|\d+)\s*)+)'

def process_bit_ranges(bit_ranges_value: str) -> list:
    """Process bit range expressions into a structured format."""
    return bit_ranges_value.strip().split()

def extract_opcodes(file_path: str) -> list:
    """Extract instruction definitions from a RISC-V opcode file."""
    opcode_data = []
    extension = os.path.basename(file_path)  # Get filename as extension
    
    # Compile regex patterns
    instruction_regex = re.compile(INSTRUCTION_PATTERN)
    pseudo_op_regex = re.compile(PSEUDO_OP_PATTERN)
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
                
            # Handle pseudo-ops
            if line.startswith('$pseudo_op'):
                match = pseudo_op_regex.match(line)
                if match:
                    instruction = f"pseudo_op-{match.group('instruction')}"
                    bit_ranges = process_bit_ranges(match.group('bit_ranges'))
                    opcode_data.append((instruction, bit_ranges, extension))
                continue
            
            # Handle regular instructions
            match = instruction_regex.match(line)
            if match:
                instruction = match.group('instruction')
                bit_ranges = process_bit_ranges(match.group('bit_ranges'))
                opcode_data.append((instruction, bit_ranges, extension))
                
    return opcode_data

def save_to_json(opcode_data: list, json_file_path: str) -> None:
    """Save extracted opcode data to a JSON file with unified instruction format."""
    # Group data by instruction
    unified_data = defaultdict(lambda: {"bit_ranges": [], "extension": []})
    
    for instruction, bit_ranges, extension in opcode_data:
        # Add unique bit ranges
        for bit_range in bit_ranges:
            if bit_range not in unified_data[instruction]["bit_ranges"]:
                unified_data[instruction]["bit_ranges"].append(bit_range)
        
        # Add extension if not already present
        if extension not in unified_data[instruction]["extension"]:
            unified_data[instruction]["extension"].append(extension)
    
    # Convert to list format for JSON
    formatted_data = [
        {
            "instruction": instruction,
            "bit_ranges": data["bit_ranges"],
            "extension": data["extension"]
        }
        for instruction, data in unified_data.items()
    ]
    
    # Save to JSON with pretty printing
    with open(json_file_path, 'w') as json_file:
        json.dump(formatted_data, json_file, indent=2)

def main():
    # Process all opcode files
    folder_path = './data/opcodes/'
    all_opcode_data = []

    # Process each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print(f"Processing {filename}...")
            opcode_data = extract_opcodes(file_path)
            all_opcode_data.extend(opcode_data)

    print(f"\nTotal instructions found: {len(all_opcode_data)}")

    # Create DataFrame for analysis
    df = pd.DataFrame(all_opcode_data, columns=['instruction', 'bit_ranges', 'extension'])

    # Save to JSON
    json_file_path = './data/output_opcodes.json'
    save_to_json(all_opcode_data, json_file_path)
    print(f"\nOpcode data saved to {json_file_path}")

    # Display extension distribution
    print("\nExtension distribution:")
    print(df['extension'].value_counts())

    print(f"\nUnique instructions: {len(df['instruction'].unique())}")

    # Convert bit_ranges to string for comparison
    df['bit_ranges_str'] = df['bit_ranges'].apply(lambda x: ','.join(sorted(x)))

    # Find duplicates using string representation
    duplicates = df[df.duplicated(['instruction', 'bit_ranges_str'], keep=False)].sort_values('instruction')
    if not duplicates.empty:
        print("\nWarning: Found duplicate instruction definitions:")
        print(duplicates[['instruction', 'bit_ranges', 'extension']])

    # Sample of processed data
    print("\nSample of processed instructions:")
    print(df[['instruction', 'bit_ranges', 'extension']].head())

if __name__ == "__main__":
    main() 