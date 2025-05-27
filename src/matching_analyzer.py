"""
Enhanced Matching Analyzer for WSA Retention Analysis

This module provides advanced matching capabilities and analysis tools
to improve the matching rate between registration and retention survey data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from fuzzywuzzy import fuzz, process
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class MatchingAnalyzer:
    """
    Advanced matching analyzer with improved algorithms and diagnostic tools.
    """
    
    def __init__(self, data_processor):
        """
        Initialize with a data processor instance.
        
        Args:
            data_processor: Instance of DataProcessor class
        """
        self.data_processor = data_processor
        # Ensure data is loaded and preprocessed if not already done
        if self.data_processor.retention_survey is None:
            self.data_processor.preprocess_data()
        self.unmatched_analysis = {}
        
    def analyze_unmatched_records(self, year: int) -> Dict[str, any]:
        """
        Analyze unmatched records to understand why they're not matching.
        
        Args:
            year (int): Year to analyze (2023 or 2024)
            
        Returns:
            Dict containing detailed analysis of unmatched records
        """
        logger.info(f"Analyzing unmatched records for {year}...")
        
        # Get the registration data
        if year == 2023:
            registrations = self.data_processor.registrations_2023
        elif year == 2024:
            registrations = self.data_processor.registrations_2024
        else:
            raise ValueError("Year must be 2023 or 2024")
        
        # Perform matching to identify unmatched records
        matched_data = self.data_processor.match_members(year)
        unmatched = matched_data[matched_data['retention_status'] == 'Unknown'].copy()
        
        logger.info(f"Found {len(unmatched)} unmatched records in {year}")
        
        # Analyze patterns in unmatched data
        analysis = {
            'year': year,
            'total_registrations': len(registrations),
            'total_unmatched': len(unmatched),
            'unmatched_percentage': (len(unmatched) / len(registrations)) * 100,
            'unmatched_records': unmatched.to_dict('records'),
            'patterns': self._analyze_unmatched_patterns(unmatched),
            'potential_matches': self._find_potential_matches(unmatched, year),
            'suggestions': self._generate_matching_suggestions(unmatched)
        }
        
        self.unmatched_analysis[year] = analysis
        return analysis
    
    def _analyze_unmatched_patterns(self, unmatched: pd.DataFrame) -> Dict[str, any]:
        """Analyze patterns in unmatched data."""
        patterns = {}
        
        # Institution breakdown
        patterns['by_institution'] = unmatched['Institution of Study'].value_counts().to_dict()
        
        # Program breakdown
        patterns['by_program'] = unmatched['Program of Study'].value_counts().to_dict()
        
        # Country breakdown
        patterns['by_country'] = unmatched['Country of Origin'].value_counts().to_dict()
        
        # Email domain analysis
        unmatched['email_domain'] = unmatched['email_clean'].str.extract(r'@(.+)')
        patterns['by_email_domain'] = unmatched['email_domain'].value_counts().to_dict()
        
        # Name characteristics
        patterns['name_characteristics'] = {
            'avg_name_length': unmatched['name_clean'].str.len().mean(),
            'names_with_special_chars': len(unmatched[unmatched['Name'].str.contains(r'[^\w\s]', na=False)]),
            'very_short_names': len(unmatched[unmatched['name_clean'].str.len() < 5]),
            'very_long_names': len(unmatched[unmatched['name_clean'].str.len() > 30])
        }
        
        return patterns
    
    def _find_potential_matches(self, unmatched: pd.DataFrame, year: int) -> List[Dict]:
        """Find potential matches using more relaxed criteria."""
        potential_matches = []
        survey_data = self.data_processor.retention_survey
        
        for idx, person in unmatched.iterrows():
            name = person['name_clean']
            email = person['email_clean']
            
            # Try different matching strategies
            matches = []
            
            # 1. Partial name matching
            if name:
                name_parts = name.split()
                if len(name_parts) >= 2:
                    # Try first + last name combinations
                    first_last = f"{name_parts[0]} {name_parts[-1]}"
                    partial_matches = process.extract(first_last, survey_data['name_clean'], limit=3)
                    for match_result in partial_matches:
                        match, score = match_result[0], match_result[1]
                        if score >= 70:
                            survey_row = survey_data[survey_data['name_clean'] == match].iloc[0]
                            matches.append({
                                'type': 'partial_name',
                                'score': score,
                                'matched_name': survey_row['Name'],
                                'matched_email': survey_row['Email Address'],
                                'status': survey_row['Status']
                            })
            
            # 2. Email domain matching
            if email and '@' in email:
                email_parts = email.split('@')
                username = email_parts[0]
                domain = email_parts[1]
                
                # Look for same domain with different username
                same_domain = survey_data[survey_data['email_clean'].str.contains(f'@{domain}', na=False)]
                for _, survey_row in same_domain.iterrows():
                    survey_username = survey_row['email_clean'].split('@')[0]
                    username_score = fuzz.ratio(username, survey_username)
                    if username_score >= 60:
                        matches.append({
                            'type': 'email_domain',
                            'score': username_score,
                            'matched_name': survey_row['Name'],
                            'matched_email': survey_row['Email Address'],
                            'status': survey_row['Status']
                        })
            
            # 3. Nickname/variant matching
            if name:
                # Common nickname patterns
                name_variants = self._generate_name_variants(name)
                for variant in name_variants:
                    variant_matches = process.extract(variant, survey_data['name_clean'], limit=2)
                    for match_result in variant_matches:
                        match, score = match_result[0], match_result[1]
                        if score >= 80:
                            survey_row = survey_data[survey_data['name_clean'] == match].iloc[0]
                            matches.append({
                                'type': 'name_variant',
                                'score': score,
                                'matched_name': survey_row['Name'],
                                'matched_email': survey_row['Email Address'],
                                'status': survey_row['Status'],
                                'variant_used': variant
                            })
            
            if matches:
                potential_matches.append({
                    'registration_name': person['Name'],
                    'registration_email': person['Email'],
                    'potential_matches': matches[:5]  # Top 5 matches
                })
        
        return potential_matches
    
    def _generate_name_variants(self, name: str) -> List[str]:
        """Generate common name variants and nicknames."""
        variants = []
        name_parts = name.split()
        
        if len(name_parts) >= 2:
            # Try reversing first and last name
            variants.append(f"{name_parts[-1]} {name_parts[0]}")
            
            # Try with middle initials removed
            if len(name_parts) > 2:
                variants.append(f"{name_parts[0]} {name_parts[-1]}")
            
            # Common nickname mappings
            nickname_map = {
                'william': 'bill', 'robert': 'bob', 'james': 'jim', 'richard': 'rick',
                'michael': 'mike', 'david': 'dave', 'christopher': 'chris',
                'matthew': 'matt', 'anthony': 'tony', 'joseph': 'joe',
                'daniel': 'dan', 'andrew': 'andy', 'kenneth': 'ken',
                'elizabeth': 'liz', 'patricia': 'pat', 'jennifer': 'jen',
                'margaret': 'meg', 'catherine': 'kate', 'stephanie': 'steph'
            }
            
            first_name = name_parts[0].lower()
            if first_name in nickname_map:
                variants.append(f"{nickname_map[first_name]} {' '.join(name_parts[1:])}")
            
            # Check reverse (nickname to full name)
            for full, nick in nickname_map.items():
                if first_name == nick:
                    variants.append(f"{full} {' '.join(name_parts[1:])}")
        
        return variants
    
    def _generate_matching_suggestions(self, unmatched: pd.DataFrame) -> List[str]:
        """Generate suggestions for improving matching."""
        suggestions = []
        
        if len(unmatched) > 50:
            suggestions.append("High number of unmatched records suggests data quality issues")
            suggestions.append("Consider reviewing data entry processes for consistency")
        
        # Check for email patterns
        email_domains = unmatched['email_clean'].str.extract(r'@(.+)')[0].value_counts()
        if len(email_domains) > 0:
            top_domain = email_domains.index[0]
            suggestions.append(f"Most common email domain in unmatched: {top_domain}")
            suggestions.append("Consider reaching out to institution IT for email format standards")
        
        # Check name patterns
        short_names = len(unmatched[unmatched['name_clean'].str.len() < 10])
        if short_names > len(unmatched) * 0.3:
            suggestions.append("Many unmatched records have short names - possible incomplete data")
        
        return suggestions
    
    def improved_matching(self, year: int, confidence_threshold: int = 75) -> pd.DataFrame:
        """
        Perform improved matching with relaxed criteria.
        
        Args:
            year (int): Year to analyze
            confidence_threshold (int): Minimum confidence score for matches
            
        Returns:
            DataFrame with improved matching results
        """
        logger.info(f"Running improved matching for {year} with threshold {confidence_threshold}...")
        
        # Get original matching results
        original_results = self.data_processor.match_members(year)
        
        # Work on the unmatched records
        unmatched = original_results[original_results['retention_status'] == 'Unknown'].copy()
        survey_data = self.data_processor.retention_survey
        
        improvements = 0
        
        for idx, person in unmatched.iterrows():
            name = person['name_clean']
            email = person['email_clean']
            
            best_match = None
            best_score = 0
            match_type = None
            
            # Strategy 1: Partial name matching (first + last name only)
            if name and not best_match:
                name_parts = name.split()
                if len(name_parts) >= 2:
                    first_last = f"{name_parts[0]} {name_parts[-1]}"
                    name_matches = process.extract(first_last, survey_data['name_clean'], limit=3)
                    for match_result in name_matches:
                        match_name, score = match_result[0], match_result[1]
                        if score >= confidence_threshold:
                            best_match = match_name
                            best_score = score
                            match_type = 'Partial_Name'
                            break
            
            # Strategy 2: Phonetic matching (sounds like)
            if name and not best_match:
                # Simple phonetic matching - remove vowels for comparison
                name_consonants = re.sub(r'[aeiou]', '', name.lower())
                for survey_name in survey_data['name_clean']:
                    if pd.isna(survey_name):
                        continue
                    survey_consonants = re.sub(r'[aeiou]', '', survey_name.lower())
                    if len(name_consonants) > 3 and len(survey_consonants) > 3:
                        consonant_score = fuzz.ratio(name_consonants, survey_consonants)
                        if consonant_score >= confidence_threshold + 10:  # Higher threshold for phonetic
                            best_match = survey_name
                            best_score = consonant_score
                            match_type = 'Phonetic'
                            break
            
            # Strategy 3: Email username matching
            if email and '@' in email and not best_match:
                username = email.split('@')[0]
                for survey_email in survey_data['email_clean']:
                    if pd.isna(survey_email) or '@' not in survey_email:
                        continue
                    survey_username = survey_email.split('@')[0]
                    username_score = fuzz.ratio(username, survey_username)
                    if username_score >= confidence_threshold:
                        survey_row = survey_data[survey_data['email_clean'] == survey_email].iloc[0]
                        best_match = survey_row['name_clean']
                        best_score = username_score
                        match_type = 'Email_Username'
                        break
            
            # Apply the best match found
            if best_match:
                match_idx = survey_data[survey_data['name_clean'] == best_match].index[0]
                original_results.at[idx, 'retention_status'] = survey_data.at[match_idx, 'Status']
                original_results.at[idx, 'match_type'] = match_type
                original_results.at[idx, 'match_confidence'] = best_score
                improvements += 1
        
        logger.info(f"Improved matching found {improvements} additional matches")
        return original_results
    
    def export_unmatched_for_manual_review(self, year: int, filename: str = None) -> str:
        """
        Export unmatched records to CSV for manual review and LinkedIn research.
        
        Args:
            year (int): Year to export
            filename (str): Optional filename
            
        Returns:
            str: Path to exported file
        """
        if filename is None:
            filename = f"unmatched_members_{year}_for_review.csv"
        
        # Get unmatched records
        matched_data = self.data_processor.match_members(year)
        unmatched = matched_data[matched_data['retention_status'] == 'Unknown'].copy()
        
        # Add helpful columns for manual research
        unmatched['LinkedIn_Search_Name'] = unmatched['Name'].apply(self._format_for_linkedin_search)
        unmatched['LinkedIn_URL'] = ''  # Empty column for manual filling
        unmatched['Manual_Status'] = ''  # Empty column for manual status
        unmatched['Notes'] = ''  # Empty column for notes
        unmatched['Confidence_Level'] = ''  # For manual confidence assessment
        
        # Select and reorder columns for easy review
        export_columns = [
            'Name', 'Email', 'Institution of Study', 'Program of Study', 
            'Country of Origin', 'Date of Enrollment', 'LinkedIn_Search_Name',
            'LinkedIn_URL', 'Manual_Status', 'Notes', 'Confidence_Level'
        ]
        
        export_data = unmatched[export_columns].copy()
        
        # Create output directory
        output_dir = Path("manual_review")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        export_data.to_csv(filepath, index=False)
        
        logger.info(f"Exported {len(export_data)} unmatched records to {filepath}")
        return str(filepath)
    
    def _format_for_linkedin_search(self, name: str) -> str:
        """Format name for LinkedIn search."""
        if pd.isna(name):
            return ""
        
        # Remove common prefixes/suffixes and clean up
        name = re.sub(r'\b(mr\.?|mrs\.?|ms\.?|dr\.?|prof\.?)\b', '', name.lower())
        name = re.sub(r'[^\w\s]', ' ', name)
        name = ' '.join(name.split())  # Remove extra spaces
        
        # Capitalize properly
        return ' '.join(word.capitalize() for word in name.split())
    
    def generate_matching_report(self, year: int) -> Dict[str, any]:
        """Generate comprehensive matching report."""
        logger.info(f"Generating matching report for {year}...")
        
        # Get both original and improved matching results
        original_results = self.data_processor.match_members(year)
        improved_results = self.improved_matching(year)
        
        # Get unmatched analysis
        unmatched_analysis = self.analyze_unmatched_records(year)
        
        # Calculate improvements
        original_matched = len(original_results[original_results['retention_status'] != 'Unknown'])
        improved_matched = len(improved_results[improved_results['retention_status'] != 'Unknown'])
        additional_matches = improved_matched - original_matched
        
        report = {
            'year': year,
            'original_stats': {
                'total_registrations': len(original_results),
                'matched': original_matched,
                'unmatched': len(original_results) - original_matched,
                'match_rate': (original_matched / len(original_results)) * 100
            },
            'improved_stats': {
                'total_registrations': len(improved_results),
                'matched': improved_matched,
                'unmatched': len(improved_results) - improved_matched,
                'match_rate': (improved_matched / len(improved_results)) * 100
            },
            'improvements': {
                'additional_matches': additional_matches,
                'improvement_percentage': (additional_matches / len(original_results)) * 100
            },
            'unmatched_analysis': unmatched_analysis,
            'recommendations': self._generate_recommendations(unmatched_analysis, additional_matches)
        }
        
        return report
    
    def _generate_recommendations(self, unmatched_analysis: Dict, additional_matches: int) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if additional_matches > 0:
            recommendations.append(f"✅ Improved matching found {additional_matches} additional matches")
            recommendations.append("Consider implementing the improved matching algorithm permanently")
        
        remaining_unmatched = unmatched_analysis['total_unmatched'] - additional_matches
        
        if remaining_unmatched > 50:
            recommendations.append("🔍 High number of unmatched records requires manual investigation")
            recommendations.append("Use the exported CSV file for LinkedIn and manual research")
            recommendations.append("Consider contacting institutions for updated member lists")
        
        if remaining_unmatched > 20:
            recommendations.append("📧 Consider sending follow-up emails to unmatched members")
            recommendations.append("Review data collection processes for consistency")
        
        # Institution-specific recommendations
        inst_patterns = unmatched_analysis['patterns']['by_institution']
        if inst_patterns:
            highest_unmatched_inst = max(inst_patterns, key=inst_patterns.get)
            recommendations.append(f"🏫 {highest_unmatched_inst} has the most unmatched records - review their data quality")
        
        return recommendations 