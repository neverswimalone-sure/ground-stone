"""
Helper script to convert Excel file to CSV format.

This script helps convert your Excel file with golf companies to the required CSV format.

Prerequisites:
    pip install openpyxl pandas

Usage:
    python convert_excel_to_csv.py input.xlsx

The script will:
1. Read the Excel file
2. Select only the required columns (회사이름, 공시회사명, 사업자등록번호)
3. Save as UTF-8 CSV to data/golf_companies.csv
4. Display statistics
"""

import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("❌ Error: pandas not installed")
    print("   Please run: pip install pandas openpyxl")
    sys.exit(1)

def convert_excel_to_csv(excel_path: str):
    """Convert Excel file to CSV format."""

    excel_file = Path(excel_path)
    if not excel_file.exists():
        print(f"❌ Error: File not found: {excel_path}")
        sys.exit(1)

    print("=" * 80)
    print("Excel to CSV Converter - Golf Companies")
    print("=" * 80)
    print(f"Input file: {excel_path}")

    # Read Excel file
    print("\n📖 Reading Excel file...")
    try:
        df = pd.read_excel(excel_path)
        print(f"   ✅ Loaded {len(df)} rows")
        print(f"   Columns found: {list(df.columns)}")
    except Exception as e:
        print(f"   ❌ Error reading Excel: {e}")
        sys.exit(1)

    # Check required columns
    required_columns = ['회사이름', '공시회사명', '사업자등록번호']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"\n❌ Error: Missing required columns: {missing_columns}")
        print(f"   Available columns: {list(df.columns)}")
        sys.exit(1)

    # Select only required columns
    print(f"\n📋 Selecting required columns...")
    df_filtered = df[required_columns].copy()

    # Remove rows with empty 공시회사명
    original_count = len(df_filtered)
    df_filtered = df_filtered[df_filtered['공시회사명'].notna()]
    df_filtered = df_filtered[df_filtered['공시회사명'].str.strip() != '']
    removed_count = original_count - len(df_filtered)

    if removed_count > 0:
        print(f"   ⚠️  Removed {removed_count} rows with empty 공시회사명")

    print(f"   ✅ Final count: {len(df_filtered)} companies")

    # Show sample data
    print(f"\n📊 Sample data (first 5 rows):")
    for i, row in df_filtered.head().iterrows():
        print(f"   {i+1}. {row['공시회사명']:20s} - {row['회사이름']:30s} - {row['사업자등록번호']}")

    # Save to CSV
    output_path = Path("data/golf_companies.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n💾 Saving to CSV...")
    print(f"   Output: {output_path}")

    try:
        df_filtered.to_csv(
            output_path,
            index=False,
            encoding='utf-8',
            lineterminator='\n'
        )
        print(f"   ✅ Saved successfully!")
    except Exception as e:
        print(f"   ❌ Error saving CSV: {e}")
        sys.exit(1)

    # Verify the saved file
    print(f"\n🔍 Verifying saved file...")
    with open(output_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"   Total lines: {len(lines)} (including header)")
        print(f"   Total companies: {len(lines) - 1}")

    print("\n" + "=" * 80)
    print("✅ Conversion completed successfully!")
    print("=" * 80)
    print(f"Companies: {len(df_filtered)}")
    print(f"Output: {output_path}")
    print(f"\nNext steps:")
    print(f"1. Run: python verify_setup.py")
    print(f"2. Commit: git add data/golf_companies.csv")
    print(f"3. Push: git commit -m 'Add complete golf companies list'")
    print("=" * 80)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_excel_to_csv.py <excel_file>")
        print("Example: python convert_excel_to_csv.py golf_companies.xlsx")
        sys.exit(1)

    excel_path = sys.argv[1]
    convert_excel_to_csv(excel_path)
