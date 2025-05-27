# Quick Start Guide - WSA Retention Analysis

This guide will help you quickly run the retention analysis and get results.

## Prerequisites

- Python 3.8+ installed
- Your CSV data files ready

## Step 1: Prepare Your Data

Make sure you have these three CSV files:
1. `Are they still in PEI? - Members Summary.csv` (retention survey data)
2. `Website Memberships-Backend-2023.csv` (2023 registrations)  
3. `Website Memberships-Backend-2024.csv` (2024 registrations)

Place them in the `data/raw/` directory.

## Step 2: Install Dependencies

Run this command in your terminal:

```bash
pip3 install pandas numpy matplotlib seaborn fuzzywuzzy python-Levenshtein
```

## Step 3: Run the Analysis

### Option 1: Complete Analysis (Recommended)
```bash
python3 run_analysis.py
```

This will:
- Analyze both 2023 and 2024 data
- Generate summary reports  
- Save detailed JSON files
- Show key insights

### Option 2: Interactive Python Analysis
```python
import sys
sys.path.append('src')

from retention_analyzer import RetentionAnalyzer

# Initialize analyzer
analyzer = RetentionAnalyzer()

# Run analysis for 2023
results_2023 = analyzer.analyze_retention(year=2023)
analyzer.print_summary(results_2023, year=2023)

# Run analysis for 2024  
results_2024 = analyzer.analyze_retention(year=2024)
analyzer.print_summary(results_2024, year=2024)

# Compare years
comparison = analyzer.compare_years(results_2023, results_2024)
```

## Step 4: View Results

After running the analysis, check:

1. **Console Output**: Summary statistics and key findings
2. **Reports Directory**: Detailed JSON files with complete analysis
3. **[Executive Summary](docs/analysis/executive-summary.md)**: Key findings and strategic insights
4. **[Complete Documentation](docs/README.md)**: Full documentation hub

## Understanding the Results

### Key Metrics Explained

- **Total Registered Members**: Number of people who signed up in that year
- **Members with Retention Data**: How many we could match with the survey
- **Match Rate**: Percentage of successful matches (higher is better)
- **Still in PEI**: Members confirmed to still be living in PEI
- **No Longer in PEI**: Members who have moved away
- **Inconclusive**: Status unclear (email bounced, no response, etc.)

### Example Output
```
============================================================
WSA RETENTION ANALYSIS SUMMARY - 2024
============================================================

OVERALL STATISTICS:
  Total Registered Members: 316
  Members with Retention Data: 275
  Match Rate: 87.0%

RETENTION BREAKDOWN:
  Still in PEI: 211 (76.7%)
  No Longer in PEI: 29 (10.5%)
  Inconclusive: 27 (9.8%)
  Unknown: 41
```

## Troubleshooting

### Common Issues

**Error: "File not found"**
- Make sure CSV files are in `data/raw/` directory
- Check file names match exactly

**Error: "Module not found"**
- Run: `pip3 install -r requirements.txt`
- Make sure you're in the project directory

**Low match rates**
- Check if email addresses in files are formatted consistently
- Verify member names are spelled similarly across files

### Getting Help

1. Check the full README.md for detailed documentation
2. Review the [Executive Summary](docs/analysis/executive-summary.md) for interpretation guidance
3. Browse the [Complete Documentation](docs/README.md) for all guides and resources
4. Examine the JSON files in `reports/` for raw data

## Next Steps

1. **Review Results**: Analyze the retention percentages and trends
2. **Institution Analysis**: Look at performance by school
3. **Action Planning**: Use insights to improve retention strategies
4. **Regular Updates**: Re-run analysis with new data periodically

---

## Quick Commands Reference

```bash
# Install dependencies
pip3 install pandas numpy matplotlib seaborn fuzzywuzzy python-Levenshtein

# Run complete analysis
python3 run_analysis.py

# Check results
ls reports/
cat docs/analysis/executive-summary.md
```

That's it! You should now have comprehensive retention analysis results. 