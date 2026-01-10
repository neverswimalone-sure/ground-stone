"""
DART API 클라이언트 모듈
"""

import requests
import time
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, date
from dataclasses import dataclass

from .config import config

logger = logging.getLogger(__name__)


@dataclass
class DartDisclosure:
    """DART 공시 정보를 담는 클래스"""
    corp_code: str          # 고유번호
    corp_name: str          # 회사명
    stock_code: str         # 종목코드
    report_nm: str          # 보고서명
    rcept_no: str           # 접수번호
    flr_nm: str             # 공시 제출인명
    rcept_dt: str           # 접수일자 (YYYYMMDD)
    rm: str                 # 비고

    @property
    def detail_url(self) -> str:
        """공시 상세 URL"""
        return f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={self.rcept_no}"

    @property
    def is_audit_report(self) -> bool:
        """감사보고서 여부 확인"""
        audit_keywords = ["감사보고서", "사업보고서"]
        return any(keyword in self.report_nm for keyword in audit_keywords)

    def __repr__(self):
        return f"DartDisclosure(corp_name={self.corp_name}, report_nm={self.report_nm}, rcept_dt={self.rcept_dt})"


class DartAPIClient:
    """DART API 클라이언트 클래스"""

    def __init__(self, api_key: str = config.DART_API_KEY):
        """
        Args:
            api_key: DART API 인증키
        """
        self.api_key = api_key
        self.base_url = config.DART_API_BASE_URL
        self.session = requests.Session()

    def get_disclosures(
        self,
        corp_code: str,
        bgn_de: str,
        end_de: str,
        page_no: int = 1,
        page_count: int = 100
    ) -> List[DartDisclosure]:
        """
        기업의 공시 목록 조회

        Args:
            corp_code: 기업 고유번호 (8자리)
            bgn_de: 시작일자 (YYYYMMDD)
            end_de: 종료일자 (YYYYMMDD)
            page_no: 페이지 번호
            page_count: 페이지당 건수 (최대 100)

        Returns:
            공시 목록
        """
        url = f"{self.base_url}/list.json"
        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
            "page_no": page_no,
            "page_count": page_count,
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # API 응답 상태 확인
            if data.get("status") != "000":
                error_message = data.get("message", "Unknown error")
                if data.get("status") == "013":  # 조회된 데이터 없음
                    logger.debug(f"조회된 데이터 없음: {corp_code}")
                    return []
                logger.warning(f"DART API 에러 (코드: {data.get('status')}): {error_message}")
                return []

            # 공시 목록 파싱
            disclosures = []
            if "list" in data and data["list"]:
                for item in data["list"]:
                    disclosure = DartDisclosure(
                        corp_code=item.get("corp_code", ""),
                        corp_name=item.get("corp_name", ""),
                        stock_code=item.get("stock_code", ""),
                        report_nm=item.get("report_nm", ""),
                        rcept_no=item.get("rcept_no", ""),
                        flr_nm=item.get("flr_nm", ""),
                        rcept_dt=item.get("rcept_dt", ""),
                        rm=item.get("rm", ""),
                    )
                    disclosures.append(disclosure)

            logger.debug(f"{corp_code}: {len(disclosures)}건 공시 조회")
            return disclosures

        except requests.RequestException as e:
            logger.error(f"DART API 호출 실패 ({corp_code}): {e}")
            return []

    def get_audit_reports(
        self,
        corp_code: str,
        year: int = config.TARGET_YEAR
    ) -> List[DartDisclosure]:
        """
        특정 연도의 감사보고서만 조회

        Args:
            corp_code: 기업 고유번호
            year: 조회 연도

        Returns:
            감사보고서 목록
        """
        bgn_de = f"{year}0101"
        end_de = f"{year}1231"

        all_disclosures = self.get_disclosures(corp_code, bgn_de, end_de)

        # 감사보고서만 필터링
        audit_reports = [d for d in all_disclosures if d.is_audit_report]

        if audit_reports:
            logger.info(f"{corp_code}: {year}년 감사보고서 {len(audit_reports)}건 발견")

        return audit_reports

    def get_all_companies_audit_reports(
        self,
        companies: List[Any],
        year: int = config.TARGET_YEAR
    ) -> List[DartDisclosure]:
        """
        여러 회사의 감사보고서를 일괄 조회

        Args:
            companies: CompanyData 객체 리스트
            year: 조회 연도

        Returns:
            전체 감사보고서 목록
        """
        all_audit_reports = []

        logger.info(f"총 {len(companies)}개 회사의 {year}년 감사보고서 조회 시작")

        for idx, company in enumerate(companies, 1):
            logger.info(f"[{idx}/{len(companies)}] {company.corp_name} 조회 중...")

            audit_reports = self.get_audit_reports(company.corp_code, year)
            all_audit_reports.extend(audit_reports)

            # API Rate Limit 방지를 위한 딜레이
            if idx < len(companies):
                time.sleep(config.API_DELAY)

        logger.info(f"조회 완료: 총 {len(all_audit_reports)}건의 감사보고서 발견")
        return all_audit_reports


if __name__ == "__main__":
    # 테스트 코드
    logging.basicConfig(level=logging.INFO)

    client = DartAPIClient()

    # 테스트: 삼성전자(00126380)의 2025년 공시 조회
    test_corp_code = "00126380"
    disclosures = client.get_disclosures(test_corp_code, "20250101", "20251231")

    print(f"\n조회된 공시: {len(disclosures)}건")
    for disc in disclosures[:5]:
        print(f"  - {disc.report_nm} ({disc.rcept_dt})")
