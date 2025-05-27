#!/usr/bin/env python3
"""
Main script to run the WSA Retention Analysis

This script performs the complete retention analysis for both 2023 and 2024,
generates reports, and saves the results.
"""

import sys
import json
from pathlib import Path

# Add src to path so we can import our modules
sys.path.append('src')

from retention_analyzer import RetentionAnalyzer


def main():
    """
    Run the complete WSA retention analysis.
    """
    print("WSA Retention Analysis - Starting...")
    print("=" * 60)
    
    try:
        # Initialize the analyzer
        analyzer = RetentionAnalyzer()
        
        # Run analysis for 2023
        print("\nAnalyzing 2023 data...")
        results_2023 = analyzer.analyze_retention(year=2023)
        analyzer.print_summary(results_2023, year=2023)
        
        # Save 2023 results
        file_2023 = analyzer.save_results(results_2023, "retention_analysis_2023.json")
        print(f"\n2023 Results saved to: {file_2023}")
        
        # Run analysis for 2024
        print("\nAnalyzing 2024 data...")
        results_2024 = analyzer.analyze_retention(year=2024)
        analyzer.print_summary(results_2024, year=2024)
        
        # Save 2024 results
        file_2024 = analyzer.save_results(results_2024, "retention_analysis_2024.json")
        print(f"\n2024 Results saved to: {file_2024}")
        
        # Compare years
        print("\nGenerating comparison between 2023 and 2024...")
        comparison = analyzer.compare_years(results_2023, results_2024)
        
        # Save comparison
        comparison_file = Path("reports") / "year_comparison.json"
        with open(comparison_file, 'w') as f:
            json.dump(comparison, f, indent=2, default=str)
        
        print(f"Comparison saved to: {comparison_file}")
        
        # Print key insights
        print("\n" + "=" * 60)
        print("KEY INSIGHTS")
        print("=" * 60)
        
        print(f"\n2023 vs 2024 Summary:")
        print(f"  Total Members Change: {comparison['summary_comparison']['changes']['total_members_change']:+d}")
        print(f"  Retention Rate Change: {comparison['summary_comparison']['changes']['retention_rate_change']:+.1f}%")
        print(f"  Match Rate Change: {comparison['summary_comparison']['changes']['match_rate_change']:+.1f}%")
        
        # Top retention rates by institution
        print(f"\nHighest Retention Rates (2024):")
        inst_data = results_2024['institution_breakdown']
        sorted_institutions = sorted(inst_data.items(), key=lambda x: x[1]['retention_rate'], reverse=True)
        
        for i, (institution, data) in enumerate(sorted_institutions[:3]):
            if data['matched_members'] >= 5:  # Only show institutions with meaningful sample size
                print(f"  {i+1}. {institution}: {data['retention_rate']:.1f}%")
        
        print("\nAnalysis completed successfully!")
        print("Check the 'reports' directory for detailed JSON files.")
        
    except FileNotFoundError as e:
        print(f"Error: Required data files not found: {e}")
        print("Please ensure the following files are in the 'data/raw' directory:")
        print("  - Are they still in PEI? - Members Summary.csv")
        print("  - Website Memberships-Backend-2023.csv")
        print("  - Website Memberships-Backend-2024.csv")
        sys.exit(1)
    
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 