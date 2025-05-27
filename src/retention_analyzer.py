"""
Retention Analyzer Module for WSA Retention Analysis

This module contains the core analysis logic for calculating retention statistics
and generating comprehensive reports.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path
from datetime import datetime
import json

from data_processor import DataProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetentionAnalyzer:
    """
    Main class for performing retention analysis on WSA member data.
    """
    
    def __init__(self, data_dir: str = "data/raw"):
        """
        Initialize the RetentionAnalyzer.
        
        Args:
            data_dir (str): Directory containing the raw CSV files
        """
        self.data_processor = DataProcessor(data_dir)
        self.matched_data = {}
        
    def load_and_preprocess_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load and preprocess all data for analysis.
        
        Returns:
            Dict[str, pd.DataFrame]: Preprocessed datasets
        """
        logger.info("Loading and preprocessing data for retention analysis...")
        return self.data_processor.preprocess_data()
    
    def analyze_retention(self, year: int) -> Dict[str, any]:
        """
        Perform comprehensive retention analysis for a specific year.
        
        Args:
            year (int): Year to analyze (2023 or 2024)
            
        Returns:
            Dict[str, any]: Comprehensive analysis results
        """
        logger.info(f"Starting retention analysis for {year}...")
        
        # Ensure data is loaded
        if self.data_processor.retention_survey is None:
            self.load_and_preprocess_data()
        
        # Match members with retention survey
        matched_data = self.data_processor.match_members(year)
        self.matched_data[year] = matched_data
        
        # Calculate basic statistics
        total_members = len(matched_data)
        matched_members = len(matched_data[matched_data['retention_status'] != 'Unknown'])
        
        # Count retention statuses
        status_counts = matched_data['retention_status'].value_counts()
        
        # Calculate percentages (based on matched members)
        if matched_members > 0:
            still_in_pei = status_counts.get('Still in PEI', 0)
            no_longer_in_pei = status_counts.get('No longer in PEI', 0)
            inconclusive = status_counts.get('Inconclusive', 0)
            
            still_in_pei_pct = (still_in_pei / matched_members) * 100
            no_longer_in_pei_pct = (no_longer_in_pei / matched_members) * 100
            inconclusive_pct = (inconclusive / matched_members) * 100
        else:
            still_in_pei = no_longer_in_pei = inconclusive = 0
            still_in_pei_pct = no_longer_in_pei_pct = inconclusive_pct = 0
        
        # Institution-wise breakdown
        institution_breakdown = self._analyze_by_institution(matched_data)
        
        # Program-wise breakdown
        program_breakdown = self._analyze_by_program(matched_data)
        
        # Country of origin breakdown
        country_breakdown = self._analyze_by_country(matched_data)
        
        # Match quality analysis
        match_quality = self._analyze_match_quality(matched_data)
        
        # Timeline analysis
        timeline_analysis = self._analyze_timeline(matched_data, year)
        
        results = {
            'year': year,
            'analysis_date': datetime.now().isoformat(),
            'summary': {
                'total_registered_members': total_members,
                'members_with_retention_data': matched_members,
                'match_rate_percent': (matched_members / total_members * 100) if total_members > 0 else 0,
                'still_in_pei': still_in_pei,
                'no_longer_in_pei': no_longer_in_pei,
                'inconclusive': inconclusive,
                'unknown': status_counts.get('Unknown', 0),
                'still_in_pei_percent': still_in_pei_pct,
                'no_longer_in_pei_percent': no_longer_in_pei_pct,
                'inconclusive_percent': inconclusive_pct
            },
            'institution_breakdown': institution_breakdown,
            'program_breakdown': program_breakdown,
            'country_breakdown': country_breakdown,
            'match_quality': match_quality,
            'timeline_analysis': timeline_analysis,
            'raw_data_sample': matched_data.head(10).to_dict('records')
        }
        
        logger.info(f"Retention analysis completed for {year}")
        return results
    
    def _analyze_by_institution(self, data: pd.DataFrame) -> Dict[str, Dict]:
        """
        Analyze retention by institution.
        
        Args:
            data (pd.DataFrame): Matched member data
            
        Returns:
            Dict[str, Dict]: Institution-wise retention breakdown
        """
        institution_analysis = {}
        
        for institution in data['Institution of Study'].dropna().unique():
            inst_data = data[data['Institution of Study'] == institution]
            total = len(inst_data)
            
            status_counts = inst_data['retention_status'].value_counts()
            matched = len(inst_data[inst_data['retention_status'] != 'Unknown'])
            
            if matched > 0:
                still_in_pei = status_counts.get('Still in PEI', 0)
                no_longer = status_counts.get('No longer in PEI', 0)
                inconclusive = status_counts.get('Inconclusive', 0)
                
                institution_analysis[institution] = {
                    'total_members': total,
                    'matched_members': matched,
                    'still_in_pei': still_in_pei,
                    'no_longer_in_pei': no_longer,
                    'inconclusive': inconclusive,
                    'still_in_pei_percent': (still_in_pei / matched * 100),
                    'retention_rate': (still_in_pei / matched * 100)
                }
        
        return institution_analysis
    
    def _analyze_by_program(self, data: pd.DataFrame) -> Dict[str, Dict]:
        """
        Analyze retention by program of study.
        
        Args:
            data (pd.DataFrame): Matched member data
            
        Returns:
            Dict[str, Dict]: Program-wise retention breakdown
        """
        program_analysis = {}
        
        # Get top programs (with at least 5 members)
        program_counts = data['Program of Study'].value_counts()
        top_programs = program_counts[program_counts >= 5].index
        
        for program in top_programs:
            prog_data = data[data['Program of Study'] == program]
            total = len(prog_data)
            
            status_counts = prog_data['retention_status'].value_counts()
            matched = len(prog_data[prog_data['retention_status'] != 'Unknown'])
            
            if matched > 0:
                still_in_pei = status_counts.get('Still in PEI', 0)
                no_longer = status_counts.get('No longer in PEI', 0)
                inconclusive = status_counts.get('Inconclusive', 0)
                
                program_analysis[program] = {
                    'total_members': total,
                    'matched_members': matched,
                    'still_in_pei': still_in_pei,
                    'no_longer_in_pei': no_longer,
                    'inconclusive': inconclusive,
                    'retention_rate': (still_in_pei / matched * 100)
                }
        
        return program_analysis
    
    def _analyze_by_country(self, data: pd.DataFrame) -> Dict[str, Dict]:
        """
        Analyze retention by country of origin.
        
        Args:
            data (pd.DataFrame): Matched member data
            
        Returns:
            Dict[str, Dict]: Country-wise retention breakdown
        """
        country_analysis = {}
        
        # Get top countries (with at least 3 members)
        country_counts = data['Country of Origin'].value_counts()
        top_countries = country_counts[country_counts >= 3].index
        
        for country in top_countries:
            country_data = data[data['Country of Origin'] == country]
            total = len(country_data)
            
            status_counts = country_data['retention_status'].value_counts()
            matched = len(country_data[country_data['retention_status'] != 'Unknown'])
            
            if matched > 0:
                still_in_pei = status_counts.get('Still in PEI', 0)
                no_longer = status_counts.get('No longer in PEI', 0)
                inconclusive = status_counts.get('Inconclusive', 0)
                
                country_analysis[country] = {
                    'total_members': total,
                    'matched_members': matched,
                    'still_in_pei': still_in_pei,
                    'no_longer_in_pei': no_longer,
                    'inconclusive': inconclusive,
                    'retention_rate': (still_in_pei / matched * 100)
                }
        
        return country_analysis
    
    def _analyze_match_quality(self, data: pd.DataFrame) -> Dict[str, any]:
        """
        Analyze the quality of member matching.
        
        Args:
            data (pd.DataFrame): Matched member data
            
        Returns:
            Dict[str, any]: Match quality statistics
        """
        match_types = data['match_type'].value_counts()
        total_matches = len(data[data['retention_status'] != 'Unknown'])
        
        quality_analysis = {
            'total_matches': total_matches,
            'match_type_breakdown': match_types.to_dict(),
            'average_confidence': data[data['retention_status'] != 'Unknown']['match_confidence'].mean(),
            'high_confidence_matches': len(data[data['match_confidence'] >= 95]),
            'medium_confidence_matches': len(data[(data['match_confidence'] >= 80) & (data['match_confidence'] < 95)]),
            'low_confidence_matches': len(data[(data['match_confidence'] < 80) & (data['match_confidence'] > 0)])
        }
        
        return quality_analysis
    
    def _analyze_timeline(self, data: pd.DataFrame, year: int) -> Dict[str, any]:
        """
        Analyze retention trends over time within the year.
        
        Args:
            data (pd.DataFrame): Matched member data
            year (int): Year being analyzed
            
        Returns:
            Dict[str, any]: Timeline analysis
        """
        # Filter data with valid enrollment dates
        timeline_data = data[data['enrollment_date'].notna()].copy()
        timeline_data['enrollment_month'] = timeline_data['enrollment_date'].dt.month
        
        monthly_analysis = {}
        
        for month in range(1, 13):
            month_data = timeline_data[timeline_data['enrollment_month'] == month]
            if len(month_data) > 0:
                status_counts = month_data['retention_status'].value_counts()
                matched = len(month_data[month_data['retention_status'] != 'Unknown'])
                
                if matched > 0:
                    still_in_pei = status_counts.get('Still in PEI', 0)
                    retention_rate = (still_in_pei / matched * 100)
                else:
                    retention_rate = 0
                
                monthly_analysis[month] = {
                    'total_enrollments': len(month_data),
                    'matched_members': matched,
                    'retention_rate': retention_rate
                }
        
        return {
            'monthly_breakdown': monthly_analysis,
            'total_with_dates': len(timeline_data),
            'missing_dates': len(data) - len(timeline_data)
        }
    
    def print_summary(self, results: Dict[str, any], year: int) -> None:
        """
        Print a formatted summary of the retention analysis.
        
        Args:
            results (Dict[str, any]): Analysis results
            year (int): Year analyzed
        """
        summary = results['summary']
        
        print(f"\n{'='*60}")
        print(f"WSA RETENTION ANALYSIS SUMMARY - {year}")
        print(f"{'='*60}")
        
        print(f"\nOVERALL STATISTICS:")
        print(f"  Total Registered Members: {summary['total_registered_members']:,}")
        print(f"  Members with Retention Data: {summary['members_with_retention_data']:,}")
        print(f"  Match Rate: {summary['match_rate_percent']:.1f}%")
        
        print(f"\nRETENTION BREAKDOWN:")
        print(f"  Still in PEI: {summary['still_in_pei']:,} ({summary['still_in_pei_percent']:.1f}%)")
        print(f"  No Longer in PEI: {summary['no_longer_in_pei']:,} ({summary['no_longer_in_pei_percent']:.1f}%)")
        print(f"  Inconclusive: {summary['inconclusive']:,} ({summary['inconclusive_percent']:.1f}%)")
        print(f"  Unknown: {summary['unknown']:,}")
        
        print(f"\nTOP INSTITUTIONS BY RETENTION RATE:")
        inst_data = results['institution_breakdown']
        sorted_institutions = sorted(inst_data.items(), key=lambda x: x[1]['retention_rate'], reverse=True)
        
        for i, (institution, data) in enumerate(sorted_institutions[:5]):
            print(f"  {i+1}. {institution}: {data['retention_rate']:.1f}% ({data['still_in_pei']}/{data['matched_members']})")
        
        print(f"\nMATCH QUALITY:")
        match_quality = results['match_quality']
        print(f"  Average Confidence: {match_quality['average_confidence']:.1f}%")
        print(f"  High Confidence Matches (95%+): {match_quality['high_confidence_matches']:,}")
        print(f"  Medium Confidence Matches (80-94%): {match_quality['medium_confidence_matches']:,}")
        
        print(f"\n{'='*60}")
    
    def save_results(self, results: Dict[str, any], filename: str = None) -> str:
        """
        Save analysis results to a JSON file.
        
        Args:
            results (Dict[str, any]): Analysis results
            filename (str, optional): Output filename
            
        Returns:
            str: Path to saved file
        """
        if filename is None:
            year = results['year']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"retention_analysis_{year}_{timestamp}.json"
        
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved to {filepath}")
        return str(filepath)
    
    def compare_years(self, results_2023: Dict[str, any], results_2024: Dict[str, any]) -> Dict[str, any]:
        """
        Compare retention analysis results between 2023 and 2024.
        
        Args:
            results_2023 (Dict[str, any]): 2023 analysis results
            results_2024 (Dict[str, any]): 2024 analysis results
            
        Returns:
            Dict[str, any]: Comparison analysis
        """
        comparison = {
            'comparison_date': datetime.now().isoformat(),
            'summary_comparison': {
                '2023': results_2023['summary'],
                '2024': results_2024['summary'],
                'changes': {
                    'total_members_change': results_2024['summary']['total_registered_members'] - results_2023['summary']['total_registered_members'],
                    'retention_rate_change': results_2024['summary']['still_in_pei_percent'] - results_2023['summary']['still_in_pei_percent'],
                    'match_rate_change': results_2024['summary']['match_rate_percent'] - results_2023['summary']['match_rate_percent']
                }
            },
            'institution_comparison': self._compare_institutions(results_2023, results_2024),
            'country_comparison': self._compare_countries(results_2023, results_2024)
        }
        
        return comparison
    
    def _compare_institutions(self, results_2023: Dict, results_2024: Dict) -> Dict[str, Dict]:
        """Compare institution retention rates between years."""
        inst_2023 = results_2023['institution_breakdown']
        inst_2024 = results_2024['institution_breakdown']
        
        comparison = {}
        all_institutions = set(inst_2023.keys()) | set(inst_2024.keys())
        
        for institution in all_institutions:
            rate_2023 = inst_2023.get(institution, {}).get('retention_rate', 0)
            rate_2024 = inst_2024.get(institution, {}).get('retention_rate', 0)
            
            comparison[institution] = {
                '2023_retention_rate': rate_2023,
                '2024_retention_rate': rate_2024,
                'change': rate_2024 - rate_2023
            }
        
        return comparison
    
    def _compare_countries(self, results_2023: Dict, results_2024: Dict) -> Dict[str, Dict]:
        """Compare country retention rates between years."""
        country_2023 = results_2023['country_breakdown']
        country_2024 = results_2024['country_breakdown']
        
        comparison = {}
        all_countries = set(country_2023.keys()) | set(country_2024.keys())
        
        for country in all_countries:
            rate_2023 = country_2023.get(country, {}).get('retention_rate', 0)
            rate_2024 = country_2024.get(country, {}).get('retention_rate', 0)
            
            comparison[country] = {
                '2023_retention_rate': rate_2023,
                '2024_retention_rate': rate_2024,
                'change': rate_2024 - rate_2023
            }
        
        return comparison 