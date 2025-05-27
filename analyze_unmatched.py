#!/usr/bin/env python3
"""
Unmatched Records Analysis Script

This script analyzes and improves matching for WSA retention data,
specifically addressing the issue of unmatched members in 2024.
"""

import sys
import json
import pandas as pd
from pathlib import Path
import logging

# Add src to path so we can import our modules
sys.path.append('src')

from data_processor import DataProcessor
from matching_analyzer import MatchingAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main function to analyze and improve matching."""
    print("🔍 WSA Retention Analysis - Unmatched Records Investigation")
    print("=" * 70)
    
    try:
        # Initialize components
        print("📊 Initializing data processor...")
        processor = DataProcessor()
        
        print("🔬 Initializing matching analyzer...")
        analyzer = MatchingAnalyzer(processor)
        
        # Focus on 2024 as mentioned in the issue
        year = 2024
        print(f"\n🎯 Analyzing unmatched records for {year}...")
        
        # Step 1: Analyze current unmatched records
        print("\n" + "="*50)
        print("STEP 1: ANALYZING UNMATCHED RECORDS")
        print("="*50)
        
        unmatched_analysis = analyzer.analyze_unmatched_records(year)
        
        print(f"\n📈 CURRENT MATCHING STATISTICS FOR {year}:")
        print(f"   Total Registrations: {unmatched_analysis['total_registrations']}")
        print(f"   Unmatched Records: {unmatched_analysis['total_unmatched']}")
        print(f"   Unmatched Percentage: {unmatched_analysis['unmatched_percentage']:.1f}%")
        
        # Show patterns in unmatched data
        patterns = unmatched_analysis['patterns']
        
        print(f"\n🏫 UNMATCHED BY INSTITUTION:")
        for inst, count in patterns['by_institution'].items():
            print(f"   {inst}: {count} unmatched")
        
        print(f"\n🌍 UNMATCHED BY COUNTRY:")
        for country, count in list(patterns['by_country'].items())[:5]:
            print(f"   {country}: {count} unmatched")
        
        print(f"\n📧 UNMATCHED BY EMAIL DOMAIN:")
        for domain, count in list(patterns['by_email_domain'].items())[:5]:
            print(f"   {domain}: {count} unmatched")
        
        # Step 2: Run improved matching
        print("\n" + "="*50)
        print("STEP 2: RUNNING IMPROVED MATCHING ALGORITHM")
        print("="*50)
        
        print("🔄 Running improved matching with multiple strategies...")
        improved_results = analyzer.improved_matching(year, confidence_threshold=75)
        
        # Step 3: Generate comprehensive report
        print("\n" + "="*50)
        print("STEP 3: GENERATING MATCHING REPORT")
        print("="*50)
        
        report = analyzer.generate_matching_report(year)
        
        print(f"\n📊 MATCHING IMPROVEMENT RESULTS:")
        print(f"   Original Match Rate: {report['original_stats']['match_rate']:.1f}%")
        print(f"   Improved Match Rate: {report['improved_stats']['match_rate']:.1f}%")
        print(f"   Additional Matches Found: {report['improvements']['additional_matches']}")
        print(f"   Improvement: +{report['improvements']['improvement_percentage']:.1f}%")
        
        remaining_unmatched = report['improved_stats']['unmatched']
        print(f"   Remaining Unmatched: {remaining_unmatched}")
        
        # Step 4: Export unmatched for manual review
        print("\n" + "="*50)
        print("STEP 4: EXPORTING UNMATCHED RECORDS FOR MANUAL REVIEW")
        print("="*50)
        
        if remaining_unmatched > 0:
            export_path = analyzer.export_unmatched_for_manual_review(year)
            print(f"✅ Exported {remaining_unmatched} unmatched records to: {export_path}")
            print(f"📝 This file includes LinkedIn-ready names and columns for manual status updates")
            print(f"🔍 Use this file to research members on LinkedIn and social media")
        else:
            print("🎉 All records have been matched! No manual review needed.")
        
        # Step 5: Save detailed analysis report
        print("\n" + "="*50)
        print("STEP 5: SAVING DETAILED ANALYSIS REPORT")
        print("="*50)
        
        # Create reports directory
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        # Save matching report
        report_path = reports_dir / f"matching_analysis_{year}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"💾 Detailed report saved to: {report_path}")
        
        # Step 6: Show recommendations
        print("\n" + "="*50)
        print("STEP 6: RECOMMENDATIONS")
        print("="*50)
        
        print("\n🎯 RECOMMENDED ACTIONS:")
        for i, recommendation in enumerate(report['recommendations'], 1):
            print(f"   {i}. {recommendation}")
        
        # Step 7: Show potential matches for manual review
        if unmatched_analysis['potential_matches']:
            print(f"\n🔍 POTENTIAL MATCHES FOUND (Top 10):")
            for i, match in enumerate(unmatched_analysis['potential_matches'][:10], 1):
                print(f"\n   {i}. Registration: {match['registration_name']}")
                print(f"      Email: {match['registration_email']}")
                print(f"      Potential Matches:")
                for potential in match['potential_matches'][:2]:  # Show top 2
                    print(f"        - {potential['matched_name']} ({potential['type']}, {potential['score']}% confidence)")
                    print(f"          Status: {potential['status']}")
        
        print(f"\n" + "="*70)
        print("ANALYSIS COMPLETE!")
        print("="*70)
        print(f"📋 SUMMARY:")
        print(f"   • Original unmatched: {report['original_stats']['unmatched']}")
        print(f"   • Improved matching found: {report['improvements']['additional_matches']} additional matches")
        print(f"   • Still need manual review: {remaining_unmatched}")
        print(f"   • Export file created for LinkedIn research")
        print(f"   • Detailed report saved to {report_path}")
        
        if remaining_unmatched > 0:
            print(f"\n📝 NEXT STEPS:")
            print(f"   1. Open the exported CSV file: {export_path}")
            print(f"   2. Research unmatched members on LinkedIn using the 'LinkedIn_Search_Name' column")
            print(f"   3. Fill in the 'LinkedIn_URL', 'Manual_Status', and 'Notes' columns")
            print(f"   4. Run this script again after updating the retention survey with new findings")
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        print(f"❌ Error: {e}")
        return 1
    
    return 0


def analyze_year_comparison():
    """Compare matching quality between 2023 and 2024."""
    print("\n🔬 COMPARING MATCHING QUALITY: 2023 vs 2024")
    print("="*50)
    
    try:
        processor = DataProcessor()
        analyzer = MatchingAnalyzer(processor)
        
        # Analyze both years
        for year in [2023, 2024]:
            print(f"\n📊 {year} Analysis:")
            analysis = analyzer.analyze_unmatched_records(year)
            print(f"   Total: {analysis['total_registrations']}")
            print(f"   Unmatched: {analysis['total_unmatched']} ({analysis['unmatched_percentage']:.1f}%)")
            
            # Try improved matching
            improved = analyzer.improved_matching(year)
            original_matched = analysis['total_registrations'] - analysis['total_unmatched']
            improved_matched = len(improved[improved['retention_status'] != 'Unknown'])
            additional = improved_matched - original_matched
            
            print(f"   Improved: +{additional} additional matches")
            print(f"   Final unmatched: {analysis['total_registrations'] - improved_matched}")
    
    except Exception as e:
        print(f"Error in comparison: {e}")


if __name__ == "__main__":
    exit_code = main()
    
    # Optionally run year comparison
    if len(sys.argv) > 1 and sys.argv[1] == "--compare":
        analyze_year_comparison()
    
    sys.exit(exit_code) 