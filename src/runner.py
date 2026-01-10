"""
DART 골프장 감사보고서 모니터링 메인 실행 모듈
"""

import logging
import sys
from typing import List
from datetime import datetime

from .config import config
from .excel_loader import load_golf_companies
from .dart_client import DartAPIClient, DartDisclosure
from .telegram_client import TelegramClient
from .state_store import StateStore

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('dart_monitoring.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


class DartMonitoringRunner:
    """DART 모니터링 실행 클래스"""

    def __init__(self):
        """초기화"""
        self.dart_client = DartAPIClient()
        self.telegram_client = TelegramClient()
        self.state_store = StateStore()

    def run_once(self) -> dict:
        """
        모니터링을 한 번 실행

        Returns:
            실행 결과 통계
        """
        logger.info("=" * 60)
        logger.info("DART 골프장 감사보고서 모니터링 시작")
        logger.info("=" * 60)

        stats = {
            "start_time": datetime.now(),
            "total_companies": 0,
            "total_disclosures": 0,
            "new_disclosures": 0,
            "notifications_sent": 0,
            "errors": 0
        }

        try:
            # 1. 환경 변수 검증
            logger.info("1. 환경 변수 검증 중...")
            config.validate()
            logger.info("   ✅ 환경 변수 검증 완료")

            # 2. 골프장 회사 목록 로드
            logger.info("2. 골프장 회사 목록 로드 중...")
            companies = load_golf_companies()
            stats["total_companies"] = len(companies)
            logger.info(f"   ✅ {len(companies)}개 회사 로드 완료")

            if not companies:
                logger.warning("   ⚠️  모니터링 대상 회사가 없습니다.")
                return stats

            # 3. DART API로 감사보고서 조회
            logger.info(f"3. {config.TARGET_YEAR}년 감사보고서 조회 중...")
            all_audit_reports = self.dart_client.get_all_companies_audit_reports(
                companies,
                year=config.TARGET_YEAR
            )
            stats["total_disclosures"] = len(all_audit_reports)
            logger.info(f"   ✅ 총 {len(all_audit_reports)}건 감사보고서 발견")

            if not all_audit_reports:
                logger.info("   ℹ️  발견된 감사보고서가 없습니다.")
                self._send_summary_notification(stats["total_companies"], 0, [])
                return stats

            # 4. 신규 공시 필터링
            logger.info("4. 신규 공시 필터링 중...")
            new_reports = self.state_store.get_new_disclosures(all_audit_reports)
            stats["new_disclosures"] = len(new_reports)
            logger.info(f"   ✅ {len(new_reports)}건의 신규 감사보고서 발견")

            if not new_reports:
                logger.info("   ℹ️  새로운 감사보고서가 없습니다.")
                self._send_summary_notification(stats["total_companies"], 0, [])
                return stats

            # 5. 텔레그램 알림 발송
            logger.info("5. 텔레그램 알림 발송 중...")
            for idx, report in enumerate(new_reports, 1):
                logger.info(f"   [{idx}/{len(new_reports)}] {report.corp_name} - {report.report_nm}")

                try:
                    if self.telegram_client.send_audit_report_notification(report):
                        # 발송 성공 시 상태 저장
                        self.state_store.mark_as_sent(report.rcept_no)
                        stats["notifications_sent"] += 1
                        logger.info(f"      ✅ 알림 발송 완료")
                    else:
                        logger.error(f"      ❌ 알림 발송 실패")
                        stats["errors"] += 1

                except Exception as e:
                    logger.error(f"      ❌ 알림 발송 중 에러: {e}")
                    stats["errors"] += 1

            # 6. 요약 알림 발송
            logger.info("6. 요약 알림 발송 중...")
            self._send_summary_notification(
                stats["total_companies"],
                stats["notifications_sent"],
                new_reports
            )

        except FileNotFoundError as e:
            logger.error(f"❌ 파일을 찾을 수 없습니다: {e}")
            stats["errors"] += 1
            return stats

        except ValueError as e:
            logger.error(f"❌ 설정 오류: {e}")
            stats["errors"] += 1
            return stats

        except Exception as e:
            logger.error(f"❌ 예상치 못한 에러 발생: {e}", exc_info=True)
            stats["errors"] += 1
            return stats

        finally:
            stats["end_time"] = datetime.now()
            stats["duration"] = (stats["end_time"] - stats["start_time"]).total_seconds()

            # 실행 결과 로그
            logger.info("=" * 60)
            logger.info("모니터링 실행 완료")
            logger.info(f"  • 모니터링 회사: {stats['total_companies']}개")
            logger.info(f"  • 발견된 감사보고서: {stats['total_disclosures']}건")
            logger.info(f"  • 신규 감사보고서: {stats['new_disclosures']}건")
            logger.info(f"  • 알림 발송: {stats['notifications_sent']}건")
            logger.info(f"  • 에러: {stats['errors']}건")
            logger.info(f"  • 소요 시간: {stats['duration']:.2f}초")
            logger.info("=" * 60)

        return stats

    def _send_summary_notification(
        self,
        total_companies: int,
        new_reports_count: int,
        reports: List[DartDisclosure]
    ) -> None:
        """요약 알림 발송"""
        try:
            self.telegram_client.send_summary_notification(
                total_companies,
                new_reports_count,
                reports
            )
        except Exception as e:
            logger.error(f"요약 알림 발송 실패: {e}")

    def test_setup(self) -> bool:
        """
        설정 및 연결 테스트

        Returns:
            모든 테스트 통과 여부
        """
        logger.info("=" * 60)
        logger.info("설정 테스트 시작")
        logger.info("=" * 60)

        all_passed = True

        # 1. 환경 변수 검증
        logger.info("1. 환경 변수 검증...")
        try:
            config.validate()
            logger.info("   ✅ 환경 변수 검증 완료")
        except Exception as e:
            logger.error(f"   ❌ 환경 변수 검증 실패: {e}")
            all_passed = False

        # 2. 엑셀 파일 읽기 테스트
        logger.info("2. 엑셀 파일 읽기 테스트...")
        try:
            companies = load_golf_companies()
            logger.info(f"   ✅ {len(companies)}개 회사 로드 성공")
        except Exception as e:
            logger.error(f"   ❌ 엑셀 파일 읽기 실패: {e}")
            all_passed = False

        # 3. 텔레그램 연결 테스트
        logger.info("3. 텔레그램 연결 테스트...")
        try:
            if self.telegram_client.test_connection():
                logger.info("   ✅ 텔레그램 연결 성공")
            else:
                logger.error("   ❌ 텔레그램 연결 실패")
                all_passed = False
        except Exception as e:
            logger.error(f"   ❌ 텔레그램 연결 실패: {e}")
            all_passed = False

        # 4. 상태 저장소 테스트
        logger.info("4. 상태 저장소 테스트...")
        try:
            stats = self.state_store.get_stats()
            logger.info(f"   ✅ 상태 저장소 정상 (저장된 기록: {stats['total_sent']}건)")
        except Exception as e:
            logger.error(f"   ❌ 상태 저장소 테스트 실패: {e}")
            all_passed = False

        logger.info("=" * 60)
        if all_passed:
            logger.info("✅ 모든 테스트 통과!")
        else:
            logger.error("❌ 일부 테스트 실패")
        logger.info("=" * 60)

        return all_passed


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description="DART 골프장 감사보고서 모니터링 봇")
    parser.add_argument(
        "--test",
        action="store_true",
        help="설정 및 연결 테스트만 실행"
    )
    parser.add_argument(
        "--reset-state",
        action="store_true",
        help="상태 초기화 (모든 알림 기록 삭제)"
    )

    args = parser.parse_args()

    runner = DartMonitoringRunner()

    # 상태 초기화
    if args.reset_state:
        logger.warning("⚠️  상태 초기화를 실행합니다. 모든 알림 기록이 삭제됩니다.")
        response = input("계속하시겠습니까? (yes/no): ")
        if response.lower() == "yes":
            runner.state_store.reset()
            logger.info("✅ 상태 초기화 완료")
        else:
            logger.info("ℹ️  취소되었습니다.")
        return

    # 테스트 모드
    if args.test:
        runner.test_setup()
        return

    # 정상 실행
    runner.run_once()


if __name__ == "__main__":
    main()
