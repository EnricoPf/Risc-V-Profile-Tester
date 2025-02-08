#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_profile_data(file_path: str) -> pd.DataFrame:
    """
    Load and validate the profile data from CSV file.
    
    Args:
        file_path: Path to the profiles CSV file
        
    Returns:
        DataFrame containing the profile data
    """
    try:
        # Read CSV with first column as index
        df = pd.read_csv(file_path, index_col=0)
        # Name the index as 'extension'
        df.index.name = 'extension'
        logger.info(f"Successfully loaded profile data from {file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"Profile data file not found at {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading profile data: {str(e)}")
        raise

def process_profile_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process the profile data to create value counts and boolean maps.
    
    Args:
        df: Input DataFrame with profile data
        
    Returns:
        Tuple of (value_counts DataFrame, boolean_map DataFrame)
    """
    try:
        # Create value counts
        value_counts = (df
            .replace('?', pd.NA)
            .replace('n', pd.NA)
            .replace('i', 'o')
            .replace('p', 'o')
            .apply(pd.Series.value_counts)
            .fillna(0))
            
        # Create boolean map
        boolean_map = df.applymap(lambda x: False if x == 'n' else True)
        
        logger.info("Successfully processed profile data")
        return value_counts, boolean_map
        
    except Exception as e:
        logger.error(f"Error processing profile data: {str(e)}")
        raise

def plot_extension_distribution(value_counts: pd.DataFrame, output_dir: str = None):
    """
    Create and save visualization of extension distribution.
    
    Args:
        value_counts: DataFrame containing extension value counts
        output_dir: Optional directory to save plot
    """
    try:
        plt.figure(figsize=(12, 8))
        value_counts_t = value_counts.T
        ax = value_counts_t.plot(kind='bar')
        plt.ylabel('Number of Extensions')
        plt.title('Distribution of Mandatory and Optional Extensions per Profile')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, 'extension_distribution.png'))
            logger.info(f"Saved plot to {output_dir}/extension_distribution.png")
        else:
            plt.show()
            
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        raise

def analyze_profiles(value_counts: pd.DataFrame, boolean_map: pd.DataFrame) -> Dict:
    """
    Analyze profile data and generate statistics.
    
    Args:
        value_counts: DataFrame with extension value counts
        boolean_map: DataFrame with boolean extension map
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        analysis = {
            'total_extensions': len(boolean_map.index),
            'total_profiles': len(boolean_map.columns),
            'mandatory_by_profile': value_counts.loc['m'].to_dict() if 'm' in value_counts.index else {},
            'optional_by_profile': value_counts.loc['o'].to_dict() if 'o' in value_counts.index else {},
            'extension_support': boolean_map.sum().to_dict()
        }
        
        logger.info("Successfully analyzed profile data")
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing profiles: {str(e)}")
        raise

def main():
    """Main function to run the profile map creation and analysis."""
    try:
        # Load data
        profile_data = load_profile_data("./data/csv/profiles.csv")
        
        # Process data
        value_counts, boolean_map = process_profile_data(profile_data)
        
        # Create visualization
        plot_extension_distribution(value_counts, output_dir="./output")
        
        # Analyze data
        analysis = analyze_profiles(value_counts, boolean_map)
        
        # Print analysis results
        print("\nProfile Analysis Results:")
        print(f"Total Extensions: {analysis['total_extensions']}")
        print(f"Total Profiles: {analysis['total_profiles']}")
        print("\nMandatory Extensions by Profile:")
        for profile, count in analysis['mandatory_by_profile'].items():
            print(f"  {profile}: {int(count)}")
        print("\nOptional Extensions by Profile:")
        for profile, count in analysis['optional_by_profile'].items():
            print(f"  {profile}: {int(count)}")
            
        # Save boolean map to CSV
        boolean_map.to_csv("./output/profile_map.csv")
        logger.info("Saved profile map to ./output/profile_map.csv")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 