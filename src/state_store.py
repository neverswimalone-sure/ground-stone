"""
공시 알림 상태 저장 모듈
"""

import json
import logging
from typing import Set, List, Any
from pathlib import Path
from datetime import datetime

from .config import config

logger = logging.getLogger(__name__)


class StateStore:
    """공시 알림 상태를 관리하는 클래스"""

    def __init__(self, state_file: Path = config.STATE_FILE_PATH):
        """
        Args:
            state_file: 상태 저장 파일 경로
        """
        self.state_file = state_file
        self._sent_rcpnos: Set[str] = set()
        self._load()

    def _load(self) -> None:
        """상태 파일에서 데이터 로드"""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._sent_rcpnos = set(data.get("sent_rcpnos", []))
                    logger.info(f"상태 파일 로드 완료: {len(self._sent_rcpnos)}건의 이전 알림 기록")
            except Exception as e:
                logger.error(f"상태 파일 로드 실패: {e}")
                self._sent_rcpnos = set()
        else:
            logger.info("상태 파일이 없습니다. 새로 생성됩니다.")
            self._sent_rcpnos = set()

    def _save(self) -> None:
        """상태 파일에 데이터 저장"""
        try:
            data = {
                "sent_rcpnos": list(self._sent_rcpnos),
                "last_updated": datetime.now().isoformat(),
                "total_count": len(self._sent_rcpnos)
            }

            # 부모 디렉토리가 없으면 생성
            self.state_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"상태 파일 저장 완료: {len(self._sent_rcpnos)}건")
        except Exception as e:
            logger.error(f"상태 파일 저장 실패: {e}")

    def is_sent(self, rcept_no: str) -> bool:
        """
        해당 접수번호가 이미 알림 발송되었는지 확인

        Args:
            rcept_no: 접수번호

        Returns:
            이미 발송된 경우 True
        """
        return rcept_no in self._sent_rcpnos

    def mark_as_sent(self, rcept_no: str) -> None:
        """
        접수번호를 발송 완료로 표시

        Args:
            rcept_no: 접수번호
        """
        self._sent_rcpnos.add(rcept_no)
        self._save()

    def mark_multiple_as_sent(self, rcept_nos: List[str]) -> None:
        """
        여러 접수번호를 일괄 발송 완료로 표시

        Args:
            rcept_nos: 접수번호 리스트
        """
        self._sent_rcpnos.update(rcept_nos)
        self._save()

    def get_new_disclosures(self, all_disclosures: List[Any]) -> List[Any]:
        """
        전체 공시 목록에서 아직 알림을 보내지 않은 신규 공시만 필터링

        Args:
            all_disclosures: DartDisclosure 객체 리스트

        Returns:
            신규 공시 리스트
        """
        new_disclosures = [
            disclosure for disclosure in all_disclosures
            if not self.is_sent(disclosure.rcept_no)
        ]

        logger.info(f"전체 {len(all_disclosures)}건 중 신규 {len(new_disclosures)}건 발견")
        return new_disclosures

    def get_stats(self) -> dict:
        """
        상태 통계 반환

        Returns:
            통계 정보 딕셔너리
        """
        return {
            "total_sent": len(self._sent_rcpnos),
            "state_file": str(self.state_file),
            "file_exists": self.state_file.exists()
        }

    def reset(self) -> None:
        """상태 초기화 (주의: 모든 기록 삭제)"""
        logger.warning("상태 초기화 중...")
        self._sent_rcpnos = set()
        self._save()

    def __len__(self) -> int:
        """저장된 접수번호 개수"""
        return len(self._sent_rcpnos)

    def __contains__(self, rcept_no: str) -> bool:
        """in 연산자 지원"""
        return self.is_sent(rcept_no)


if __name__ == "__main__":
    # 테스트 코드
    logging.basicConfig(level=logging.INFO)

    store = StateStore()

    print(f"\n현재 상태:")
    stats = store.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # 테스트 데이터 추가
    test_rcpno = "20250000001"
    print(f"\n테스트 접수번호 추가: {test_rcpno}")
    store.mark_as_sent(test_rcpno)

    print(f"저장 확인: {test_rcpno in store}")
