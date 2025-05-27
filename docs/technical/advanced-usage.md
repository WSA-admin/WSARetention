# Advanced Usage

*🏠 [Back to Documentation](../README.md) | 🏗️ [Architecture](architecture.md) | 🔧 [API Reference](api-reference.md)*

---

## 🚀 Power User Features

### **Custom Matching Algorithms**
```python
# Create custom matching analyzer with specific thresholds
from src.matching_analyzer import MatchingAnalyzer

analyzer = MatchingAnalyzer(data_processor)

# High-precision matching (stricter)
high_precision = analyzer.improved_matching(2024, confidence_threshold=90)

# High-recall matching (more permissive)  
high_recall = analyzer.improved_matching(2024, confidence_threshold=65)
```

### **Batch Processing Multiple Years**
```python
def analyze_multiple_years(years):
    results = {}
    for year in years:
        matched_data = processor.match_members(year)
        results[year] = {
            'total': len(matched_data),
            'matched': len(matched_data[matched_data['retention_status'] != 'Unknown']),
            'retention_rate': len(matched_data[matched_data['retention_status'] == 'Still in PEI']) / len(matched_data) * 100
        }
    return results

# Usage
yearly_results = analyze_multiple_years([2021, 2022, 2023, 2024])
```

---

## 📊 Custom Analysis Patterns

### **Institution-Specific Deep Dive**
```python
def analyze_institution(institution_name, year):
    matched_data = processor.match_members(year)
    
    # Filter by institution
    inst_data = matched_data[matched_data['Institution of Study'] == institution_name]
    
    # Calculate metrics
    total = len(inst_data)
    retention_stats = inst_data['retention_status'].value_counts()
    
    return {
        'institution': institution_name,
        'total_members': total,
        'retention_breakdown': retention_stats.to_dict(),
        'retention_rate': (retention_stats.get('Still in PEI', 0) / total) * 100
    }

# Usage
dalhousie_analysis = analyze_institution('Dalhousie', 2024)
```

### **Program-Level Retention Analysis**
```python
def analyze_by_program(year, min_members=5):
    matched_data = processor.match_members(year)
    matched_only = matched_data[matched_data['retention_status'] != 'Unknown']
    
    results = {}
    for program in matched_only['Program of Study'].unique():
        program_data = matched_only[matched_only['Program of Study'] == program]
        
        if len(program_data) >= min_members:  # Only analyze programs with sufficient data
            retention_rate = (len(program_data[program_data['retention_status'] == 'Still in PEI']) / len(program_data)) * 100
            results[program] = {
                'total_members': len(program_data),
                'retention_rate': retention_rate,
                'outmigration_rate': (len(program_data[program_data['retention_status'] == 'No longer in PEI']) / len(program_data)) * 100
            }
    
    return results

program_analysis = analyze_by_program(2024, min_members=3)
```

---

## 🔧 Data Quality Enhancement

### **Custom Data Cleaning**
```python
def enhanced_data_cleaning(df):
    """Custom data cleaning beyond standard preprocessing"""
    
    # Remove common title variations
    df['Name'] = df['Name'].str.replace(r'\b(Dr|Prof|Mr|Mrs|Ms)\.?\s+', '', regex=True)
    
    # Standardize university names
    university_mappings = {
        'UPEI': 'University of Prince Edward Island',
        'Dal': 'Dalhousie University',
        'CBU': 'Cape Breton University'
    }
    
    for short, full in university_mappings.items():
        df['Institution of Study'] = df['Institution of Study'].str.replace(short, full)
    
    return df

# Apply to data before analysis
processor.registrations_2024 = enhanced_data_cleaning(processor.registrations_2024)
```

### **Advanced Duplicate Detection**
```python
def find_potential_duplicates(df, similarity_threshold=85):
    """Find potential duplicates using fuzzy matching"""
    from fuzzywuzzy import fuzz
    
    potential_duplicates = []
    names = df['Name'].dropna().tolist()
    
    for i, name1 in enumerate(names):
        for j, name2 in enumerate(names[i+1:], i+1):
            similarity = fuzz.ratio(name1.lower(), name2.lower())
            if similarity >= similarity_threshold:
                potential_duplicates.append({
                    'name1': name1,
                    'name2': name2,
                    'similarity': similarity,
                    'index1': i,
                    'index2': j
                })
    
    return potential_duplicates

duplicates = find_potential_duplicates(processor.registrations_2024)
```

---

## 📈 Advanced Analytics

### **Retention Trend Analysis**
```python
def calculate_retention_trends(years):
    """Calculate retention trends across multiple years"""
    trends = {}
    
    for year in years:
        matched_data = processor.match_members(year)
        matched_only = matched_data[matched_data['retention_status'] != 'Unknown']
        
        total = len(matched_only)
        still_in_pei = len(matched_only[matched_only['retention_status'] == 'Still in PEI'])
        
        trends[year] = {
            'total_analyzed': total,
            'retention_count': still_in_pei,
            'retention_rate': (still_in_pei / total) * 100 if total > 0 else 0
        }
    
    # Calculate year-over-year changes
    years_sorted = sorted(years)
    for i in range(1, len(years_sorted)):
        current_year = years_sorted[i]
        previous_year = years_sorted[i-1]
        
        change = trends[current_year]['retention_rate'] - trends[previous_year]['retention_rate']
        trends[current_year]['yoy_change'] = change
    
    return trends

trends = calculate_retention_trends([2022, 2023, 2024])
```

### **Predictive Modeling Setup**
```python
def prepare_features_for_ml(matched_data):
    """Prepare features for machine learning models"""
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder
    
    # Create feature matrix
    features = matched_data.copy()
    
    # Encode categorical variables
    le_institution = LabelEncoder()
    features['institution_encoded'] = le_institution.fit_transform(features['Institution of Study'])
    
    le_program = LabelEncoder()
    features['program_encoded'] = le_program.fit_transform(features['Program of Study'])
    
    le_country = LabelEncoder()
    features['country_encoded'] = le_country.fit_transform(features['Country of Origin'])
    
    # Create target variable (binary: stayed or left)
    features['stayed_in_pei'] = (features['retention_status'] == 'Still in PEI').astype(int)
    
    # Extract enrollment features
    features['enrollment_date'] = pd.to_datetime(features['Date of Enrollment'])
    features['enrollment_month'] = features['enrollment_date'].dt.month
    features['enrollment_year'] = features['enrollment_date'].dt.year
    
    return features

ml_features = prepare_features_for_ml(matched_2024)
```

---

## 🔍 Debugging & Diagnostics

### **Detailed Matching Analysis**
```python
def debug_matching_process(name, year):
    """Debug why a specific member wasn't matched"""
    
    # Get registration data
    if year == 2023:
        registrations = processor.registrations_2023
    else:
        registrations = processor.registrations_2024
    
    # Find the registration
    reg = registrations[registrations['Name'].str.contains(name, case=False, na=False)]
    
    if len(reg) == 0:
        print(f"No registration found for '{name}' in {year}")
        return
    
    reg_record = reg.iloc[0]
    print(f"Registration: {reg_record['Name']} | {reg_record['Email']}")
    
    # Try different matching strategies
    survey = processor.retention_survey
    
    # Exact email match
    email_matches = survey[survey['email_clean'] == reg_record['email_clean']]
    print(f"Exact email matches: {len(email_matches)}")
    
    # Exact name match  
    name_matches = survey[survey['name_clean'] == reg_record['name_clean']]
    print(f"Exact name matches: {len(name_matches)}")
    
    # Fuzzy name matches
    from fuzzywuzzy import process
    fuzzy_matches = process.extract(reg_record['name_clean'], survey['name_clean'], limit=5)
    print(f"Top fuzzy matches: {fuzzy_matches}")

debug_matching_process("John Smith", 2024)
```

### **Performance Monitoring**
```python
import time
import psutil
import pandas as pd

def performance_monitor(func):
    """Decorator to monitor function performance"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        print(f"Function: {func.__name__}")
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        print(f"Memory usage: {end_memory - start_memory:.2f} MB")
        
        return result
    return wrapper

# Usage
@performance_monitor
def analyze_with_monitoring():
    return processor.match_members(2024)

results = analyze_with_monitoring()
```

---

## 🔄 Automation & Scheduling

### **Automated Report Generation**
```python
def generate_automated_report(output_dir="reports"):
    """Generate comprehensive automated report"""
    from pathlib import Path
    import json
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Run all analyses
    matched_2023 = processor.match_members(2023)
    matched_2024 = processor.match_members(2024)
    
    # Generate graduation analysis
    from src.graduation_analyzer import GraduationAnalyzer
    grad_analyzer = GraduationAnalyzer(processor)
    grad_comparison = grad_analyzer.compare_graduation_retention_by_year()
    
    # Compile report
    report = {
        'timestamp': timestamp,
        'summary': {
            '2023': {
                'total': len(matched_2023),
                'matched': len(matched_2023[matched_2023['retention_status'] != 'Unknown']),
                'match_rate': len(matched_2023[matched_2023['retention_status'] != 'Unknown']) / len(matched_2023) * 100
            },
            '2024': {
                'total': len(matched_2024),
                'matched': len(matched_2024[matched_2024['retention_status'] != 'Unknown']),
                'match_rate': len(matched_2024[matched_2024['retention_status'] != 'Unknown']) / len(matched_2024) * 100
            }
        },
        'graduation_analysis': grad_comparison
    }
    
    # Save report
    output_path = Path(output_dir) / f"automated_report_{timestamp}.json"
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"Report generated: {output_path}")
    return output_path

report_path = generate_automated_report()
```

---

*⚡ **Pro Tip**: Combine multiple advanced techniques for maximum insight - use custom matching with institution-specific analysis and performance monitoring for production-ready analyses.* 