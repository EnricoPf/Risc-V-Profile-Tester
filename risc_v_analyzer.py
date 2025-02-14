#!/usr/bin/env python3

import json          # For reading opcode definitions
import pandas as pd  # For data manipulation
import numpy as np   # For array operations
import re           # For pattern matching
import os           # For file operations
from typing import List, Dict, Any, Optional
import sys

class RiscVInstructionAnalyzer:
    """
    Analyzes RISC-V instructions from hex files and determines compatible profiles.
    
    This class provides functionality for:
    - Converting hex instructions to binary
    - Decoding instructions and extracting opcodes
    - Matching bit patterns to identify instructions
    - Finding compatible RISC-V profiles
    """
    
    def __init__(self, opcode_json_path: str = './data/output_opcodes.json', 
                 profile_csv_path: str = './data/csv/profile_mapping.csv'):
        """
        Initialize the analyzer with opcode and profile data.
        
        Args:
            opcode_json_path: Path to the JSON file containing opcode definitions
            profile_csv_path: Path to the CSV file containing profile mappings
        """
        # Load and preprocess opcode data
        self.df = pd.read_json(opcode_json_path)
        self.df['bit_ranges'] = self.df['bit_ranges'].apply(lambda x: np.array(x).ravel())
        self.df_sorted = self.df.sort_values(by='bit_ranges', key=lambda x: x.apply(len), ascending=False)
        self.df_sorted['bit_ranges'] = self.df_sorted['bit_ranges'].apply(lambda x: [self.parse_range(y) for y in x])
        
        # Load and preprocess profile data
        self.profiles_df = pd.read_csv(profile_csv_path, index_col='extension')
        self.profiles_df.loc['TOTAL'] = self.profiles_df.sum()
        self._preprocess_profiles()

    def _preprocess_profiles(self):
        """Preprocess profile data by combining RV64I/RV32I and RV64E/RV32E."""
        # Combine RV64I and RV32I into I using logical OR
        self.profiles_df.loc['I'] = self.profiles_df.loc[['rv64_i', 'rv34_i']].any()
        # Combine RV64E and RV32E into E using logical OR
        self.profiles_df.loc['E'] = self.profiles_df.loc[['rv64_e', 'rv34_e']].any()
        # Drop the original rows
        self.profiles_df = self.profiles_df.drop(['rv64_i', 'rv34_i', 'rv64_e', 'rv34_e'])

    @staticmethod
    def hex_to_bin(hex_str: str) -> str:
        """
        Convert hexadecimal string to binary string with proper padding.
        
        Args:
            hex_str: Hexadecimal string to convert
            
        Returns:
            Binary representation padded to 32 bits
        """
        # Remove whitespace and '0x' prefix
        hex_str = hex_str.strip().replace('0x', '')
        if not hex_str:
            return '0' * 32
        
        # Convert to binary and remove '0b' prefix
        binary = bin(int(hex_str, 16))[2:]
        
        # Pad to 32 bits for RISC-V instructions
        padding = (32 - len(binary)) if len(binary) < 32 else 0
        return '0' * padding + binary

    @staticmethod
    def parse_range(s: str) -> List[Any]:
        """
        Parse a range string in either 'X..Y=Z' or 'X=Z' format.
        
        Args:
            s: Range string to parse
            
        Returns:
            For 'X..Y=Z' format: [X, Y, Z] where:
                - X: start position (int)
                - Y: end position (int)
                - Z: binary value (str)
            For 'X=Z' format: [X, Z] where:
                - X: bit position (int)
                - Z: binary value (str)
        """
        # Handle range format 'X..Y=Z'
        if '..' in s:
            match = re.match(r'(\d+)\.\.(\d+)=(-?0x[\da-fA-F]+|-?\d+)', s)
            if match:
                start_pos = int(match.group(1))
                end_pos = int(match.group(2))
                value = match.group(3)
                # Convert value to binary
                binary_value = RiscVInstructionAnalyzer.hex_to_bin(value) if (value.startswith('0x') or value.startswith('-0x')) \
                              else bin(int(value))[2:]
                return [start_pos, end_pos, binary_value]
        
        # Handle single bit format 'X=Z'
        else:
            match = re.match(r'(\d+)=(-?0x[\da-fA-F]+|-?\d+)', s)
            if match:
                bit_pos = int(match.group(1))
                value = match.group(2)
                # Convert value to binary
                binary_value = RiscVInstructionAnalyzer.hex_to_bin(value) if (value.startswith('0x') or value.startswith('-0x')) \
                              else bin(int(value))[2:]
                return [bit_pos, binary_value]
        return None

    def get_instructions_from_hex(self, hex_content: List[str]) -> List[pd.Series]:
        """
        Extract RISC-V instructions from hex content.
        
        Args:
            hex_content: List of hex strings representing instructions
            
        Returns:
            List of pandas Series containing instruction information
        """
        instructions = []
        for line in hex_content:
            line = line.strip()
            line = self.hex_to_bin(line)[::-1]
            for index, row in self.df_sorted.iterrows():
                count = len(row['bit_ranges'])
                for rg in row['bit_ranges']:
                    if len(rg) == 3:
                        end = rg[0]
                        start = rg[1]
                        value = rg[2]
                        inter = line[start:end+1]
                        if (start > len(line)) or (end > len(line)):
                            continue
                        if int(inter[::-1], 2) != int(value, 2):
                            continue
                        count = count - 1
                    else:
                        position = rg[0]
                        value = rg[1]
                        if (position >= len(line)):
                            continue
                        if line[position] != value:
                            continue
                        count = count - 1
                    if count == 0:
                        instructions.append(row)
                        break
                if count == 0:
                    break
        return instructions

    def get_compatible_profiles(self, extensions: List[str]) -> List[str]:
        """
        Find RISC-V profiles that support all given extensions.
        
        Args:
            extensions: List of required RISC-V extensions
            
        Returns:
            List of profile names that support all required extensions
        """
        # Check which profiles support all required extensions
        profiles_with_all_extensions = self.profiles_df.loc[extensions].all(axis=0)
        
        # Return profiles that support all extensions
        return profiles_with_all_extensions[profiles_with_all_extensions == True].index.to_list()

    def analyze_hex_file(self, hex_file_path: str) -> Dict[str, Any]:
        """
        Analyze a hex file and determine compatible RISC-V profiles.
        
        Args:
            hex_file_path: Path to the hex file to analyze
            
        Returns:
            Dictionary containing analysis results:
            - instructions: List of found instructions
            - required_extensions: List of required extensions
            - compatible_profiles: List of compatible profiles
            - smallest_profile: Name of the smallest compatible profile
        """
        # Read hex file
        with open(hex_file_path, 'r') as file:
            hex_content = file.readlines()

        # Find instructions
        instructions = self.get_instructions_from_hex(hex_content)
        
        # Extract required extensions
        extensions = [instr['extension'][0].split("_", 1)[1].upper() for instr in instructions]
        
        # Find compatible profiles
        compatible_profiles = self.get_compatible_profiles(extensions)
        matches = self.profiles_df[compatible_profiles].loc['TOTAL'].sort_values()
        
        return {
            'instructions': instructions,
            'required_extensions': extensions,
            'compatible_profiles': matches.to_dict(),
            'smallest_profile': matches.index[0] if not matches.empty else None
        }

def main():
    """Example usage of the RISC-V Instruction Analyzer."""
    # Initialize analyzer
    analyzer = RiscVInstructionAnalyzer()
    
    # Get test file from command line args or use default
    test_file = sys.argv[1] if len(sys.argv) > 1 else './data/tests/memory/003-and.hex'
    
    # Analyze the hex file
    results = analyzer.analyze_hex_file(test_file)
    
    # Print results
    print("Found instructions:")
    print(results['instructions'])
    print("\nRequired extensions:")
    print(results['required_extensions'])
    print("\nCompatible profiles sorted by size (smallest first):")
    for profile, size in results['compatible_profiles'].items():
        print(f"{profile}: {size}")
    print(f"Smallest compatible profile: {results['smallest_profile']}")

if __name__ == "__main__":
    main()