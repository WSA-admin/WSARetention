# API Reference

*🏠 [Back to Documentation](../README.md) | 🏗️ [Architecture](architecture.md) | ⚡ [Advanced Usage](advanced-usage.md)*

---

## 🔧 Core Classes

### **DataProcessor**
```python
from src.data_processor import DataProcessor

processor = DataProcessor()
processor.preprocess_data()  # Load and clean all data
matched_data = processor.match_members(2024)  # Get matched data for year
```

#### **Key Methods**
- `preprocess_data()` - Load and clean all CSV files
- `match_members(year)` - Return matched registration + retention data
- `get_unmatched_members(year)` - Return unmatched registrations

---

### **MatchingAnalyzer**
```python
from src.matching_analyzer import MatchingAnalyzer

analyzer = MatchingAnalyzer(data_processor)
results = analyzer.analyze_unmatched_records(2024)
improved = analyzer.improved_matching(2024, confidence_threshold=75)
```

#### **Key Methods**
- `analyze_unmatched_records(year)` - Detailed analysis of unmatched members
- `improved_matching(year, threshold)` - Enhanced matching with fuzzy algorithms
- `export_unmatched_for_manual_review(year)` - Generate LinkedIn research CSV

---

### **GraduationAnalyzer**  
```python
from src.graduation_analyzer import GraduationAnalyzer

grad_analyzer = GraduationAnalyzer(data_processor)
analysis = grad_analyzer.analyze_graduation_retention(2024)
comparison = grad_analyzer.compare_graduation_retention_by_year()
```

#### **Key Methods**
- `analyze_graduation_retention(year)` - Graduate vs student analysis
- `compare_graduation_retention_by_year()` - Year-over-year comparison
- `classify_graduation_status(program, date)` - Individual classification

---

## 📊 Common Usage Patterns

### **Basic Analysis Workflow**
```python
# 1. Initialize system
from src.data_processor import DataProcessor
processor = DataProcessor()
processor.preprocess_data()

# 2. Get matched data
matched_2024 = processor.match_members(2024)
retention_stats = matched_2024['retention_status'].value_counts()

# 3. Enhanced matching for unmatched
from src.matching_analyzer import MatchingAnalyzer
matcher = MatchingAnalyzer(processor)
improved_results = matcher.improved_matching(2024)

# 4. Export for manual research
csv_path = matcher.export_unmatched_for_manual_review(2024)
```

### **Graduation Analysis Workflow**
```python
# 1. Setup graduation analyzer
from src.graduation_analyzer import GraduationAnalyzer
grad_analyzer = GraduationAnalyzer(processor)

# 2. Analyze by graduation status
grad_results = grad_analyzer.analyze_graduation_retention(2024)

# 3. Export detailed data
export_path = grad_analyzer.export_graduation_analysis()
```

---

## 📈 Data Structures

### **Matched Data DataFrame**
```python
# Columns in matched_members result:
matched_data.columns = [
    'Name', 'Email', 'Institution of Study', 'Program of Study',
    'Date of Enrollment', 'Country of Origin', 'retention_status',
    'match_type', 'match_confidence'
]

# retention_status values:
# - 'Still in PEI'
# - 'No longer in PEI' 
# - 'Inconclusive'
# - 'Unknown' (unmatched)
```

### **Analysis Results Dictionary**
```python
# Structure of analysis results:
{
    'year': 2024,
    'total_registrations': 316,
    'matched': 278,
    'unmatched': 38,
    'match_rate': 88.0,
    'retention_breakdown': {
        'Still in PEI': 211,
        'No longer in PEI': 29,
        'Inconclusive': 27
    },
    'unmatched_analysis': {...},
    'recommendations': [...]
}
```

---

## ⚙️ Configuration Options

### **Matching Thresholds**
```python
# Fuzzy matching confidence levels
EXACT_MATCH = 100
HIGH_CONFIDENCE = 85
MEDIUM_CONFIDENCE = 75
LOW_CONFIDENCE = 60

# Usage in improved_matching
improved = analyzer.improved_matching(2024, confidence_threshold=75)
```

### **Program Duration Mapping**
```python
# Customize graduation classification
program_durations = {
    'bachelor': 4,      # years
    'master': 2,        # years
    'diploma': 1.5,     # years
    'certificate': 1    # year
}
```

---

## 🔍 Debugging & Logging

### **Enable Debug Mode**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run analysis with detailed logs
processor = DataProcessor()
processor.preprocess_data()  # Will show detailed loading info
```

### **Check Data Quality**
```bash
python3 check_data_quality.py  # Automated quality checks
```

### **Verify Security**
```bash
python3 check_security.py     # Security audit
```

---

## 📤 Export Functions

### **CSV Exports**
```python
# Unmatched members for research
csv_path = matcher.export_unmatched_for_manual_review(2024)
# Output: manual_review/unmatched_members_2024_for_review.csv

# Graduation analysis
grad_path = grad_analyzer.export_graduation_analysis()
# Output: reports/graduation_retention_analysis.csv
```

### **JSON Reports**
```python
import json

# Save analysis results
with open('reports/analysis_2024.json', 'w') as f:
    json.dump(analysis_results, f, indent=2)
```

---

## 🚨 Error Handling

### **Common Errors**
```python
try:
    processor.preprocess_data()
except FileNotFoundError:
    print("Data files not found. Check data/raw/ directory.")
except pd.errors.EmptyDataError:
    print("CSV files are empty or corrupted.")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### **Data Validation**
```python
# Check data completeness
if processor.retention_survey is None:
    raise ValueError("Retention survey data not loaded")

if len(processor.registrations_2024) == 0:
    raise ValueError("No 2024 registration data found")
```

---

*📚 **Note**: All functions return structured data types (DataFrames, dictionaries) for easy integration with external systems.* 