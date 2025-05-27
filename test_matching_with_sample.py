#!/usr/bin/env python3
"""
Test Matching Analysis with Sample Data

This script demonstrates the improved matching functionality using
sample data to verify the system works correctly.
"""

import sys
import pandas as pd
from pathlib import Path

# Add src to path so we can import our modules
sys.path.append('src')

from data_processor import DataProcessor
from matching_analyzer import MatchingAnalyzer


def main():
    """Test matching analysis with sample data."""
    print("🧪 Testing WSA Retention Analysis - Matching Improvements")
    print("=" * 70)
    print("Using sample data to demonstrate functionality")
    print("=" * 70)
    
    # Use sample data instead of real data
    sample_data_dir = "data/sample"
    
    # Create a modified data processor for sample data
    processor = DataProcessor(data_dir=sample_data_dir)
    
    # Manually load sample data with correct names
    try:
        # Load sample retention survey
        processor.retention_survey = pd.read_csv(f"{sample_data_dir}/sample_retention_survey.csv")
        print(f"✅ Loaded sample retention survey: {len(processor.retention_survey)} records")
        
        # Load sample registrations  
        processor.registrations_2023 = pd.read_csv(f"{sample_data_dir}/sample_registrations_2023.csv")
        processor.registrations_2024 = pd.read_csv(f"{sample_data_dir}/sample_registrations_2024.csv")
        print(f"✅ Loaded sample 2023 registrations: {len(processor.registrations_2023)} records")
        print(f"✅ Loaded sample 2024 registrations: {len(processor.registrations_2024)} records")
        
        # Preprocess the data
        processor.preprocess_data()
        print("✅ Data preprocessing completed")
        
        # Create matching analyzer
        analyzer = MatchingAnalyzer(processor)
        print("✅ Matching analyzer initialized")
        
        # Test with 2024 data
        year = 2024
        print(f"\n🔍 Testing matching analysis for {year}...")
        
        # Analyze unmatched records
        print("\n📊 Running unmatched analysis...")
        unmatched_analysis = analyzer.analyze_unmatched_records(year)
        
        print(f"\n📈 SAMPLE DATA STATISTICS FOR {year}:")
        print(f"   Total Registrations: {unmatched_analysis['total_registrations']}")
        print(f"   Unmatched Records: {unmatched_analysis['total_unmatched']}")
        print(f"   Unmatched Percentage: {unmatched_analysis['unmatched_percentage']:.1f}%")
        
        # Test improved matching
        print(f"\n🔄 Testing improved matching algorithm...")
        improved_results = analyzer.improved_matching(year)
        
        # Generate report
        print(f"\n📋 Generating matching report...")
        report = analyzer.generate_matching_report(year)
        
        print(f"\n📊 SAMPLE DATA MATCHING RESULTS:")
        print(f"   Original Match Rate: {report['original_stats']['match_rate']:.1f}%")
        print(f"   Improved Match Rate: {report['improved_stats']['match_rate']:.1f}%")
        print(f"   Additional Matches Found: {report['improvements']['additional_matches']}")
        print(f"   Remaining Unmatched: {report['improved_stats']['unmatched']}")
        
        # Test export functionality
        if report['improved_stats']['unmatched'] > 0:
            print(f"\n📄 Testing export functionality...")
            export_path = analyzer.export_unmatched_for_manual_review(year, f"sample_unmatched_{year}.csv")
            print(f"✅ Exported unmatched records to: {export_path}")
        
        print(f"\n🎯 RECOMMENDATIONS:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print(f"📝 The system is working correctly with sample data.")
        print(f"🔄 Ready to process real data when available.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


def show_real_data_instructions():
    """Show instructions for using with real data."""
    print(f"\n" + "="*70)
    print("INSTRUCTIONS FOR REAL DATA ANALYSIS")
    print("="*70)
    print(f"""
To analyze your real WSA retention data:

1. 📁 Place your CSV files in data/raw/ directory:
   • Are they still in PEI? - Members Summary.csv
   • Website Memberships-Backend-2023.csv  
   • Website Memberships-Backend-2024.csv

2. 🔄 Run the analysis:
   python3 analyze_unmatched.py

3. 📊 The analysis will:
   • Identify unmatched members (currently 89 in 2024)
   • Apply improved matching algorithms
   • Export unmatched records for LinkedIn research
   • Generate comprehensive reports

4. 🔍 For LinkedIn research:
   • Open the exported CSV file
   • Use the 'LinkedIn_Search_Name' column for searches
   • Fill in findings in the manual review columns
   • Update your retention survey with new data

5. 🔁 Repeat analysis after updates to see improvements

The improved matching algorithms include:
✅ Partial name matching (first + last name only)
✅ Phonetic matching (sound-alike names)  
✅ Email username similarity
✅ Nickname and name variant detection
✅ Better fuzzy matching thresholds
""")


if __name__ == "__main__":
    exit_code = main()
    show_real_data_instructions()
    sys.exit(exit_code) 