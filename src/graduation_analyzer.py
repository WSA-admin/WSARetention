"""
Graduation Analysis for WSA Retention Study

This module identifies likely graduates based on program types and enrollment dates,
then analyzes retention patterns for graduates vs current students.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class GraduationAnalyzer:
    """
    Analyzes graduation patterns and retention rates for graduates vs current students.
    """
    
    def __init__(self, data_processor):
        """
        Initialize with a data processor instance.
        
        Args:
            data_processor: Instance of DataProcessor class
        """
        self.data_processor = data_processor
        
        # Program duration mapping (in years)
        self.program_durations = {
            # Bachelor's programs (4 years)
            'bachelor': 4,
            'computer science': 4,
            'biology': 4, 
            'psychology': 4,
            'economics': 4,
            'kinesiology': 4,
            'business administration': 4,
            'sustainable design engineering': 4,
            
            # Master's programs (2 years)
            'master': 2,
            'mba': 2,
            'master of education': 2,
            'master of digital innovation': 2,
            'master of development economics': 2,
            
            # Diploma/Certificate programs (1-2 years)
            'diploma': 1.5,
            'certificate': 1,
            'project management': 1.5,
            'data analytics': 1.5,
            'marketing and advertising management': 2,
            'business management': 1.5,
            'occupational health and safety': 1,
            
            # Post-baccalaureate (1 year)
            'post baccalaureate': 1,
            'post-baccalaureate': 1,
        }
        
    def classify_graduation_status(self, student_status: str, program: str = None, enrollment_date: str = None, analysis_date: str = None) -> str:
        """
        Classify graduation status using the actual Student Status field from raw data.
        
        Args:
            student_status (str): Actual "Student Status" field from registration data
            program (str): Program of study (kept for compatibility, not used)
            enrollment_date (str): Date of enrollment (kept for compatibility, not used)
            analysis_date (str): Date of analysis (kept for compatibility, not used)
            
        Returns:
            str: 'Graduate', 'Current Student', or 'Unknown'
        """
        if pd.isna(student_status) or student_status == "":
            return 'Unknown'
        
        # Clean and standardize the student status
        status_clean = str(student_status).strip().lower()
        
        # Map actual student status values
        if status_clean in ['graduate', 'graduated']:
            return 'Graduate'
        elif status_clean in ['current student', 'student', 'current']:
            return 'Current Student'
        else:
            # Log unexpected values for debugging
            logger.warning(f"Unexpected student status value: '{student_status}'")
            return 'Unknown'
    
    def _estimate_program_duration(self, program_lower: str) -> float:
        """Estimate program duration based on program name."""
        
        # Check for exact matches first
        for keyword, duration in self.program_durations.items():
            if keyword in program_lower:
                return duration
        
        # Default assumptions based on common patterns
        if any(word in program_lower for word in ['master', 'mba', 'graduate']):
            return 2  # Master's programs
        elif any(word in program_lower for word in ['bachelor', 'undergraduate', 'degree']):
            return 4  # Bachelor's programs
        elif any(word in program_lower for word in ['diploma', 'certificate', 'post']):
            return 1.5  # Diploma/Certificate programs
        else:
            return 2  # Default to 2 years if unsure
    
    def analyze_graduation_retention(self, year: int) -> Dict[str, any]:
        """
        Analyze retention patterns by graduation status.
        
        Args:
            year (int): Year to analyze (2023 or 2024)
            
        Returns:
            Dict containing graduation retention analysis
        """
        logger.info(f"Analyzing graduation retention for {year}...")
        
        # Get matched data
        matched_data = self.data_processor.match_members(year)
        matched_only = matched_data[matched_data['retention_status'] != 'Unknown'].copy()
        
        # Add graduation classification
        matched_only['graduation_status'] = matched_only.apply(
            lambda row: self.classify_graduation_status(
                row['Student Status'], 
                row['Program of Study'], 
                row['Date of Enrollment']
            ), axis=1
        )
        
        # Analyze by graduation status
        graduation_analysis = {}
        
        for grad_status in ['Graduate', 'Current Student', 'Unknown']:
            subset = matched_only[matched_only['graduation_status'] == grad_status]
            
            if len(subset) > 0:
                retention_counts = subset['retention_status'].value_counts()
                total = len(subset)
                
                graduation_analysis[grad_status] = {
                    'total_members': total,
                    'retention_breakdown': {
                        'Still in PEI': retention_counts.get('Still in PEI', 0),
                        'No longer in PEI': retention_counts.get('No longer in PEI', 0),
                        'Inconclusive': retention_counts.get('Inconclusive', 0)
                    },
                    'retention_percentages': {
                        'Still in PEI': (retention_counts.get('Still in PEI', 0) / total) * 100,
                        'No longer in PEI': (retention_counts.get('No longer in PEI', 0) / total) * 100,
                        'Inconclusive': (retention_counts.get('Inconclusive', 0) / total) * 100
                    }
                }
        
        # Overall summary
        total_analyzed = len(matched_only)
        graduation_summary = {
            'year': year,
            'total_analyzed': total_analyzed,
            'graduation_distribution': {
                'Graduate': len(matched_only[matched_only['graduation_status'] == 'Graduate']),
                'Current Student': len(matched_only[matched_only['graduation_status'] == 'Current Student']),
                'Unknown': len(matched_only[matched_only['graduation_status'] == 'Unknown'])
            },
            'by_graduation_status': graduation_analysis,
            'key_insights': self._generate_graduation_insights(graduation_analysis, year)
        }
        
        return graduation_summary
    
    def _generate_graduation_insights(self, analysis: Dict, year: int) -> List[str]:
        """Generate key insights from graduation analysis."""
        insights = []
        
        if 'Graduate' in analysis and 'Current Student' in analysis:
            grad_retention = analysis['Graduate']['retention_percentages']['Still in PEI']
            student_retention = analysis['Current Student']['retention_percentages']['Still in PEI']
            
            if grad_retention > student_retention:
                diff = grad_retention - student_retention
                insights.append(f"Graduates have higher retention rate: {grad_retention:.1f}% vs {student_retention:.1f}% (+{diff:.1f}%)")
            else:
                diff = student_retention - grad_retention
                insights.append(f"Current students have higher retention rate: {student_retention:.1f}% vs {grad_retention:.1f}% (+{diff:.1f}%)")
            
            grad_leaving = analysis['Graduate']['retention_percentages']['No longer in PEI']
            student_leaving = analysis['Current Student']['retention_percentages']['No longer in PEI']
            
            if grad_leaving > student_leaving:
                diff = grad_leaving - student_leaving
                insights.append(f"Graduates leave PEI more often: {grad_leaving:.1f}% vs {student_leaving:.1f}% (+{diff:.1f}%)")
            else:
                diff = student_leaving - grad_leaving
                insights.append(f"Current students leave PEI more often: {student_leaving:.1f}% vs {grad_leaving:.1f}% (+{diff:.1f}%)")
        
        return insights
    
    def compare_graduation_retention_by_year(self) -> Dict[str, any]:
        """Compare graduation retention patterns between 2023 and 2024."""
        logger.info("Comparing graduation retention between 2023 and 2024...")
        
        analysis_2023 = self.analyze_graduation_retention(2023)
        analysis_2024 = self.analyze_graduation_retention(2024)
        
        comparison = {
            '2023': analysis_2023,
            '2024': analysis_2024,
            'year_over_year_changes': self._calculate_yoy_changes(analysis_2023, analysis_2024)
        }
        
        return comparison
    
    def _calculate_yoy_changes(self, analysis_2023: Dict, analysis_2024: Dict) -> Dict:
        """Calculate year-over-year changes in graduation retention."""
        changes = {}
        
        for grad_status in ['Graduate', 'Current Student']:
            if grad_status in analysis_2023['by_graduation_status'] and grad_status in analysis_2024['by_graduation_status']:
                retention_2023 = analysis_2023['by_graduation_status'][grad_status]['retention_percentages']['Still in PEI']
                retention_2024 = analysis_2024['by_graduation_status'][grad_status]['retention_percentages']['Still in PEI']
                
                changes[grad_status] = {
                    'retention_change': retention_2024 - retention_2023,
                    '2023_retention': retention_2023,
                    '2024_retention': retention_2024
                }
        
        return changes
    
    def export_graduation_analysis(self, filename: str = None) -> str:
        """Export graduation analysis to CSV for further review."""
        if filename is None:
            filename = "graduation_retention_analysis.csv"
        
        # Get both years' data
        matched_2023 = self.data_processor.match_members(2023)
        matched_2024 = self.data_processor.match_members(2024)
        
        # Add graduation status
        for df, year in [(matched_2023, 2023), (matched_2024, 2024)]:
            df['graduation_status'] = df.apply(
                lambda row: self.classify_graduation_status(
                    row['Student Status'], 
                    row['Program of Study'], 
                    row['Date of Enrollment']
                ), axis=1
            )
            df['analysis_year'] = year
        
        # Combine and export
        combined = pd.concat([matched_2023, matched_2024], ignore_index=True)
        combined = combined[combined['retention_status'] != 'Unknown']  # Only matched records
        
        # Select relevant columns
        export_columns = [
            'Name', 'Email', 'Institution of Study', 'Program of Study',
            'Date of Enrollment', 'retention_status', 'graduation_status',
            'analysis_year', 'Country of Origin'
        ]
        
        export_data = combined[export_columns].copy()
        
        from pathlib import Path
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        export_data.to_csv(filepath, index=False)
        
        logger.info(f"Exported graduation analysis to {filepath}")
        return str(filepath) 