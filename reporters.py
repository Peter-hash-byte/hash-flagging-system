"""Report generation for hash flagging results"""

import json
from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate reports from duplicate hash analysis"""
    
    def __init__(self, flagged_employees: List[Dict], summary: Dict):
        """
        Initialize report generator
        
        Args:
            flagged_employees: List of flagged employee records
            summary: Summary statistics dictionary
        """
        self.flagged_employees = flagged_employees
        self.summary = summary
        self.timestamp = datetime.now()
    
    def generate_json_report(self) -> str:
        """Generate JSON format report"""
        report = {
            "generated_at": self.timestamp.isoformat(),
            "summary": self.summary,
            "flagged_employees": self.flagged_employees
        }
        return json.dumps(report, indent=2)
    
    def generate_csv_report(self) -> str:
        """Generate CSV format report"""
        if not self.flagged_employees:
            return "No duplicates found"
        
        lines = ["ID,Email,Shared_With_Count,Risk_Level,Shared_With_Emails"]
        
        for emp in self.flagged_employees:
            shared_emails = ";".join(emp.get('shared_with_emails', []))
            line = f"{emp['id']},{emp['email']},{emp['shared_with_count']},{emp['risk_level']},\"{shared_emails}\""
            lines.append(line)
        
        return "\n".join(lines)
    
    def generate_html_report(self) -> str:
        """Generate HTML format report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hash Flagging Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
        }}
        .summary {{
            background-color: #f9f9f9;
            padding: 15px;
            border-left: 4px solid #007bff;
            margin: 20px 0;
        }}
        .critical {{
            background-color: #fff3cd;
            color: #856404;
            padding: 10px;
            border-left: 4px solid #ff0000;
            margin: 10px 0;
        }}
        .high {{
            background-color: #fff3cd;
            color: #856404;
            padding: 10px;
            border-left: 4px solid #ff9800;
            margin: 10px 0;
        }}
        .medium {{
            background-color: #e7f3ff;
            color: #004085;
            padding: 10px;
            border-left: 4px solid #ffc107;
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #007bff;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Hash Flagging Security Report</h1>
        
        <div class="summary">
            <h2>Summary</h2>
            <p><strong>Total Duplicate Hashes Found:</strong> {self.summary.get('total_duplicate_hashes', 0)}</p>
            <p><strong>Total Employees Affected:</strong> {self.summary.get('total_employees_affected', 0)}</p>
        </div>
        
        <h2>⚠️ Flagged Employees</h2>
"""
        
        if not self.flagged_employees:
            html += "<p>No duplicates found. All employees have unique password hashes.</p>"
        else:
            html += "<table><tr><th>Employee ID</th><th>Email</th><th>Risk Level</th><th>Shared With Count</th><th>Shared With</th></tr>"
            
            for emp in self.flagged_employees:
                risk_class = emp['risk_level'].lower()
                shared_emails = ", ".join(emp.get('shared_with_emails', []))
                
                html += f"""
            <tr>
                <td>{emp['id']}</td>
                <td>{emp['email']}</td>
                <td><span class="{risk_class}">{emp['risk_level']}</span></td>
                <td>{emp['shared_with_count']}</td>
                <td>{shared_emails}</td>
            </tr>
"""
            
            html += "</table>"
        
        html += f"""
        <div class="timestamp">
            <p>Report generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def generate_text_report(self) -> str:
        """Generate plain text format report"""
        lines = [
            "=" * 80,
            "HASH FLAGGING SECURITY REPORT",
            "=" * 80,
            f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "SUMMARY",
            "-" * 80,
            f"Total Duplicate Hashes: {self.summary.get('total_duplicate_hashes', 0)}",
            f"Total Employees Affected: {self.summary.get('total_employees_affected', 0)}",
            "",
            "FLAGGED EMPLOYEES",
            "-" * 80,
        ]
        
        if not self.flagged_employees:
            lines.append("No duplicates found.")
        else:
            for emp in self.flagged_employees:
                lines.append(f"\nEmployee ID: {emp['id']}")
                lines.append(f"Email: {emp['email']}")
                lines.append(f"Risk Level: {emp['risk_level']}")
                lines.append(f"Shared With {emp['shared_with_count']} other employee(s):")
                for email in emp.get('shared_with_emails', []):
                    lines.append(f"  - {email}")
        
        lines.append("\n" + "=" * 80)
        return "\n".join(lines)
    
    def save_report(self, filepath: str, format_type: str = 'html'):
        """
        Save report to file
        
        Args:
            filepath: Output file path
            format_type: Report format ('html', 'json', 'csv', 'txt')
        """
        format_type = format_type.lower()
        
        if format_type == 'html':
            content = self.generate_html_report()
        elif format_type == 'json':
            content = self.generate_json_report()
        elif format_type == 'csv':
            content = self.generate_csv_report()
        elif format_type in ['txt', 'text']:
            content = self.generate_text_report()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Report saved to {filepath}")
