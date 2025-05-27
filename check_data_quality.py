#!/usr/bin/env python3
"""
Data Quality Checker for WSA Retention Analysis

This script checks for common data quality issues that can cause
poor matching rates between registration and retention survey data.
"""

import sys
import pandas as pd
import re
from pathlib import Path
from collections import Counter

# Add src to path
sys.path.append('src')
from data_processor import DataProcessor


def check_name_quality(df, name_col):
    """Check quality of name data."""
    issues = []
    
    # Missing names
    missing = df[name_col].isna().sum()
    if missing > 0:
        issues.append(f"Missing names: {missing}")
    
    # Very short names (likely incomplete)
    short_names = df[df[name_col].str.len() < 3].shape[0]
    if short_names > 0:
        issues.append(f"Very short names (< 3 chars): {short_names}")
    
    # Names with numbers (potential data entry errors)
    names_with_numbers = df[df[name_col].str.contains(r'\d', na=False)].shape[0]
    if names_with_numbers > 0:
        issues.append(f"Names containing numbers: {names_with_numbers}")
    
    # Names with excessive special characters
    names_with_special = df[df[name_col].str.contains(r'[^\w\s\-\.]', na=False)].shape[0]
    if names_with_special > 0:
        issues.append(f"Names with special characters: {names_with_special}")
    
    # Duplicate names (potential data entry issues)
    duplicates = df[name_col].duplicated().sum()
    if duplicates > 0:
        issues.append(f"Duplicate names: {duplicates}")
    
    return issues


def check_email_quality(df, email_col):
    """Check quality of email data."""
    issues = []
    
    # Missing emails
    missing = df[email_col].isna().sum()
    if missing > 0:
        issues.append(f"Missing emails: {missing}")
    
    # Invalid email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    invalid_emails = df[~df[email_col].str.match(email_pattern, na=False)].shape[0]
    if invalid_emails > 0:
        issues.append(f"Invalid email format: {invalid_emails}")
    
    # Duplicate emails
    duplicates = df[email_col].duplicated().sum()
    if duplicates > 0:
        issues.append(f"Duplicate emails: {duplicates}")
    
    # Analyze email domains
    domains = df[email_col].str.extract(r'@(.+)')[0].value_counts()
    
    return issues, domains


def check_institution_consistency(df, inst_col):
    """Check institution name consistency."""
    institutions = df[inst_col].value_counts()
    
    # Look for potential duplicates with slight variations
    inst_names = institutions.index.tolist()
    potential_duplicates = []
    
    for i, name1 in enumerate(inst_names):
        for name2 in inst_names[i+1:]:
            if name1.lower().replace(' ', '') == name2.lower().replace(' ', ''):
                potential_duplicates.append((name1, name2))
    
    return institutions, potential_duplicates


def main():
    """Main data quality check function."""
    print("🔍 WSA Retention Analysis - Data Quality Check")
    print("=" * 60)
    
    try:
        processor = DataProcessor()
        
        # Load data
        print("📊 Loading data files...")
        data = processor.load_data()
        
        print(f"✅ Loaded retention survey: {len(data['retention_survey'])} records")
        print(f"✅ Loaded 2023 registrations: {len(data['registrations_2023'])} records")
        print(f"✅ Loaded 2024 registrations: {len(data['registrations_2024'])} records")
        
        print("\n" + "="*60)
        print("RETENTION SURVEY QUALITY CHECK")
        print("="*60)
        
        # Check retention survey
        retention_df = data['retention_survey']
        
        print("\n📧 Email Quality:")
        email_issues, email_domains = check_email_quality(retention_df, 'Email Address')
        if email_issues:
            for issue in email_issues:
                print(f"   ⚠️  {issue}")
        else:
            print("   ✅ No email issues found")
        
        print(f"\n📧 Email Domains (Top 5):")
        for domain, count in email_domains.head().items():
            print(f"   {domain}: {count} emails")
        
        print("\n👤 Name Quality:")
        name_issues = check_name_quality(retention_df, 'Name')
        if name_issues:
            for issue in name_issues:
                print(f"   ⚠️  {issue}")
        else:
            print("   ✅ No name issues found")
        
        # Check retention status distribution
        print(f"\n📊 Status Distribution:")
        status_counts = retention_df['Status'].value_counts()
        for status, count in status_counts.items():
            print(f"   {status}: {count}")
        
        # Check for each registration year
        for year in [2023, 2024]:
            reg_df = data[f'registrations_{year}']
            
            print(f"\n" + "="*60)
            print(f"{year} REGISTRATIONS QUALITY CHECK")
            print("="*60)
            
            print("\n📧 Email Quality:")
            email_issues, email_domains = check_email_quality(reg_df, 'Email')
            if email_issues:
                for issue in email_issues:
                    print(f"   ⚠️  {issue}")
            else:
                print("   ✅ No email issues found")
            
            print(f"\n📧 Email Domains (Top 5):")
            for domain, count in email_domains.head().items():
                print(f"   {domain}: {count} emails")
            
            print("\n👤 Name Quality:")
            name_issues = check_name_quality(reg_df, 'Name')
            if name_issues:
                for issue in name_issues:
                    print(f"   ⚠️  {issue}")
            else:
                print("   ✅ No name issues found")
            
            print(f"\n🏫 Institution Analysis:")
            institutions, potential_dups = check_institution_consistency(reg_df, 'Institution of Study')
            
            print(f"   Total institutions: {len(institutions)}")
            for inst, count in institutions.items():
                print(f"   {inst}: {count} students")
            
            if potential_dups:
                print(f"\n   ⚠️  Potential duplicate institutions:")
                for dup1, dup2 in potential_dups:
                    print(f"      '{dup1}' vs '{dup2}'")
            
            # Check province distribution and non-PEI students
            print(f"\n📍 Province/Location Analysis:")
            if 'Province' in reg_df.columns:
                province_counts = reg_df['Province'].value_counts(dropna=False)
                print(f"   Province Distribution:")
                for province, count in province_counts.items():
                    if pd.isna(province):
                        print(f"      Missing/Unknown: {count}")
                    else:
                        print(f"      {province}: {count}")
                
                # Highlight non-PEI students
                pei_variations = [
                    'Prince Edward Island', 'Prince-Edward-Island', 'PEI', 
                    'P.E.I.', 'Prince Edward Island, Canada', 'PE'
                ]
                non_pei_mask = ~reg_df['Province'].str.lower().str.strip().isin([var.lower() for var in pei_variations])
                non_pei = reg_df[non_pei_mask]
                
                if len(non_pei) > 0:
                    print(f"\n   🚨 NON-PEI STUDENTS FOUND: {len(non_pei)} students")
                    print(f"      These will be automatically filtered out:")
                    for province, count in non_pei['Province'].value_counts().items():
                        print(f"         - {province}: {count} students")
                    
                    # Show some examples if not too many
                    if len(non_pei) <= 10:
                        print(f"      Example names:")
                        for _, row in non_pei.head(5).iterrows():
                            print(f"         - {row.get('Name', 'N/A')} ({row.get('Province', 'N/A')})")
                else:
                    print(f"   ✅ All students are from PEI")
            else:
                print(f"   ℹ️  No Province column found - filtering by institution only")
        
        # Cross-dataset analysis
        print(f"\n" + "="*60)
        print("CROSS-DATASET QUALITY CHECK")
        print("="*60)
        
        # Email domain comparison
        print("\n📧 Email Domain Comparison:")
        retention_domains = set(retention_df['Email Address'].str.extract(r'@(.+)')[0].dropna())
        reg_2023_domains = set(data['registrations_2023']['Email'].str.extract(r'@(.+)')[0].dropna())
        reg_2024_domains = set(data['registrations_2024']['Email'].str.extract(r'@(.+)')[0].dropna())
        
        common_domains = retention_domains & reg_2023_domains & reg_2024_domains
        print(f"   Common domains across all files: {len(common_domains)}")
        
        unique_retention = retention_domains - reg_2023_domains - reg_2024_domains
        if unique_retention:
            print(f"   Domains only in retention survey: {len(unique_retention)}")
            print(f"   Examples: {list(unique_retention)[:3]}")
        
        # Name format comparison
        print(f"\n👤 Name Format Analysis:")
        
        def analyze_name_format(df, name_col, label):
            avg_length = df[name_col].str.len().mean()
            avg_words = df[name_col].str.split().str.len().mean()
            print(f"   {label}:")
            print(f"      Average name length: {avg_length:.1f} characters")
            print(f"      Average words per name: {avg_words:.1f}")
        
        analyze_name_format(retention_df, 'Name', 'Retention Survey')
        analyze_name_format(data['registrations_2023'], 'Name', '2023 Registrations')
        analyze_name_format(data['registrations_2024'], 'Name', '2024 Registrations')
        
        print(f"\n" + "="*60)
        print("RECOMMENDATIONS")
        print("="*60)
        
        print(f"\n🎯 Based on the analysis above:")
        print(f"   1. Review any data quality issues identified")
        print(f"   2. Standardize institution names if duplicates found")
        print(f"   3. Check email format consistency")
        print(f"   4. Consider name standardization before matching")
        print(f"   5. Note: Non-PEI students are automatically filtered out")
        print(f"   6. Run improved matching algorithm: python3 analyze_unmatched.py")
        
    except FileNotFoundError as e:
        print(f"❌ Data file not found: {e}")
        print(f"📁 Please ensure your CSV files are in data/raw/ directory")
        return 1
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 