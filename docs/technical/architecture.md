# System Architecture

*🏠 [Back to Documentation](../README.md) | 🔧 [API Reference](api-reference.md) | ⚡ [Advanced Usage](advanced-usage.md)*

---

## 🏗️ System Overview

The WSA Retention Analysis System is a Python-based data processing pipeline designed for analyzing member retention patterns with advanced matching algorithms.

### **Core Components**
```
WSARetention/
├── src/                      # Core analysis modules
├── data/                     # Data storage (protected)
├── reports/                  # Generated analysis outputs
├── docs/                     # Documentation
├── tests/                    # Unit tests
└── notebooks/                # Interactive analysis
```

---

## 🔧 Key Modules

### **DataProcessor** (`src/data_processor.py`)
**Purpose**: Data loading, cleaning, and preprocessing  
**Key Features**:
- CSV file handling with security protection
- Data standardization (names, emails)
- Duplicate detection and handling
- Cross-year data integration

### **RetentionAnalyzer** (`src/retention_analyzer.py`)  
**Purpose**: Core retention analysis and reporting  
**Key Features**:
- Member status calculation
- Institution-wise breakdown
- Trend analysis across years
- Statistical reporting

### **MatchingAnalyzer** (`src/matching_analyzer.py`)
**Purpose**: Advanced member matching algorithms  
**Key Features**:
- Fuzzy string matching (85%+ confidence)
- Phonetic matching for name variations
- Email username matching
- Nickname detection and mapping
- LinkedIn-ready export formatting

### **GraduationAnalyzer** (`src/graduation_analyzer.py`)
**Purpose**: Graduation status classification and analysis using actual student status data  
**Key Features**:
- Direct "Student Status" field mapping from registration data
- Graduate vs student retention comparison
- Year-over-year graduate population analysis
- Post-graduation intervention insights

---

## 📊 Data Flow

### **1. Data Ingestion**
```
Raw CSV Files → DataProcessor → Cleaned DataFrames
```
- Retention survey data (961 records)
- 2023 registrations (365 records)  
- 2024 registrations (316 records)

### **2. Matching Process**
```
Registration Data → MatchingAnalyzer → Matched Records
```
- **Level 1**: Exact email matching (highest confidence)
- **Level 2**: Exact name matching
- **Level 3**: Fuzzy name matching (75%+ threshold)
- **Level 4**: Phonetic + username matching
- **Export**: Unmatched records for manual research

### **3. Analysis Pipeline**
```
Matched Data → RetentionAnalyzer → Statistical Reports
               ↓
             GraduationAnalyzer → Graduate-specific insights
```

### **4. Output Generation**
```
Analysis Results → JSON Reports + CSV Exports + Markdown Summaries
```

---

## 🔒 Security Architecture

### **Data Protection**
- `.gitignore` blocks all sensitive files
- Sample data for safe demonstrations
- Automatic path protection for real data
- Clear separation of demo vs production

### **Access Control**
- Local file system security
- No external data transmission
- Manual approval for all operations
- Comprehensive audit trails

---

## ⚡ Performance Characteristics

### **Processing Speed**
- **Small datasets** (<1000 records): <30 seconds
- **Current scale** (1642 total records): ~2 minutes
- **Matching algorithms**: Linear scaling with record count
- **Memory usage**: <500MB for current datasets

### **Scalability Limits**
- **Recommended max**: 10,000 records per analysis
- **Fuzzy matching**: Computationally intensive at scale
- **Export formats**: CSV scales better than JSON for large datasets

---

## 🔄 Algorithm Details

### **Enhanced Matching (v2.0)**

#### **Fuzzy String Matching**
```python
# Uses fuzzywuzzy library with Levenshtein distance
threshold = 75  # Configurable confidence level
matches = process.extract(name, survey_names, limit=3)
```

#### **Phonetic Matching**
```python
# Consonant-based comparison for sound-alike names
name_consonants = re.sub(r'[aeiou]', '', name.lower())
threshold = 85  # Higher threshold for phonetic
```

#### **Email Username Analysis**
```python
# Compare email usernames across domains
username_similarity = fuzz.ratio(reg_username, survey_username)
threshold = 75  # Username matching confidence
```

### **Graduation Classification**
```python
# Uses actual "Student Status" field from registration data
def classify_graduation_status(student_status):
    if student_status == "Graduate":
        return "Graduate"
    elif student_status == "Current Student":
        return "Current Student"
    else:
        return "Unknown"
```

---

## 📈 System Evolution

### **Version 1.0** (Initial)
- Basic exact matching only
- Manual data quality checks
- Simple statistical reporting

### **Version 2.0** (Current) 
- Enhanced fuzzy matching algorithms
- Automated quality assessment
- Graduation status analysis
- LinkedIn export functionality
- Comprehensive documentation

### **Version 3.0** (Planned)
- Real-time dashboard
- Predictive analytics
- Automated survey integration
- API endpoints for external systems

---

## 🛠️ Development Environment

### **Requirements**
- Python 3.8+
- pandas, numpy (data processing)
- fuzzywuzzy (string matching)
- matplotlib, seaborn (visualization)
- jupyter (interactive analysis)

### **Setup Commands**
```bash
pip install -r requirements.txt  # Install dependencies
python3 run_demo.py              # Test with sample data
python3 run_analysis.py          # Run with real data
```

### **Testing**
```bash
python3 -m pytest tests/         # Unit tests
python3 check_data_quality.py    # Quality verification
python3 check_security.py        # Security audit
```

---

## 🔧 Configuration

### **Key Settings** (`src/config.py` - if needed)
- Fuzzy matching thresholds
- Institution name mappings  
- Program duration definitions
- Export format preferences

### **Environment Variables**
- `WSA_DATA_PATH`: Override default data directory
- `WSA_EXPORT_PATH`: Custom export location
- `WSA_DEBUG`: Enable detailed logging

---

*⚡ **Performance Tip**: For large datasets, run matching algorithms in batches and cache intermediate results.* 