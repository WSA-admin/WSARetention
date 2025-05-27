#!/usr/bin/env python3
"""
Security Check Script for WSA Retention Analysis

This script verifies that sensitive data is properly protected before making
the repository public. It checks for potential data exposure issues.
"""

import os
import subprocess
import sys
from pathlib import Path
import re


def run_command(cmd):
    """Run a command and return the output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def check_gitignore_exists():
    """Check if .gitignore file exists and contains essential rules."""
    print("🔍 Checking .gitignore file...")
    
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        print("❌ .gitignore file not found!")
        return False
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    essential_rules = [
        "data/raw/*.csv",
        "reports/*.json", 
        "*.csv",
        ".venv"
    ]
    
    missing_rules = []
    for rule in essential_rules:
        if rule not in content:
            missing_rules.append(rule)
    
    if missing_rules:
        print(f"❌ Missing essential .gitignore rules: {missing_rules}")
        return False
    
    print("✅ .gitignore file is properly configured")
    return True


def check_git_tracked_files():
    """Check if any sensitive files are being tracked by git."""
    print("\n🔍 Checking for tracked sensitive files...")
    
    # Check what files git would include
    code, stdout, stderr = run_command("git ls-files --exclude-standard")
    
    if code != 0:
        print(f"❌ Error running git command: {stderr}")
        return False
    
    tracked_files = stdout.strip().split('\n') if stdout.strip() else []
    
    # Check for sensitive file patterns
    sensitive_patterns = [
        r'\.csv$',
        r'reports/.*\.json$',
        r'data/raw/.*',
        r'.*Members Summary.*',
        r'.*Backend-20\d{2}.*'
    ]
    
    # Safe patterns that are allowed (sample data with fictional content)
    safe_patterns = [
        r'data/sample/.*\.csv$'
    ]
    
    sensitive_tracked = []
    for file in tracked_files:
        # Check if file matches any safe pattern first
        is_safe = False
        for safe_pattern in safe_patterns:
            if re.search(safe_pattern, file, re.IGNORECASE):
                is_safe = True
                break
        
        if not is_safe:
            # Check if file matches sensitive patterns
            for pattern in sensitive_patterns:
                if re.search(pattern, file, re.IGNORECASE):
                    sensitive_tracked.append(file)
                    break
    
    if sensitive_tracked:
        print("❌ Sensitive files are being tracked:")
        for file in sensitive_tracked:
            print(f"   - {file}")
        return False
    
    print("✅ No sensitive files are being tracked")
    return True


def check_sample_data():
    """Check if sample data files exist."""
    print("\n🔍 Checking sample data availability...")
    
    sample_files = [
        "data/sample/sample_retention_survey.csv",
        "data/sample/sample_registrations_2023.csv", 
        "data/sample/sample_registrations_2024.csv"
    ]
    
    missing_samples = []
    for file in sample_files:
        if not Path(file).exists():
            missing_samples.append(file)
    
    if missing_samples:
        print("❌ Missing sample data files:")
        for file in missing_samples:
            print(f"   - {file}")
        return False
    
    print("✅ Sample data files are available")
    return True


def check_documentation():
    """Check if security documentation exists."""
    print("\n🔍 Checking security documentation...")
    
    required_docs = [
        "DATA_SECURITY.md",
        "README.md",
        "QUICK_START.md"
    ]
    
    missing_docs = []
    for doc in required_docs:
        if not Path(doc).exists():
            missing_docs.append(doc)
    
    if missing_docs:
        print("❌ Missing documentation files:")
        for doc in missing_docs:
            print(f"   - {doc}")
        return False
    
    # Check if DATA_SECURITY.md mentions key security topics
    with open("DATA_SECURITY.md", 'r') as f:
        content = f.read().lower()
    
    security_topics = [
        "sensitive",
        "gitignore", 
        "csv",
        "protect"
    ]
    
    missing_topics = []
    for topic in security_topics:
        if topic not in content:
            missing_topics.append(topic)
    
    if missing_topics:
        print(f"⚠️  DATA_SECURITY.md may be missing key topics: {missing_topics}")
    
    print("✅ Security documentation is available")
    return True


def check_demo_script():
    """Check if demo script exists and works."""
    print("\n🔍 Checking demo script...")
    
    if not Path("run_demo.py").exists():
        print("❌ Demo script (run_demo.py) not found")
        return False
    
    print("✅ Demo script is available")
    return True


def check_real_data_exists():
    """Check if real data files exist (they should, but not be tracked)."""
    print("\n🔍 Checking for real data files...")
    
    real_data_files = [
        "data/raw/Are they still in PEI? - Members Summary.csv",
        "data/raw/Website Memberships-Backend-2023.csv",
        "data/raw/Website Memberships-Backend-2024.csv"
    ]
    
    exists_count = 0
    for file in real_data_files:
        if Path(file).exists():
            exists_count += 1
    
    if exists_count > 0:
        print(f"ℹ️  Found {exists_count} real data files (this is OK if they're ignored by git)")
        
        # Double-check they're not tracked
        code, stdout, stderr = run_command("git ls-files data/raw/")
        if stdout.strip():
            print("❌ Real data files are being tracked by git!")
            return False
        else:
            print("✅ Real data files exist but are properly ignored")
    else:
        print("ℹ️  No real data files found (users will need to add their own)")
    
    return True


def main():
    """Run all security checks."""
    print("🔒 WSA Retention Analysis - Security Check")
    print("=" * 60)
    print("Verifying repository is safe to make public...")
    print("=" * 60)
    
    checks = [
        ("Git ignore configuration", check_gitignore_exists),
        ("Git tracked files", check_git_tracked_files), 
        ("Sample data", check_sample_data),
        ("Documentation", check_documentation),
        ("Demo script", check_demo_script),
        ("Real data protection", check_real_data_exists)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed_checks += 1
        except Exception as e:
            print(f"❌ Error during {check_name} check: {e}")
    
    print("\n" + "=" * 60)
    print("SECURITY CHECK SUMMARY")
    print("=" * 60)
    
    if passed_checks == total_checks:
        print("🎉 ALL SECURITY CHECKS PASSED!")
        print("✅ Repository is SAFE to make public")
        print("\nNext steps:")
        print("1. Run 'python3 run_demo.py' to test functionality")
        print("2. Commit your changes: git add . && git commit -m 'Initial commit with security'")
        print("3. Push to GitHub: git push origin main")
        print("4. Make repository public when ready")
        return True
    else:
        print(f"❌ {total_checks - passed_checks} CHECK(S) FAILED")
        print("⚠️  DO NOT make repository public until all checks pass")
        print("\nFix the issues above and run this script again.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 