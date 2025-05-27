#!/usr/bin/env python3
"""
Demo Script for WSA Retention Analysis

This script demonstrates the retention analysis functionality using
SAMPLE DATA ONLY - no real personal information is used.

This is safe to run and demonstrates all features of the system.
"""

import sys
import json
from pathlib import Path

# Add src to path so we can import our modules
sys.path.append('src')

from retention_analyzer import RetentionAnalyzer


def setup_demo_environment():
    """
    Set up the demo environment with sample data.
    """
    print("Setting up demo environment with sample data...")
    
    # Create necessary directories
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    # Copy sample files to the expected locations for demo
    import shutil
    
    sample_files = [
        ("data/sample/sample_retention_survey.csv", "data/raw/Are they still in PEI? - Members Summary.csv"),
        ("data/sample/sample_registrations_2023.csv", "data/raw/Website Memberships-Backend-2023.csv"),
        ("data/sample/sample_registrations_2024.csv", "data/raw/Website Memberships-Backend-2024.csv")
    ]
    
    for source, dest in sample_files:
        if Path(source).exists():
            shutil.copy2(source, dest)
            print(f"✅ Copied {source} → {dest}")
        else:
            print(f"❌ Sample file not found: {source}")
    
    print("Demo environment ready!\n")


def cleanup_demo_environment():
    """
    Clean up demo files after the demonstration.
    """
    print("\nCleaning up demo environment...")
    
    demo_files = [
        "data/raw/Are they still in PEI? - Members Summary.csv",
        "data/raw/Website Memberships-Backend-2023.csv", 
        "data/raw/Website Memberships-Backend-2024.csv"
    ]
    
    for file_path in demo_files:
        try:
            Path(file_path).unlink()
            print(f"🗑️ Removed {file_path}")
        except FileNotFoundError:
            pass
    
    print("Demo cleanup complete!")


def main():
    """
    Run the complete WSA retention analysis demo with sample data.
    """
    print("🚀 WSA Retention Analysis - DEMO MODE")
    print("=" * 60)
    print("⚠️  This demo uses FICTIONAL DATA ONLY")
    print("⚠️  No real personal information is processed")
    print("=" * 60)
    
    try:
        # Set up demo environment
        setup_demo_environment()
        
        # Initialize the analyzer
        analyzer = RetentionAnalyzer()
        
        # Run analysis for 2023
        print("\n📊 Analyzing 2023 sample data...")
        results_2023 = analyzer.analyze_retention(year=2023)
        analyzer.print_summary(results_2023, year=2023)
        
        # Save 2023 results
        file_2023 = analyzer.save_results(results_2023, "demo_retention_analysis_2023.json")
        print(f"\n💾 2023 Demo Results saved to: {file_2023}")
        
        # Run analysis for 2024
        print("\n📊 Analyzing 2024 sample data...")
        results_2024 = analyzer.analyze_retention(year=2024)
        analyzer.print_summary(results_2024, year=2024)
        
        # Save 2024 results
        file_2024 = analyzer.save_results(results_2024, "demo_retention_analysis_2024.json")
        print(f"\n💾 2024 Demo Results saved to: {file_2024}")
        
        # Compare years
        print("\n📈 Generating comparison between 2023 and 2024...")
        comparison = analyzer.compare_years(results_2023, results_2024)
        
        # Save comparison
        comparison_file = Path("reports") / "demo_year_comparison.json"
        with open(comparison_file, 'w') as f:
            json.dump(comparison, f, indent=2, default=str)
        
        print(f"📊 Comparison saved to: {comparison_file}")
        
        # Print key insights
        print("\n" + "=" * 60)
        print("🔍 KEY DEMO INSIGHTS")
        print("=" * 60)
        
        print(f"\n2023 vs 2024 Demo Summary:")
        print(f"  Total Members Change: {comparison['summary_comparison']['changes']['total_members_change']:+d}")
        print(f"  Retention Rate Change: {comparison['summary_comparison']['changes']['retention_rate_change']:+.1f}%")
        print(f"  Match Rate Change: {comparison['summary_comparison']['changes']['match_rate_change']:+.1f}%")
        
        # Top retention rates by institution
        print(f"\nHighest Retention Rates (2024 Demo Data):")
        inst_data = results_2024['institution_breakdown']
        sorted_institutions = sorted(inst_data.items(), key=lambda x: x[1]['retention_rate'], reverse=True)
        
        for i, (institution, data) in enumerate(sorted_institutions):
            print(f"  {i+1}. {institution}: {data['retention_rate']:.1f}% ({data['still_in_pei']}/{data['matched_members']})")
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("🎯 This demonstrates all system functionality")
        print("🔒 Your real data remains protected")
        print("📁 Check the 'reports' directory for demo JSON files")
        print("📖 Read DATA_SECURITY.md for data protection guidelines")
        
        # Clean up demo files
        cleanup_demo_environment()
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        cleanup_demo_environment()
        sys.exit(1)


if __name__ == "__main__":
    main() 