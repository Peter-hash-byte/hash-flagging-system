"""File loaders for various data formats"""

import csv
import json
import xml.etree.ElementTree as ET
from typing import List, Dict
import logging
import os

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import xmltodict
    XMLTODICT_AVAILABLE = True
except ImportError:
    XMLTODICT_AVAILABLE = False

logger = logging.getLogger(__name__)


class FileLoader:
    """Load employee records from various file formats"""
    
    SUPPORTED_FORMATS = ['csv', 'json', 'xml', 'xlsx', 'xls', 'tsv']
    
    @staticmethod
    def detect_format(filepath: str) -> str:
        """Auto-detect file format from extension"""
        ext = os.path.splitext(filepath)[1].lower().lstrip('.')
        
        if ext in FileLoader.SUPPORTED_FORMATS:
            return ext
        
        raise ValueError(f"Unsupported file format: {ext}. Supported: {FileLoader.SUPPORTED_FORMATS}")
    
    @staticmethod
    def load(filepath: str, format_type: str = None, 
             id_column: str = 'id', email_column: str = 'email',
             hash_column: str = 'password_hash') -> List[Dict]:
        """
        Load employee records from file
        
        Args:
            filepath: Path to the file
            format_type: File format (auto-detected if None)
            id_column: Name of employee ID column
            email_column: Name of email column
            hash_column: Name of password hash column
            
        Returns:
            List of employee record dictionaries
        """
        if format_type is None:
            format_type = FileLoader.detect_format(filepath)
        
        format_type = format_type.lower()
        
        if format_type == 'csv':
            return FileLoader._load_csv(filepath, id_column, email_column, hash_column)
        elif format_type == 'tsv':
            return FileLoader._load_tsv(filepath, id_column, email_column, hash_column)
        elif format_type == 'json':
            return FileLoader._load_json(filepath, id_column, email_column, hash_column)
        elif format_type == 'xml':
            return FileLoader._load_xml(filepath, id_column, email_column, hash_column)
        elif format_type in ['xlsx', 'xls']:
            return FileLoader._load_excel(filepath, id_column, email_column, hash_column)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    @staticmethod
    def _load_csv(filepath: str, id_col: str, email_col: str, hash_col: str) -> List[Dict]:
        """Load from CSV file"""
        records = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append({
                        'id': row.get(id_col, ''),
                        'email': row.get(email_col, ''),
                        'password_hash': row.get(hash_col, '')
                    })
            logger.info(f"Loaded {len(records)} records from CSV")
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise
        
        return records
    
    @staticmethod
    def _load_tsv(filepath: str, id_col: str, email_col: str, hash_col: str) -> List[Dict]:
        """Load from TSV (Tab-Separated Values) file"""
        records = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                for row in reader:
                    records.append({
                        'id': row.get(id_col, ''),
                        'email': row.get(email_col, ''),
                        'password_hash': row.get(hash_col, '')
                    })
            logger.info(f"Loaded {len(records)} records from TSV")
        except Exception as e:
            logger.error(f"Error loading TSV: {e}")
            raise
        
        return records
    
    @staticmethod
    def _load_json(filepath: str, id_col: str, email_col: str, hash_col: str) -> List[Dict]:
        """Load from JSON file"""
        records = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Handle both list of objects and single object
                if isinstance(data, dict):
                    # Check if it has an 'employees' key or similar
                    for key, value in data.items():
                        if isinstance(value, list):
                            data = value
                            break
                
                if isinstance(data, list):
                    for item in data:
                        records.append({
                            'id': item.get(id_col, ''),
                            'email': item.get(email_col, ''),
                            'password_hash': item.get(hash_col, '')
                        })
            
            logger.info(f"Loaded {len(records)} records from JSON")
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            raise
        
        return records
    
    @staticmethod
    def _load_xml(filepath: str, id_col: str, email_col: str, hash_col: str) -> List[Dict]:
        """Load from XML file"""
        records = []
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            # Find employee elements (handles various naming conventions)
            for employee in root.findall('.//employee') or root.findall('.//record'):
                emp_dict = {
                    'id': '',
                    'email': '',
                    'password_hash': ''
                }
                
                # Extract values from child elements or attributes
                for child in employee:
                    tag = child.tag
                    if tag.lower() in [id_col.lower(), 'id', 'employee_id']:
                        emp_dict['id'] = child.text or ''
                    elif tag.lower() in [email_col.lower(), 'email', 'email_address']:
                        emp_dict['email'] = child.text or ''
                    elif tag.lower() in [hash_col.lower(), 'password_hash', 'hash']:
                        emp_dict['password_hash'] = child.text or ''
                
                records.append(emp_dict)
            
            logger.info(f"Loaded {len(records)} records from XML")
        except Exception as e:
            logger.error(f"Error loading XML: {e}")
            raise
        
        return records
    
    @staticmethod
    def _load_excel(filepath: str, id_col: str, email_col: str, hash_col: str) -> List[Dict]:
        """Load from Excel file (.xlsx or .xls)"""
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is required for Excel support. Install with: pip install pandas openpyxl")
        
        records = []
        try:
            df = pd.read_excel(filepath)
            
            for _, row in df.iterrows():
                records.append({
                    'id': str(row.get(id_col, '')),
                    'email': str(row.get(email_col, '')),
                    'password_hash': str(row.get(hash_col, ''))
                })
            
            logger.info(f"Loaded {len(records)} records from Excel")
        except Exception as e:
            logger.error(f"Error loading Excel: {e}")
            raise
        
        return records
