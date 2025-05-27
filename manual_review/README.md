# Manual Review Directory

This directory contains files for manual research of unmatched members.

## Current Files

### `unmatched_members_2024_for_review.csv`
**⚠️ Important Note**: This file was generated before PEI-only filtering was implemented and contains **Nova Scotia students** who will be automatically filtered out in future analyses.

**Nova Scotia Institutions Included (to be filtered out)**:
- Dalhousie University (multiple entries)
- Cape Breton University (multiple entries) 
- Saint Mary's University
- NSCC (Nova Scotia Community College)
- Acadia University
- Mount Saint Vincent University

**PEI Students Only**: Milka Mburu (Holland College)

## Next Steps

When you run the analysis with the updated PEI-only filtering:

1. **Run New Analysis**: `python3 analyze_unmatched.py`
2. **Generate PEI-Only CSV**: This will create a new file with only PEI students
3. **Archive This File**: This file serves as historical reference

## PEI Institutions

The analysis now focuses exclusively on:
- **UPEI** (University of Prince Edward Island)
- **Holland College** 
- **Collège de l'Île**
- **Maritime Christian College**
- **PEI Paramedic Academy**

Students from Nova Scotia institutions are automatically excluded to maintain the PEI retention focus. 