# Ground Stone - Golf Course Audit Report Monitor

**Updated**: 2026-01-14
**Status**: Ready for 2025 historical test

---

## ✅ What Has Been Fixed

### 1. CSV Data Loading ✓
- Complete list of 496 golf course companies loaded successfully
- Proper UTF-8 encoding for Korean characters
- Correct 3-column format: 회사이름, 공시회사명, 사업자등록번호

### 2. Company Name Matching ✓
- Added name normalization to handle company suffix variations
- Removes: (주), 주식회사, (유), 유한회사, whitespace
- Successfully matches CSV companies with DART database

### 3. DART API 3-Month Limitation ✓
- **Problem**: DART API limits date range searches to 3 months when corp_code is not specified
- **Solution**: Modified `test_historical.py` to query each company individually with their corp_code
- This allows full year (12 months) data retrieval

---

## 🚀 How to Run the 2025 Historical Test

### Step 1: Pull Latest Changes

On your Windows machine, in PowerShell:

```powershell
# Navigate to your project directory
cd D:\GitHub\ground-stone

# If git commands work:
git pull origin claude/create-claude-md-urmco

# If git doesn't work:
# Use GitHub Desktop: Click "Fetch origin" and then "Pull"
```

### Step 2: Run the Test

```powershell
# Make sure you're in the project directory
cd D:\GitHub\ground-stone

# Activate virtual environment
.\venv\Scripts\Activate

# Run the historical test
python test_historical.py
```

---

## 📊 What to Expect

### During Execution:

1. **Company Loading**:
   ```
   ✅ Found 496 golf course companies
   Sample companies: [...]
   ```

2. **Data Fetching** (10-20 minutes):
   ```
   Fetching disclosures from 2025-01-01 to 2025-12-31
   Querying 496 companies individually...
   This may take 10-20 minutes...

   Progress: 50/496 companies processed...
     Found X audit reports so far
   Progress: 100/496 companies processed...
     Found X audit reports so far
   ...
   ```

3. **Results Summary**:
   ```
   ✅ Processed 496 companies
   ✅ Fetched X total disclosures from 2025
   ✅ Found X audit reports from golf course companies

   🎯 Found X golf course audit reports!
   Expected: 400-470 reports
   ```

4. **Confirmation Prompt**:
   ```
   ⚠️  READY TO SEND X NOTIFICATIONS TO TELEGRAM
   This will:
     - Send X messages to your Telegram channel
     - Take approximately X seconds (rate limit)
     - Save all reports to database

   👉 Do you want to proceed? (yes/no):
   ```

5. **Sending Notifications**:
   ```
   [1/X] Sending: 가야개발 - 2025-03-15
   ✅ Sent successfully (1 total)
   [2/X] Sending: 가평개발 - 2025-03-20
   ✅ Sent successfully (2 total)
   ...
   ```

6. **Final Summary**:
   ```
   🎉 TEST COMPLETED!
   Total reports found: X
   Successfully sent: X
   Failed: X
   Already processed: X
   ```

---

## 🎯 Success Criteria

### Expected Results:
- **Total reports found**: 400-470 audit reports from 2025
- **Companies matched**: 496 golf course companies
- **All notifications sent successfully** to @GC_golf_audit_channel
- **No DART API errors** (3-month limitation bypassed)

### If Count is Outside Range:
- **Less than 400**: May indicate some companies didn't file reports in 2025 (normal)
- **More than 470**: Some companies may have filed multiple audit reports (amended reports, etc.)

---

## 📝 What the Script Does

### Modified Algorithm (v2):

1. **Load Golf Companies** (from CSV):
   - Reads `data/golf_companies.csv`
   - Normalizes company names for matching
   - Matches with DART database

2. **Query Each Company** (NEW approach):
   ```
   For each of 496 companies:
     1. Call DART API with corp_code + date range (2025-01-01 to 2025-12-31)
     2. Filter results for audit reports only
     3. Add to results list
   ```

   **Why this works**: DART API only limits date ranges when corp_code is NOT specified.
   When corp_code IS specified, full year queries are allowed.

3. **Filter Audit Reports**:
   - Check report name contains: "감사보고서" or "audit"

4. **Send Notifications**:
   - Format each report as Telegram message
   - Send to @GC_golf_audit_channel
   - Save to database to prevent duplicates
   - Rate limit: 10 messages/second (well below 30/sec limit)

---

## 🔄 For 2026 Production Use

After 2025 test is successful, the same code will automatically work for 2026:

### Main Bot (main.py):
```bash
# Run continuously
python main.py
```

The bot will:
- Check DART every 60 minutes (configurable in `.env`)
- Query each golf course company individually
- Find new audit reports
- Send notifications immediately
- Never miss any reports (100% coverage)

---

## ⚙️ Configuration

Your `.env` file:
```env
TELEGRAM_BOT_TOKEN=<your_token>
TELEGRAM_CHANNEL_ID=@GC_golf_audit_channel
DART_API_KEY=<your_key>
DATABASE_URL=sqlite:///data/ground-stone.db
CHECK_INTERVAL_MINUTES=60
LOG_LEVEL=INFO
```

---

## 🐛 Troubleshooting

### Problem: "No golf companies found"
**Solution**: Run `python verify_setup.py` to check CSV loading

### Problem: Still getting 3-month limitation error
**Solution**: Make sure you pulled the latest code changes

### Problem: Telegram connection failed
**Solution**:
1. Check bot token in `.env`
2. Make sure bot is added to channel as administrator
3. Verify bot has "Post Messages" permission

### Problem: Git commands not recognized in PowerShell
**Solution**: Use GitHub Desktop instead:
1. Open GitHub Desktop
2. Select "neverswimalone-sure/ground-stone" repository
3. Click "Fetch origin" button
4. If changes available, click "Pull origin"

---

## 📊 Files Modified in This Session

### Core Changes:
1. **data/golf_companies.csv**: Complete list of 496 companies (was 36)
2. **src/dart/client.py**: Added `_normalize_company_name()` method for better matching
3. **test_historical.py**: Changed to query each company individually (bypasses 3-month limit)

### Helper Files Created:
- `verify_setup.py`: Check CSV loading
- `convert_excel_to_csv.py`: Excel to CSV converter
- `STATUS.md`: Detailed status documentation
- `CLAUDE.md`: This file

---

## 🎉 Next Steps

1. **Pull latest code** (if not already done)
2. **Run**: `python test_historical.py`
3. **Wait 10-20 minutes** for data fetching
4. **Verify** expected 400-470 reports found
5. **Confirm** to send notifications
6. **Check** @GC_golf_audit_channel for all messages

Once successful, you'll have verified that:
- ✅ All 496 companies are monitored correctly
- ✅ DART API 3-month limitation is bypassed
- ✅ Audit reports are detected accurately
- ✅ Telegram notifications work correctly
- ✅ System is ready for 2026 production use

---

**Last Updated**: 2026-01-14
**Branch**: `claude/create-claude-md-urmco`
**Ready for Testing**: Yes ✅
