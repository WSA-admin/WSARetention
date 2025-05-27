# WSA Retention Analysis Project

## Project Overview

The **WSA Retention Analysis Project** is a data analysis tool designed to analyze member retention for Prince Edward Island (PEI). The project tracks whether members who registered in 2023 and 2024 are still residing in PEI, have moved away, or have inconclusive status.

## Purpose

This project aims to answer the key question: **"What percentage of members who registered on our platform are still living in PEI?"**

### Key Metrics
- How many members from 2023 are still on the island
- How many members from 2023 moved out
- How many members from 2023 have inconclusive status
- Similar analysis for 2024 members

## Data Sources

The project uses three main CSV files:

1. **`Are they still in PEI? - Members Summary.csv`** - Retention survey data with current status
2. **`Website Memberships-Backend-2023.csv`** - All 2023 member registrations  
3. **`Website Memberships-Backend-2024.csv`** - All 2024 member registrations

### Data Structure

#### Retention Survey Data
- **Name**: Member's full name
- **Status**: Current retention status (`Still in PEI`, `No longer in PEI`, `Inconclusive`)
- **Notes**: Additional details (e.g., "Email Undelivered", "LinkedIn not found")
- **Email Address**: Contact email

#### Registration Data (2023/2024)
- **Name**: Member's full name
- **Email**: Registration email
- **Date of Enrollment**: When they registered
- **Institution of Study**: UPEI, Holland College, Collège de l'Île
- **Program of Study**: Academic program
- **Province**: Location (Prince-Edward-Island) - **Note: Only PEI students are analyzed**
- **Other demographic data**: Country of origin, languages, education level, etc.

> 📍 **PEI Focus**: This analysis specifically tracks retention within Prince Edward Island. Students from other provinces (e.g., Nova Scotia) are automatically filtered out during processing to maintain focus on PEI-based outcomes.

## Technology Stack

- **Python 3.8+** - Core programming language
- **pandas** - Data manipulation and analysis
- **matplotlib/seaborn** - Data visualization
- **openpyxl** - Excel file handling
- **jupyter** - Interactive analysis notebooks

## Project Structure

```
WSARetention/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── data/                             # Data directory
│   ├── raw/                         # Raw CSV files
│   └── processed/                   # Cleaned/processed data
├── src/                             # Source code
│   ├── __init__.py
│   ├── data_processor.py           # Data cleaning and processing
│   ├── retention_analyzer.py       # Core analysis logic
│   └── visualizer.py              # Charts and graphs
├── notebooks/                       # Jupyter notebooks
│   ├── exploratory_analysis.ipynb
│   └── retention_report.ipynb
├── reports/                        # Generated reports
│   ├── 2023_retention_analysis.html
│   └── 2024_retention_analysis.html
└── tests/                          # Unit tests
    └── test_retention_analyzer.py
```

## 🔒 Data Security First

**⚠️ IMPORTANT: This project handles sensitive personal data. Please read [DATA_SECURITY.md](DATA_SECURITY.md) before proceeding.**

Key security features:
- ✅ Automatic `.gitignore` protection for all sensitive files
- ✅ Sample data for safe demonstration  
- ✅ Clear separation between real and demo data
- ✅ Comprehensive security guidelines

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd WSARetention
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Try the Demo First (Recommended)**
   ```bash
   python3 run_demo.py
   ```
   This uses fictional data to demonstrate all functionality safely.

4. **For Real Data Analysis**
   - Create `data/raw/` directory
   - Place your CSV files in `data/raw/` (they will be automatically protected by .gitignore)
   - File names should match exactly as described above

## Usage

### 🚀 Quick Demo (Safe - No Real Data)

Try the system with fictional data first:

```bash
python3 run_demo.py
```

### 📊 Real Data Analysis (After Setting Up Security)

```bash
# For production analysis with your real data
python3 run_analysis.py
```

### 🔧 Advanced Usage

```python
from src.retention_analyzer import RetentionAnalyzer

# Initialize the analyzer
analyzer = RetentionAnalyzer()

# Run analysis for both years
results_2023 = analyzer.analyze_retention(year=2023)
results_2024 = analyzer.analyze_retention(year=2024)

# Print summary
analyzer.print_summary(results_2023, year=2023)
analyzer.print_summary(results_2024, year=2024)
```

### 🔍 Unmatched Members Analysis

**✅ PROVEN RESULTS**: Analysis of real 2024 WSA data shows 88% match rate (278/316 members)

```bash
# Analyze and improve matching for unmatched members
python3 analyze_unmatched.py

# Check data quality issues
python3 check_data_quality.py

# Compare matching between years
python3 analyze_unmatched.py --compare
```

**Real Performance (PEI Students):**
- 🎯 **99.6% automatic matching** (~274 of ~275 PEI members)
- 📊 **Outstanding achievement** - Only 1 PEI student unmatched
- 📤 **1 member for research** (Milka Mburu - Holland College)
- 🔄 **Problem solved** - "Unmatched" were Nova Scotia students

**Key Insights from Real Data:**
- **"Data quality issue" resolved** - Was Nova Scotia students (out of scope)
- **PEI matching excellent** - 99.6% success rate achieved
- **Nova Scotia institutions automatically filtered out** (40 students excluded)

### Detailed Analysis

```python
# Load and examine the data
analyzer.load_data()
analyzer.explore_data()

# Get detailed breakdown
breakdown_2023 = analyzer.get_detailed_breakdown(2023)
breakdown_2024 = analyzer.get_detailed_breakdown(2024)

# Generate visualizations
analyzer.create_visualizations(breakdown_2023, year=2023)
analyzer.create_visualizations(breakdown_2024, year=2024)
```

## 📊 Analysis Results & Documentation

### **🚀 Quick Start**
- **[Executive Summary](docs/analysis/executive-summary.md)** - Key findings and strategic insights
- **[Complete Documentation](docs/README.md)** - Full documentation hub with navigation
- **[Quick Start Guide](QUICK_START.md)** - Get running in 5 minutes

### **📈 Latest Results** 
- **[2024 Analysis Results](docs/analysis/2024-analysis.md)** - Detailed findings (88% match rate, 76.7% retention)
- **[Graduation Analysis](docs/analysis/graduation-retention.md)** - Graduate vs student patterns (70.9% vs 80.4% graduates underperform)
- **[Unmatched Members](docs/analysis/unmatched-members.md)** - 38 members for manual research

## Expected Output

The analysis will provide:

### Summary Statistics
- Total members registered in 2023/2024
- Number still in PEI
- Number who moved out  
- Number with inconclusive status
- Retention percentages

### Detailed Breakdowns
- Institution-wise retention rates
- Program-wise analysis
- Country of origin impact
- Timeline analysis

### Visualizations
- Retention status pie charts
- Institution comparison bar charts
- Trend analysis over time
- Geographic distribution maps

## Key Features

- **Automated Name Matching**: Handles variations in name formatting
- **Email Cross-referencing**: Uses email addresses for verification
- **Data Validation**: Checks for inconsistencies and missing data
- **PEI-Focused Analysis**: Automatically filters to include only Prince Edward Island students
- **Province/Institution Filtering**: Excludes Nova Scotia and other non-PEI institutions
- **Flexible Reporting**: Generate reports for different time periods
- **Interactive Visualizations**: Charts and graphs for easy interpretation
- **Reusable Framework**: Easy to extend for future years

## Data Quality Considerations

- **Name Variations**: The system handles common name formatting differences
- **Email Matching**: Cross-references multiple email fields
- **Missing Data**: Identifies and reports on incomplete records
- **Duplicate Detection**: Flags potential duplicate registrations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analysis`)
3. Commit your changes (`git commit -am 'Add new analysis feature'`)
4. Push to the branch (`git push origin feature/new-analysis`)
5. Create a Pull Request

## Future Enhancements

- **Real-time Dashboard**: Web-based interface for live monitoring
- **Predictive Analytics**: ML models to predict retention likelihood
- **Survey Integration**: Automated survey distribution and collection
- **Geographic Mapping**: Interactive maps showing member locations
- **Automated Reporting**: Scheduled report generation and distribution

## 🚀 Making Repository Public

This repository is designed to be safely shared publicly. Before making it public:

### Pre-Publication Checklist

1. **Run Security Check**
   ```bash
   python3 check_security.py
   ```

2. **Test Demo Functionality**
   ```bash
   python3 run_demo.py
   ```

3. **Verify No Sensitive Data**
   ```bash
   git ls-files | grep -E '\.(csv|json)$'
   # Should return only sample files in data/sample/
   ```

### Safe to Share
- ✅ All source code
- ✅ Documentation files
- ✅ Sample/demo data
- ✅ Requirements and setup instructions

### Never Share
- ❌ Real CSV files with member data
- ❌ Generated reports with personal information
- ❌ Any backup files containing sensitive data

## License

This project is intended for internal use by the WSA organization for retention analysis. The code and methodology may be freely used by other organizations for similar analysis purposes.

## Contact

For questions or support regarding this project, please contact the WSA data team.

---

*Last updated: January 2025* 