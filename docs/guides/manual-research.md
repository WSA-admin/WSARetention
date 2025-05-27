# Manual Research Guide - LinkedIn & Contact Verification

*🏠 [Back to Documentation](../README.md) | 🔍 [Unmatched Members List](../analysis/unmatched-members.md)*

---

## 🎯 Current Task: 38 Unmatched Members Research

**Goal**: Verify retention status for 38 members using LinkedIn and alternative contact methods  
**Files**: `manual_review/unmatched_members_2024_for_review.csv`  
**Timeline**: 2-3 weeks (20-30 hours estimated)

---

## 📋 Research Process

### **Step 1: Prepare Research Spreadsheet**
1. Open `manual_review/unmatched_members_2024_for_review.csv`
2. Columns ready for completion:
   - `LinkedIn_URL` - Profile link if found
   - `Manual_Status` - Still in PEI / No longer in PEI / Inconclusive
   - `Notes` - Additional information
   - `Confidence_Level` - High / Medium / Low

### **Step 2: LinkedIn Research Method**
1. **Search Format**: Use `LinkedIn_Search_Name` column (pre-formatted)
2. **Institution Filter**: Add their institution to search
3. **Program Filter**: Include their program/field of study
4. **Location Verification**: Check current location in profile

### **Step 3: Verification Criteria**

#### ✅ **Still in PEI** (Confirmed)
- Current location shows PEI/Maritime provinces
- Recent posts/activity from PEI locations  
- Employment with PEI-based companies
- Educational status at PEI institutions

#### ❌ **No Longer in PEI** (Confirmed)
- Current location outside PEI/Maritime
- Employment with non-PEI companies
- Clear relocation posts/announcements
- Updated location in other provinces/countries

#### ❓ **Inconclusive** (Unclear)
- No clear location information
- Private/limited profile
- Conflicting information
- Unable to confirm identity

---

## 🔍 Research Strategies

### **Primary Method: LinkedIn**
- **Search**: "Name + Institution + Program"
- **Verify**: Profile photo, education history, connections
- **Location**: Current location field + recent activity
- **Employment**: Current job location indicators

### **Secondary Methods**
- **Google Search**: "Name + Institution" for news/achievements
- **University Websites**: Student directories, awards, news
- **Professional Networks**: Industry-specific platforms
- **Social Media**: Public profiles with location data

### **Institution-Specific Tips**
- **Dalhousie** (16 members): Check graduate announcements, research publications
- **Cape Breton University** (11 members): Smaller campus, easier verification
- **Others** (11 members): Check specific program websites

---

## 📊 Current Member List Breakdown

### **By Institution** (Focus Areas)
| Institution | Count | Strategy |
|-------------|--------|----------|
| Dalhousie | 16 | Graduate research, lab websites |
| Cape Breton University | 11 | Alumni networks, local connections |
| Saint Mary's University | 3 | Student achievement pages |
| Mount Saint Vincent University | 3 | Education program tracking |
| Others | 5 | Program-specific searches |

### **By Country** (Research Context)
| Country | Count | Notes |
|---------|--------|-------|
| Canada | 11 | Domestic retention focus |
| Nigeria | 7 | International student tracking |
| India | 6 | Tech/business program graduates |
| Ghana | 5 | Graduate school connections |
| Others | 9 | Various international programs |

---

## ✅ Quality Assurance

### **High Confidence** (90%+ certain)
- Direct profile match with clear location
- Recent activity confirming status
- Multiple verification sources

### **Medium Confidence** (70-89% certain)  
- Profile match with some uncertainty
- Limited recent activity
- Single source verification

### **Low Confidence** (<70% certain)
- Uncertain profile identification
- No recent location data
- Conflicting information

---

## 📝 Documentation Standards

### **Research Entry Format**
```
LinkedIn_URL: https://linkedin.com/in/profile-name
Manual_Status: Still in PEI
Notes: Currently employed at [Company] in Charlottetown, posted from UPEI campus Nov 2024
Confidence_Level: High
```

### **Common Scenarios**

#### **Graduate Working in PEI**
```
Manual_Status: Still in PEI
Notes: Graduated [Program] [Date], now working at [PEI Company], LinkedIn shows Charlottetown location
Confidence_Level: High
```

#### **Student Continuing Studies**
```
Manual_Status: Still in PEI  
Notes: Currently enrolled in [Program Year], recent campus posts, active student profile
Confidence_Level: High
```

#### **Relocated for Work**
```
Manual_Status: No longer in PEI
Notes: Moved to [City/Province] for position at [Company], updated location [Date]
Confidence_Level: High
```

#### **Unable to Verify**
```
Manual_Status: Inconclusive
Notes: Private profile, no recent activity, unable to confirm current location
Confidence_Level: Low
```

---

## 🚀 Efficiency Tips

### **Batch Research**
1. **Group by institution** for context switching
2. **Use institution networks** for cross-referencing  
3. **Check graduation lists** for recent completers
4. **LinkedIn advanced search** for location filtering

### **Time Management**
- **10-15 minutes per member** average
- **High-priority**: Recent graduates, local connections
- **Quick wins**: Clear profiles with location data
- **Save complex cases** for dedicated time

### **Verification Shortcuts**
- **Alumni pages**: Recent graduate announcements
- **Company directories**: PEI-based employment
- **News articles**: Awards, achievements, relocations
- **University announcements**: Student success stories

---

## 📞 Follow-up Actions

### **After Research Completion**
1. **Upload completed CSV** to system
2. **Run updated analysis** with manual findings
3. **Generate final retention report** with 95%+ coverage
4. **Document lessons learned** for future improvement

### **System Updates**
1. **Update retention survey** with confirmed statuses
2. **Refine matching algorithms** based on findings
3. **Improve data collection** to prevent future gaps

---

*🎯 **Success Target**: Complete research for all 38 members with 80%+ high/medium confidence results* 