"""
Comprehensive Data Validation Toolkit for June 2025
Ensures data accuracy and timeliness through multi-layered validation
"""

import requests
import pandas as pd
from datetime import datetime
import json
import logging
from typing import Dict, Any, Tuple, Optional
from pydantic import BaseModel, validator, ValidationError
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataValidator:
    """
    Main validation class that orchestrates all validation checks
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize validator with configuration
        
        Args:
            config: Dictionary containing validation parameters
                   {
                       'source_url': str,
                       'file_path': str,
                       'date_column': str,
                       'schema_model': BaseModel
                   }
        """
        self.config = config
        self.results = {}
        
    def run_validation_pipeline(self) -> Dict[str, Any]:
        """
        Execute complete validation workflow
        
        Returns:
            Dictionary containing all validation results
        """
        logger.info("Starting validation pipeline...")
        
        self.results = {
            'header_check': self.check_source_freshness(),
            'content_check': self.validate_data_content(),
            'schema_check': self.validate_data_schema()
        }
        
        # Overall validation status
        all_valid = all(result.get('valid', False) for result in self.results.values())
        self.results['overall_valid'] = all_valid
        
        logger.info(f"Validation pipeline completed. Overall valid: {all_valid}")
        return self.results
    
    def check_source_freshness(self) -> Dict[str, Any]:
        """
        Verify data source freshness via HTTP headers
        
        Returns:
            Dictionary with validation results
        """
        source_url = self.config.get('source_url')
        if not source_url:
            return {'valid': False, 'message': 'No source URL provided'}
            
        try:
            last_modified = self._get_last_modified(source_url)
            if not last_modified:
                return {
                    'valid': False, 
                    'message': 'Could not retrieve Last-Modified header',
                    'source_url': source_url
                }
            
            is_current = self._is_date_in_june_2025(last_modified)
            return {
                'valid': is_current,
                'message': 'Source is current' if is_current else 'Source is outdated',
                'timestamp': last_modified,
                'source_url': source_url
            }
            
        except Exception as e:
            logger.error(f"Error checking source freshness: {str(e)}")
            return {
                'valid': False,
                'message': f'Error checking source: {str(e)}',
                'source_url': source_url
            }
    
    def validate_data_content(self) -> Dict[str, Any]:
        """
        Validate dataset content using Pandas
        
        Returns:
            Dictionary with validation results
        """
        file_path = self.config.get('file_path')
        date_column = self.config.get('date_column', 'date')
        
        if not file_path:
            return {'valid': False, 'message': 'No file path provided'}
            
        try:
            # Check file exists
            if not Path(file_path).exists():
                return {'valid': False, 'message': f'File not found: {file_path}'}
            
            # Load data
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} rows from {file_path}")
            
            # Check for missing values
            missing_values = df.isnull().sum().sum()
            if missing_values > 0:
                missing_details = df.isnull().sum().to_dict()
                return {
                    'valid': False,
                    'message': f'Found {missing_values} missing values',
                    'missing_details': missing_details
                }
            
            # Validate date column
            if date_column not in df.columns:
                return {
                    'valid': False,
                    'message': f'Date column "{date_column}" not found',
                    'available_columns': list(df.columns)
                }
            
            # Convert date column
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            invalid_dates = df[date_column].isnull().sum()
            if invalid_dates > 0:
                return {
                    'valid': False,
                    'message': f'Found {invalid_dates} invalid date formats',
                    'invalid_rows': df[df[date_column].isnull()].index.tolist()
                }
            
            # Check for June 2025 data
            june_2025_data = df[
                (df[date_column].dt.year == 2025) & 
                (df[date_column].dt.month == 6)
            ]
            
            if june_2025_data.empty:
                return {
                    'valid': False,
                    'message': 'No data found for June 2025',
                    'date_range': {
                        'min': df[date_column].min().strftime('%Y-%m-%d'),
                        'max': df[date_column].max().strftime('%Y-%m-%d')
                    }
                }
            
            return {
                'valid': True,
                'message': 'Content validation passed',
                'rows_count': len(df),
                'june_2025_rows': len(june_2025_data),
                'date_range': {
                    'min': df[date_column].min().strftime('%Y-%m-%d'),
                    'max': df[date_column].max().strftime('%Y-%m-%d')
                }
            }
            
        except Exception as e:
            logger.error(f"Error validating data content: {str(e)}")
            return {
                'valid': False,
                'message': f'Validation error: {str(e)}'
            }
    
    def validate_data_schema(self) -> Dict[str, Any]:
        """
        Validate data against Pydantic schema
        
        Returns:
            Dictionary with validation results
        """
        schema_model = self.config.get('schema_model')
        file_path = self.config.get('file_path')
        
        if not schema_model:
            return {'valid': False, 'message': 'No schema model provided'}
            
