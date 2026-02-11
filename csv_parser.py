"""CSV file parser and validator for company data."""

import pandas as pd
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class CSVParserError(Exception):
    """Custom exception for CSV parsing errors."""
    pass


def validate_csv_structure(df: pd.DataFrame) -> None:
    """
    Validate that the CSV has the required columns.
    
    Args:
        df: DataFrame to validate
        
    Raises:
        CSVParserError: If the CSV structure is invalid
    """
    required_columns = ['company', 'sector', 'target_role']
    
    if df.shape[1] < 3:
        raise CSVParserError(
            f"CSV must have at least 3 columns. Found {df.shape[1]} columns."
        )
    
    # Rename columns to standard names (first 3 columns)
    df.columns = ['company', 'sector', 'target_role'] + list(df.columns[3:])
    
    # Check for missing values in required columns
    for col in required_columns:
        if df[col].isnull().any():
            raise CSVParserError(
                f"Column '{col}' contains empty values. All fields are required."
            )


def parse_csv_file(file_path: str) -> List[Dict[str, str]]:
    """
    Parse CSV file and return list of company/role data.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        List of dictionaries containing company, sector, and target_role
        
    Raises:
        CSVParserError: If the file cannot be parsed or is invalid
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        if df.empty:
            raise CSVParserError("CSV file is empty")
        
        # Validate structure
        validate_csv_structure(df)
        
        # Convert to list of dictionaries
        data = []
        for _, row in df.iterrows():
            data.append({
                'company': str(row['company']).strip(),
                'sector': str(row['sector']).strip(),
                'target_role': str(row['target_role']).strip()
            })
        
        logger.info(f"Successfully parsed {len(data)} entries from CSV")
        return data
        
    except FileNotFoundError:
        raise CSVParserError(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise CSVParserError("CSV file is empty")
    except Exception as e:
        raise CSVParserError(f"Error parsing CSV: {str(e)}")


def create_example_csv(file_path: str = "example_companies.csv") -> None:
    """
    Create an example CSV file with sample data.
    
    Args:
        file_path: Path where the example CSV should be created
    """
    sample_data = {
        'company': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple'],
        'sector': ['Technology', 'Technology', 'E-commerce', 'Social Media', 'Technology'],
        'target_role': ['Software Engineer', 'Senior Developer', 'DevOps Engineer', 
                       'Frontend Developer', 'iOS Developer']
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv(file_path, index=False)
    logger.info(f"Example CSV created at: {file_path}")
