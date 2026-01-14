"""Verification script to check the current setup status."""
import csv
from pathlib import Path

print("=" * 80)
print("Ground Stone - Setup Verification")
print("=" * 80)

# Check CSV file
csv_path = Path("data/golf_companies.csv")

if not csv_path.exists():
    print("❌ CSV file not found!")
else:
    print(f"✅ CSV file found: {csv_path}")

    # Count lines
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"   Total lines: {len(lines)}")
        print(f"   Total companies: {len(lines) - 1} (excluding header)")

    # Check header
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        print(f"   Headers: {headers}")

    # Load and verify companies
    companies = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company_name = row.get('공시회사명', '').strip()
            if company_name:
                companies[company_name] = row

    print(f"   Successfully loaded: {len(companies)} companies")

    # Show sample companies
    print(f"\n📋 Sample companies (first 10):")
    for i, (name, info) in enumerate(list(companies.items())[:10], 1):
        business_no = info.get('사업자등록번호', 'N/A')
        full_name = info.get('회사이름', 'N/A')
        print(f"   {i:2d}. {name:20s} - {full_name:30s} - {business_no}")

print("\n" + "=" * 80)
print("📊 Status Summary")
print("=" * 80)
print(f"Current companies in CSV: {len(companies)}")
print(f"Expected companies: 471 (from your Excel file)")
print(f"Missing companies: {471 - len(companies)}")

if len(companies) < 471:
    print("\n⚠️  IMPORTANT:")
    print("   The CSV file only has 36 companies instead of 471.")
    print("   To fix this:")
    print("   1. Open your Excel file with 471 companies")
    print("   2. Save it as CSV (UTF-8) format")
    print("   3. Make sure only these 3 columns are included:")
    print("      - 회사이름")
    print("      - 공시회사명")
    print("      - 사업자등록번호")
    print("   4. Save the file to: data/golf_companies.csv")
    print("   5. Commit and push the updated file")
else:
    print("\n✅ All companies loaded successfully!")

print("=" * 80)
