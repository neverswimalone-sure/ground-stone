"""Check which companies didn't submit audit reports in 2025."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.dart.client import DARTClient
from src.database.models import init_database, SessionLocal
from src.database.operations import DatabaseService

def main():
    print("=" * 80)
    print("감사보고서 미제출 회사 분석")
    print("=" * 80)

    # Initialize
    dart_client = DARTClient()

    # Get all golf companies (DART matched)
    print("\n1. DART 매칭된 골프장 회사 로드 중...")
    golf_companies = dart_client.get_golf_companies()
    print(f"   ✅ DART 매칭: {len(golf_companies)}개 법인")

    # Get CSV companies
    print("\n2. CSV 원본 회사 로드 중...")
    csv_companies = dart_client.load_golf_companies_from_csv()
    print(f"   ✅ CSV 원본: {len(csv_companies)}개 회사")

    # Get companies that submitted reports in 2025
    print("\n3. 2025년 감사보고서 제출 회사 확인 중...")
    db = SessionLocal()
    db_service = DatabaseService(db)

    # Get all processed reports from database
    from src.database.models import ProcessedReport
    reports_2025 = db.query(ProcessedReport).filter(
        ProcessedReport.rcept_dt.like('2025%')
    ).all()

    # Extract company names that submitted reports
    submitted_companies = set()
    submitted_corp_codes = set()

    for report in reports_2025:
        submitted_corp_codes.add(report.corp_code)
        # Find company name from golf_companies
        if report.corp_code in golf_companies:
            company_info = golf_companies[report.corp_code]
            submitted_companies.add(company_info.get('공시회사명', ''))

    print(f"   ✅ 2025년 감사보고서 제출: {len(submitted_corp_codes)}개 법인 ({len(submitted_companies)}개 회사)")

    # Find companies that didn't submit
    print("\n4. 미제출 회사 분석 중...")

    # Check which DART-matched companies didn't submit
    not_submitted_dart = []
    for corp_code, company_info in golf_companies.items():
        if corp_code not in submitted_corp_codes:
            not_submitted_dart.append({
                'corp_code': corp_code,
                'corp_name': company_info.get('corp_name', ''),
                '공시회사명': company_info.get('공시회사명', ''),
                '사업자번호': company_info.get('사업자등록번호', '')
            })

    print(f"\n{'=' * 80}")
    print(f"📊 DART 매칭 법인 중 미제출: {len(not_submitted_dart)}개")
    print(f"{'=' * 80}\n")

    # Sort by company name
    not_submitted_dart.sort(key=lambda x: x['공시회사명'])

    # Print first 50
    print("🔍 미제출 회사 목록 (처음 50개):\n")
    for i, company in enumerate(not_submitted_dart[:50], 1):
        print(f"{i:3d}. {company['공시회사명']:30s} | DART명: {company['corp_name']:30s} | 사업자: {company['사업자번호']}")

    if len(not_submitted_dart) > 50:
        print(f"\n... 외 {len(not_submitted_dart) - 50}개 더")

    # Save full list to file
    output_file = Path(__file__).parent / "미제출_회사_목록.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("2025년 감사보고서 미제출 골프장 회사 목록\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"총 {len(not_submitted_dart)}개 법인\n\n")
        f.write("-" * 100 + "\n")

        for i, company in enumerate(not_submitted_dart, 1):
            f.write(f"{i:3d}. {company['공시회사명']:30s} | DART명: {company['corp_name']:30s} | 사업자: {company['사업자번호']}\n")

    print(f"\n✅ 전체 목록 저장: {output_file}")

    # Summary
    print(f"\n{'=' * 80}")
    print("📈 요약")
    print(f"{'=' * 80}")
    print(f"CSV 원본 회사:              {len(csv_companies):3d}개")
    print(f"DART 매칭 법인:             {len(golf_companies):3d}개")
    print(f"2025년 감사보고서 제출:     {len(submitted_corp_codes):3d}개")
    print(f"미제출:                     {len(not_submitted_dart):3d}개")
    print(f"제출률:                     {len(submitted_corp_codes)/len(golf_companies)*100:.1f}%")
    print(f"{'=' * 80}")

    db.close()

if __name__ == "__main__":
    main()
