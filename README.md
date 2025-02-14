# RISC-V Profiles Analyzer

A Python-based tool for analyzing RISC-V instructions and determining which profiles are apt to run a given set of instructions. This tool helps identify the most suitable RISC-V profile for a given set of instructions by analyzing hex files and matching them against known instruction patterns.

## Features

- Convert hex instructions to binary format
- Decode RISC-V instructions from hex files
- Extract and analyze instruction patterns
- Match instructions against RISC-V extensions
- Determine compatible RISC-V profiles
- Find the smallest compatible profile for a given instruction set

## Project Structure

```
Risc-V-Profiles/
├── data/
│   ├── csv/
│   │   ├── profiles.csv          # Profile definitions
│   │   └── profile_mapping.csv   # Extension-to-profile mappings
│   ├── opcodes/                  # RISC-V opcode definitions
│   ├── output_opcodes.json       # Processed opcode data
│   └── tests/
│       ├── memory/              # Test hex files
│       ├── program/            # Test assembly files
│       └── reference/          # Reference outputs
├── risc_v_analyzer.py           # Main analyzer script
├── opcode_dict.py              # Opcode dictionary generator
└── README.md                   # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Risc-V-Profiles.git
cd Risc-V-Profiles
```

2. Install required dependencies:
```bash
pip install pandas numpy
```

## Usage

### Basic Usage

```python
from risc_v_analyzer import RiscVInstructionAnalyzer

# Initialize the analyzer
analyzer = RiscVInstructionAnalyzer()

# Analyze a hex file
results = analyzer.analyze_hex_file('path/to/your/hex/file')

# Access the results
print(f"Found instructions: {results['instructions']}")
print(f"Required extensions: {results['required_extensions']}")
print(f"Smallest compatible profile: {results['smallest_profile']}")
```

### Command Line Usage

You can also run the analyzer directly from the command line:

```bash
python risc_v_analyzer.py <path_to_hex_file>
```

This will analyze a test file and display the results.

#### Methods

- `__init__(opcode_json_path='./data/output_opcodes.json', profile_csv_path='./data/csv/profile_mapping.csv')`
  - Initialize the analyzer with custom paths for opcode dictionary and profile data

- `analyze_hex_file(hex_file_path: str) -> Dict[str, Any]`
  - Analyze a hex file and return detailed results
  - Returns a dictionary containing:
    - `instructions`: List of found instructions
    - `required_extensions`: List of required extensions
    - `compatible_profiles`: Dictionary of compatible profiles and their sizes
    - `smallest_profile`: Name of the smallest compatible profile

- `get_instructions_from_hex(hex_content: List[str]) -> List[pd.Series]`
  - Extract RISC-V instructions from hex content

- `get_compatible_profiles(extensions: List[str]) -> List[str]`
  - Find RISC-V profiles that support all given extensions

## Data Files

### profiles.csv
Contains the base profile definitions for RISC-V instruction sets.

### profile_mapping.csv
Maps extensions to specific profiles and their requirements.

### output_opcodes.json
Contains processed opcode data used for instruction matching.
 
