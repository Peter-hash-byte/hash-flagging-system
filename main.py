#!/usr/bin/env python3
"""Command-line interface for Hash Flagging System"""

import argparse
import sys
import logging
from hash_flagging_system import HashFlagger, FileLoader, ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Hash Flagging System - Detect duplicate password hashes across employee records',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --file employees.csv --output report.html
  python main.py --file employees.json --threshold 3
  python main.py --file data.xlsx --format xlsx --id-column employee_id
  python main.py --file records.xml --output report.json --output-format json
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        required=True,
        help='Path to employee records file'
    )
    
    parser.add_argument(
        '--format',
        choices=['csv', 'tsv', 'json', 'xml', 'xlsx', 'xls'],
        help='File format (auto-detected if not specified)'
    )
    
    parser.add_argument(
        '--id-column',
        default='id',
        help='Name of the employee ID column (default: id)'
    )
    
    parser.add_argument(
        '--email-column',
        default='email',
        help='Name of the email column (default: email)'
    )
    
    parser.add_argument(
        '--hash-column',
        default='password_hash',
        help='Name of the password hash column (default: password_hash)'
    )
    
    parser.add_argument(
        '--threshold',
        type=int,
        default=2,
        help='Minimum occurrences to flag as duplicate (default: 2)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path for the report'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['html', 'json', 'csv', 'txt'],
        default='html',
        help='Output report format (default: html)'
    )
    
    parser.add_argument(
        '--case-sensitive',
        action='store_true',
        help='Perform case-sensitive hash comparison'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        # Load records
        logger.info(f"Loading records from {args.file}...")
        records = FileLoader.load(
            args.file,
            format_type=args.format,
            id_column=args.id_column,
            email_column=args.email_column,
            hash_column=args.hash_column
        )
        
        logger.info(f"Successfully loaded {len(records)} employee records")
        
        # Initialize flagger
        flagger = HashFlagger(case_sensitive=args.case_sensitive)
        flagger.add_records(records)
        
        # Find duplicates
        logger.info(f"Searching for duplicate hashes (threshold: {args.threshold})...")
        flagger.find_duplicates(threshold=args.threshold)
        
        # Get results
        summary = flagger.get_duplicate_summary()
        flagged = flagger.flag_employees()
        
        # Print summary
        print("\n" + "=" * 80)
        print("HASH FLAGGING RESULTS")
        print("=" * 80)
        print(f"Total Duplicate Hashes: {summary.get('total_duplicate_hashes', 0)}")
        print(f"Total Employees Affected: {summary.get('total_employees_affected', 0)}")
        print("=" * 80)
        
        if flagged:
            print(f"\n⚠️  Found {len(flagged)} flagged employees:\n")
            for emp in flagged[:10]:  # Show first 10
                print(f"  • {emp['email']} (ID: {emp['id']}) - Risk: {emp['risk_level']}")
                print(f"    Shared password with {emp['shared_with_count']} other(s)")
            
            if len(flagged) > 10:
                print(f"  ... and {len(flagged) - 10} more")
        else:
            print("\n✅ No duplicate password hashes found!")
        
        # Generate and save report if output specified
        if args.output:
            logger.info(f"Generating {args.output_format} report...")
            reporter = ReportGenerator(flagged, summary)
            reporter.save_report(args.output, format_type=args.output_format)
            logger.info(f"Report saved to {args.output}")
        else:
            # Print default text report
            reporter = ReportGenerator(flagged, summary)
            print("\n" + reporter.generate_text_report())
        
        return 0
    
    except FileNotFoundError:
        logger.error(f"File not found: {args.file}")
        return 1
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
