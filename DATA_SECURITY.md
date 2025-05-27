# Data Security Guide

## ⚠️ IMPORTANT: Protecting Sensitive Information

This project analyzes retention data that may contain **sensitive personal information** including names, email addresses, and demographic data. It is crucial to protect this information when using the project.

## 🔒 What Data is Sensitive?

The following files contain personal information and must **NEVER** be committed to version control:

### Critical Files to Protect:
- `data/raw/*.csv` - All original CSV files
- `reports/*.json` - Generated analysis reports  
- `reports/*.html` - HTML reports
- Any backup files containing member data

### Sensitive Information Includes:
- **Names** - Full names of WSA members
- **Email Addresses** - Personal and institutional emails
- **Demographic Data** - Country of origin, programs, institutions
- **Retention Status** - Whether members are still in PEI

## 🛡️ Security Measures Implemented

### 1. Git Ignore Protection
The `.gitignore` file automatically excludes:
```
data/raw/*.csv
data/processed/*.csv
reports/*.json
reports/*.html
*.csv
```

### 2. Directory Structure
```
WSARetention/
├── data/
│   ├── raw/               # ← SENSITIVE: Real CSV files (ignored)
│   ├── processed/         # ← SENSITIVE: Processed data (ignored)
│   └── sample/           # ← SAFE: Dummy data for testing
├── reports/              # ← SENSITIVE: Generated reports (ignored)
└── src/                  # ← SAFE: Source code only
```

## 📋 Before Making Repository Public

### Step 1: Verify No Sensitive Data is Tracked
```bash
# Check what files are currently tracked
git status

# Check git history for sensitive files
git log --name-only | grep -E '\.(csv|json)$'

# If any sensitive files are tracked, remove them:
git rm --cached data/raw/*.csv
git rm --cached reports/*.json
```

### Step 2: Clean Git History (if needed)
If sensitive files were previously committed:
```bash
# Remove sensitive files from entire git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch data/raw/*.csv' \
  --prune-empty --tag-name-filter cat -- --all
```

### Step 3: Verify Protection
```bash
# This should show no CSV or JSON files
git ls-files | grep -E '\.(csv|json)$'
```

## 🧪 Using Sample Data

For demonstration and testing, use the provided sample data:

### Creating Sample Data Structure
```bash
# Create sample directory
mkdir -p data/sample

# Use anonymized sample files for testing
# (Sample files contain fake data only)
```

### Sample Data Features:
- ✅ Realistic data structure
- ✅ No real personal information  
- ✅ Safe to commit to GitHub
- ✅ Demonstrates all functionality

## 👥 For New Users

If you're using this project with your own data:

### 1. Setup Your Environment
```bash
# Clone the repository
git clone <repository-url>
cd WSARetention

# Install dependencies
pip3 install -r requirements.txt
```

### 2. Add Your Data Safely
```bash
# Create data directories
mkdir -p data/raw
mkdir -p data/processed

# Copy your CSV files to data/raw/
# (These will be automatically ignored by git)
```

### 3. Run Analysis
```bash
# Your data is protected, run analysis normally
python3 run_analysis.py
```

## 🔐 Best Practices

### For Data Handlers:
1. **Never share raw CSV files** via email, Slack, or cloud storage
2. **Use encrypted storage** for sensitive data files
3. **Regularly audit** who has access to data
4. **Delete old data** that's no longer needed
5. **Use VPN** when accessing data remotely

### For Developers:
1. **Always check `git status`** before committing
2. **Use `git add` selectively**, not `git add .`
3. **Review diffs** before pushing changes
4. **Test with sample data** first
5. **Document security measures** for team members

### For Organizations:
1. **Train staff** on data security practices
2. **Implement access controls** on data repositories  
3. **Regular security audits** of data handling
4. **Backup procedures** for sensitive data
5. **Incident response plan** for data breaches

## 🚨 Emergency Procedures

### If Sensitive Data is Accidentally Committed:

1. **Stop immediately** - Don't push if you haven't already
2. **Remove from staging**:
   ```bash
   git reset HEAD sensitive_file.csv
   ```
3. **Remove from last commit**:
   ```bash
   git reset --soft HEAD~1
   ```
4. **If already pushed** - Contact your Git admin immediately
5. **Clean history** if necessary (see Step 2 above)

### If Data Breach Occurs:
1. **Document the incident** - What data, when, how
2. **Notify stakeholders** - IT security, management, legal
3. **Secure the breach** - Remove access, change credentials
4. **Assess impact** - Who might be affected
5. **Follow organizational protocols** - Legal requirements vary

## 📞 Support

For security concerns or questions:
- Check with your IT security team
- Review your organization's data handling policies
- Contact the project maintainers for technical issues (but never include sensitive data in support requests)

---

## ✅ Security Checklist

Before making the repository public:

- [ ] `.gitignore` file is in place
- [ ] No CSV files in git history
- [ ] No JSON reports in git history  
- [ ] Sample data created for demonstration
- [ ] Team trained on security practices
- [ ] Data access controls implemented
- [ ] Backup procedures documented

---

**Remember: When in doubt, keep it private. It's better to be overly cautious with sensitive data.** 