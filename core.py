"""Core functionality for hash flagging and duplicate detection"""

import hashlib
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HashFlagger:
    """Main class for detecting duplicate hashes in employee records"""
    
    def __init__(self, case_sensitive: bool = False, hash_algorithm: str = 'sha256'):
        """
        Initialize the HashFlagger
        
        Args:
            case_sensitive: Whether hash comparison is case-sensitive
            hash_algorithm: Algorithm to use for hashing ('sha256', 'md5', 'sha1')
        """
        self.case_sensitive = case_sensitive
        self.hash_algorithm = hash_algorithm
        self.employee_records = []
        self.hash_map = defaultdict(list)  # Maps hash -> [employees]
        self.duplicates = {}
        
    def add_record(self, employee_id: str, email: str, password_hash: str):
        """Add a single employee record"""
        record = {
            'id': employee_id,
            'email': email,
            'password_hash': password_hash
        }
        self.employee_records.append(record)
        
        # Normalize hash for comparison
        normalized_hash = self._normalize_hash(password_hash)
        self.hash_map[normalized_hash].append(record)
    
    def add_records(self, records: List[Dict]):
        """
        Add multiple employee records
        
        Args:
            records: List of dicts with keys: 'id', 'email', 'password_hash'
        """
        for record in records:
            self.add_record(
                record.get('id', 'UNKNOWN'),
                record.get('email', 'UNKNOWN'),
                record.get('password_hash', '')
            )
    
    def _normalize_hash(self, hash_str: str) -> str:
        """Normalize hash for comparison"""
        if not self.case_sensitive:
            hash_str = hash_str.lower()
        return hash_str.strip()
    
    def find_duplicates(self, threshold: int = 2) -> Dict[str, List[Dict]]:
        """
        Find duplicate hashes
        
        Args:
            threshold: Minimum number of occurrences to flag as duplicate
            
        Returns:
            Dictionary mapping hash -> list of employee records with that hash
        """
        self.duplicates = {}
        
        for hash_value, employees in self.hash_map.items():
            if len(employees) >= threshold:
                self.duplicates[hash_value] = employees
                logger.warning(
                    f"Duplicate hash found: {len(employees)} employees share the same password hash"
                )
        
        return self.duplicates
    
    def get_duplicate_summary(self) -> Dict:
        """Get summary statistics of duplicates"""
        if not self.duplicates:
            return {"total_duplicates": 0, "employees_affected": 0}
        
        total_duplicates = len(self.duplicates)
        employees_affected = sum(len(emps) for emps in self.duplicates.values())
        
        return {
            "total_duplicate_hashes": total_duplicates,
            "total_employees_affected": employees_affected,
            "duplicate_groups": [
                {
                    "hash": hash_val,
                    "count": len(emps),
                    "employees": [e['email'] for e in emps]
                }
                for hash_val, emps in self.duplicates.items()
            ]
        }
    
    def flag_employees(self) -> List[Dict]:
        """
        Get list of flagged employees
        
        Returns:
            List of employee records that share password hashes
        """
        flagged = []
        
        for hash_val, employees in self.duplicates.items():
            for emp in employees:
                flagged.append({
                    **emp,
                    'shared_with_count': len(employees) - 1,
                    'shared_with_emails': [
                        e['email'] for e in employees if e['email'] != emp['email']
                    ],
                    'risk_level': self._calculate_risk_level(len(employees))
                })
        
        return sorted(flagged, key=lambda x: x['shared_with_count'], reverse=True)
    
    def _calculate_risk_level(self, occurrence_count: int) -> str:
        """Calculate risk level based on number of occurrences"""
        if occurrence_count >= 5:
            return "CRITICAL"
        elif occurrence_count >= 3:
            return "HIGH"
        elif occurrence_count >= 2:
            return "MEDIUM"
        return "LOW"
    
    def clear(self):
        """Clear all records and duplicates"""
        self.employee_records = []
        self.hash_map = defaultdict(list)
        self.duplicates = {}
        logger.info("All data cleared")
