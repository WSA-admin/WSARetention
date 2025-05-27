#!/usr/bin/env python3
"""
Analyze graduation retention patterns for WSA members
"""

from src.data_processor import DataProcessor
from src.graduation_analyzer import GraduationAnalyzer
import json
from pathlib import Path

def main():
    # Initialize analyzers
    processor = DataProcessor()
    processor.preprocess_data()
    
    grad_analyzer = GraduationAnalyzer(processor)
    
    print("=== WSA GRADUATION RETENTION ANALYSIS ===")
    print()
    
    # Analyze 2023
    print("📊 2023 GRADUATION RETENTION ANALYSIS")
    print("=" * 50)
    analysis_2023 = grad_analyzer.analyze_graduation_retention(2023)
    display_graduation_analysis(analysis_2023)
    
    print()
    print("📊 2024 GRADUATION RETENTION ANALYSIS")  
    print("=" * 50)
    analysis_2024 = grad_analyzer.analyze_graduation_retention(2024)
    display_graduation_analysis(analysis_2024)
    
    print()
    print("📈 YEAR-OVER-YEAR COMPARISON")
    print("=" * 50)
    comparison = grad_analyzer.compare_graduation_retention_by_year()
    display_yoy_comparison(comparison)
    
    print()
    print("💾 EXPORTING DETAILED DATA...")
    export_path = grad_analyzer.export_graduation_analysis()
    print(f"✅ Detailed graduation analysis exported to: {export_path}")
    
    # Save JSON report
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    with open(reports_dir / "graduation_retention_analysis.json", 'w') as f:
        json.dump(comparison, f, indent=2, default=str)
    
    print(f"✅ JSON report saved to: reports/graduation_retention_analysis.json")

def display_graduation_analysis(analysis):
    """Display graduation analysis results."""
    year = analysis['year']
    total = analysis['total_analyzed']
    
    print(f"Total members analyzed: {total}")
    print()
    
    # Distribution
    print("Graduation Status Distribution:")
    for status, count in analysis['graduation_distribution'].items():
        percentage = (count / total) * 100
        print(f"  {status}: {count} ({percentage:.1f}%)")
    
    print()
    print("Retention by Graduation Status:")
    print("-" * 70)
    
    for grad_status, data in analysis['by_graduation_status'].items():
        print(f"\n🎓 {grad_status.upper()} ({data['total_members']} members)")
        
        retention = data['retention_percentages']
        print(f"  • Still in PEI: {retention['Still in PEI']:.1f}%")
        print(f"  • No longer in PEI: {retention['No longer in PEI']:.1f}%") 
        print(f"  • Inconclusive: {retention['Inconclusive']:.1f}%")
    
    print()
    print("Key Insights:")
    for insight in analysis['key_insights']:
        print(f"  ✨ {insight}")

def display_yoy_comparison(comparison):
    """Display year-over-year comparison."""
    if 'year_over_year_changes' in comparison:
        changes = comparison['year_over_year_changes']
        
        print("Retention Rate Changes (2023 → 2024):")
        print("-" * 50)
        
        for grad_status, change_data in changes.items():
            retention_2023 = change_data['2023_retention']
            retention_2024 = change_data['2024_retention']
            change = change_data['retention_change']
            
            trend = "↗️" if change > 0 else "↘️" if change < 0 else "→"
            
            print(f"{grad_status}:")
            print(f"  2023: {retention_2023:.1f}% → 2024: {retention_2024:.1f}% ({change:+.1f}%) {trend}")
        
        print()
        
        # Summary insights
        grad_change = changes.get('Likely Graduate', {}).get('retention_change', 0)
        student_change = changes.get('Current Student', {}).get('retention_change', 0)
        
        print("Summary Insights:")
        if grad_change > student_change:
            print(f"  🎯 Graduates showed better retention improvement (+{grad_change:.1f}% vs +{student_change:.1f}%)")
        elif student_change > grad_change:
            print(f"  🎯 Current students showed better retention improvement (+{student_change:.1f}% vs +{grad_change:.1f}%)")
        else:
            print(f"  🎯 Both groups showed similar retention changes")

if __name__ == "__main__":
    main() 