"""
Data Processing Module for WSA Retention Analysis

This module handles loading, cleaning, and preprocessing the CSV files
for the retention analysis.
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import logging
from fuzzywuzzy import fuzz, process

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Class to handle data loading, cleaning, and preprocessing for retention analysis.
    """
    
    def __init__(self, data_dir: str = "data/raw"):
        """
        Initialize the DataProcessor.
        
        Args:
            data_dir (str): Directory containing the raw CSV files
        """
        self.data_dir = Path(data_dir)
        self.retention_survey = None
        self.registrations_2023 = None
        self.registrations_2024 = None
        
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all CSV files into DataFrames.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing all loaded datasets
        """
        logger.info("Loading data files...")
        
        try:
            # Load retention survey data
            retention_file = self.data_dir / "Are they still in PEI? - Members Summary.csv"
            self.retention_survey = pd.read_csv(retention_file)
            logger.info(f"Loaded retention survey: {len(self.retention_survey)} records")
            
            # Load 2023 registrations
            reg_2023_file = self.data_dir / "Website Memberships-Backend-2023.csv"
            self.registrations_2023 = pd.read_csv(reg_2023_file)
            logger.info(f"Loaded 2023 registrations: {len(self.registrations_2023)} records")
            
            # Load 2024 registrations
            reg_2024_file = self.data_dir / "Website Memberships-Backend-2024.csv"
            self.registrations_2024 = pd.read_csv(reg_2024_file)
            logger.info(f"Loaded 2024 registrations: {len(self.registrations_2024)} records")
            
            return {
                'retention_survey': self.retention_survey,
                'registrations_2023': self.registrations_2023,
                'registrations_2024': self.registrations_2024
            }
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def clean_names(self, name: str) -> str:
        """
        Clean and standardize names for better matching.
        
        Args:
            name (str): Raw name string
            
        Returns:
            str: Cleaned name
        """
        if pd.isna(name) or name == "":
            return ""
        
        # Convert to string and lower case
        name = str(name).lower().strip()
        
        # Remove extra spaces
        name = re.sub(r'\s+', ' ', name)
        
        # Remove common suffixes/prefixes
        name = re.sub(r'\b(mr\.?|mrs\.?|ms\.?|dr\.?)\b', '', name)
        
        # Remove special characters but keep spaces and hyphens
        name = re.sub(r'[^\w\s\-]', '', name)
        
        return name.strip()
    
    def clean_emails(self, email: str) -> str:
        """
        Clean and standardize email addresses.
        
        Args:
            email (str): Raw email string
            
        Returns:
            str: Cleaned email
        """
        if pd.isna(email) or email == "":
            return ""
        
        email = str(email).lower().strip()
        
        # Handle multiple emails separated by commas, semicolons, or spaces
        emails = re.split(r'[,;\s]+', email)
        
        # Return the first valid email
        for e in emails:
            e = e.strip()
            if '@' in e and '.' in e.split('@')[-1]:
                return e
        
        return email
    
    def filter_pei_students(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter registrations to include only students from PEI institutions/province.
        
        Args:
            df (pd.DataFrame): Registration DataFrame
            
        Returns:
            pd.DataFrame: Filtered DataFrame with only PEI students
        """
        if df is None or df.empty:
            return df
        
        # Check if Province column exists
        if 'Province' in df.columns:
            # Filter for Prince Edward Island variations
            pei_variations = [
                'Prince Edward Island',
                'Prince-Edward-Island', 
                'PEI',
                'P.E.I.',
                'Prince Edward Island, Canada',
                'PE'
            ]
            
            # Create case-insensitive filter
            pei_mask = df['Province'].str.lower().str.strip().isin([var.lower() for var in pei_variations])
            original_count = len(df)
            df_filtered = df[pei_mask].copy()
            filtered_count = len(df_filtered)
            
            logger.info(f"Province filtering: {original_count} -> {filtered_count} records (removed {original_count - filtered_count} non-PEI students)")
            return df_filtered
        
        # If no Province column, check Institution of Study for PEI institutions
        elif 'Institution of Study' in df.columns:
            pei_institutions = [
                'UPEI',
                'University of Prince Edward Island',
                'Holland College',
                'Collège de l\'Île',
                'College de l\'Ile',
                'Maritime Christian College',
                'PEI Paramedic Academy'
            ]
            
            # Create case-insensitive filter
            institution_mask = df['Institution of Study'].str.lower().str.strip().isin([inst.lower() for inst in pei_institutions])
            original_count = len(df)
            df_filtered = df[institution_mask].copy()
            filtered_count = len(df_filtered)
            
            logger.info(f"Institution filtering: {original_count} -> {filtered_count} records (removed {original_count - filtered_count} non-PEI institution students)")
            return df_filtered
        
        else:
            logger.warning("No Province or Institution of Study column found - cannot filter for PEI students")
            return df

    def preprocess_data(self) -> Dict[str, pd.DataFrame]:
        """
        Clean and preprocess all datasets.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing cleaned datasets
        """
        logger.info("Preprocessing data...")
        
        if self.retention_survey is None:
            self.load_data()
        
        # Filter for PEI students only
        logger.info("Filtering for PEI students only...")
        self.registrations_2023 = self.filter_pei_students(self.registrations_2023)
        self.registrations_2024 = self.filter_pei_students(self.registrations_2024)
        
        # Clean retention survey data
        self.retention_survey['name_clean'] = self.retention_survey['Name'].apply(self.clean_names)
        self.retention_survey['email_clean'] = self.retention_survey['Email Address'].apply(self.clean_emails)
        
        # Clean 2023 registrations
        if self.registrations_2023 is not None and not self.registrations_2023.empty:
            self.registrations_2023['name_clean'] = self.registrations_2023['Name'].apply(self.clean_names)
            self.registrations_2023['email_clean'] = self.registrations_2023['Email'].apply(self.clean_emails)
            self.registrations_2023['enrollment_date'] = pd.to_datetime(self.registrations_2023['Date of Enrollment'], errors='coerce')
        
        # Clean 2024 registrations
        if self.registrations_2024 is not None and not self.registrations_2024.empty:
            self.registrations_2024['name_clean'] = self.registrations_2024['Name'].apply(self.clean_names)
            self.registrations_2024['email_clean'] = self.registrations_2024['Email'].apply(self.clean_emails)
            self.registrations_2024['enrollment_date'] = pd.to_datetime(self.registrations_2024['Date of Enrollment'], errors='coerce')
        
        logger.info("Data preprocessing completed")
        
        return {
            'retention_survey': self.retention_survey,
            'registrations_2023': self.registrations_2023,
            'registrations_2024': self.registrations_2024
        }
    
    def find_name_matches(self, name: str, candidate_names: List[str], threshold: int = 80) -> List[Tuple[str, int]]:
        """
        Find fuzzy matches for a name in a list of candidate names.
        
        Args:
            name (str): Name to match
            candidate_names (List[str]): List of candidate names
            threshold (int): Minimum similarity score
            
        Returns:
            List[Tuple[str, int]]: List of (name, score) tuples above threshold
        """
        if not name or not candidate_names:
            return []
        
        matches = process.extract(name, candidate_names, limit=5)
        return [(match[0], match[1]) for match in matches if match[1] >= threshold]
    
    def match_members(self, year: int) -> pd.DataFrame:
        """
        Match members between registration data and retention survey.
        
        Args:
            year (int): Year to analyze (2023 or 2024)
            
        Returns:
            pd.DataFrame: Matched data with retention status
        """
        logger.info(f"Matching members for year {year}...")
        
        if year == 2023:
            registrations = self.registrations_2023
        elif year == 2024:
            registrations = self.registrations_2024
        else:
            raise ValueError("Year must be 2023 or 2024")
        
        # Create results DataFrame
        results = registrations.copy()
        results['retention_status'] = 'Unknown'
        results['match_type'] = 'None'
        results['match_confidence'] = 0
        
        # Create lookup dictionaries for fast matching
        survey_name_lookup = dict(zip(self.retention_survey['name_clean'], self.retention_survey['Status']))
        survey_email_lookup = dict(zip(self.retention_survey['email_clean'], self.retention_survey['Status']))
        
        for idx, row in results.iterrows():
            name_clean = row['name_clean']
            email_clean = row['email_clean']
            
            # Try exact email match first
            if email_clean and email_clean in survey_email_lookup:
                results.at[idx, 'retention_status'] = survey_email_lookup[email_clean]
                results.at[idx, 'match_type'] = 'Email'
                results.at[idx, 'match_confidence'] = 100
                continue
            
            # Try exact name match
            if name_clean and name_clean in survey_name_lookup:
                results.at[idx, 'retention_status'] = survey_name_lookup[name_clean]
                results.at[idx, 'match_type'] = 'Name_Exact'
                results.at[idx, 'match_confidence'] = 100
                continue
            
            # Try fuzzy name matching
            if name_clean:
                name_matches = self.find_name_matches(name_clean, list(self.retention_survey['name_clean']))
                if name_matches:
                    best_match, confidence = name_matches[0]
                    if confidence >= 85:  # High confidence threshold
                        match_idx = self.retention_survey[self.retention_survey['name_clean'] == best_match].index[0]
                        results.at[idx, 'retention_status'] = self.retention_survey.at[match_idx, 'Status']
                        results.at[idx, 'match_type'] = 'Name_Fuzzy'
                        results.at[idx, 'match_confidence'] = confidence
        
        logger.info(f"Matching completed for {year}. Found {len(results[results['retention_status'] != 'Unknown'])} matches.")
        
        return results
    
    def get_data_summary(self) -> Dict[str, Dict]:
        """
        Get summary statistics for all datasets.
        
        Returns:
            Dict[str, Dict]: Summary statistics for each dataset
        """
        summaries = {}
        
        if self.retention_survey is not None:
            summaries['retention_survey'] = {
                'total_records': len(self.retention_survey),
                'status_counts': self.retention_survey['Status'].value_counts().to_dict(),
                'missing_names': self.retention_survey['Name'].isna().sum(),
                'missing_emails': self.retention_survey['Email Address'].isna().sum()
            }
        
        if self.registrations_2023 is not None:
            summaries['registrations_2023'] = {
                'total_records': len(self.registrations_2023),
                'institutions': self.registrations_2023['Institution of Study'].value_counts().to_dict(),
                'missing_names': self.registrations_2023['Name'].isna().sum(),
                'missing_emails': self.registrations_2023['Email'].isna().sum()
            }
        
        if self.registrations_2024 is not None:
            summaries['registrations_2024'] = {
                'total_records': len(self.registrations_2024),
                'institutions': self.registrations_2024['Institution of Study'].value_counts().to_dict(),
                'missing_names': self.registrations_2024['Name'].isna().sum(),
                'missing_emails': self.registrations_2024['Email'].isna().sum()
            }
        
        return summaries 