"""
엑셀 파일에서 골프장 운영업 회사 목록을 로드하는 모듈
"""

import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
import logging

from .config import config

logger = logging.getLogger(__name__)


class CompanyData:
    """회사 데이터를 담는 클래스"""

    def __init__(self, corp_code: str, corp_name: str, business_number: Optional[str] = None):
        """
        Args:
            corp_code: DART 고유번호 (8자리)
            corp_name: 회사명
            business_number: 사업자등록번호
        """
        self.corp_code = corp_code
        self.corp_name = corp_name
        self.business_number = business_number

    def __repr__(self):
        return f"CompanyData(corp_code={self.corp_code}, corp_name={self.corp_name})"

    def to_dict(self) -> Dict[str, str]:
        """딕셔너리로 변환"""
        return {
            "corp_code": self.corp_code,
            "corp_name": self.corp_name,
            "business_number": self.business_number or ""
        }


class ExcelLoader:
    """엑셀 파일에서 회사 목록을 로드하는 클래스"""

    def __init__(self, file_path: Path = config.EXCEL_FILE_PATH):
        """
        Args:
            file_path: 엑셀 파일 경로
        """
        self.file_path = file_path
        self._df: Optional[pd.DataFrame] = None

    def load(self) -> pd.DataFrame:
        """엑셀 파일을 로드"""
        if self._df is None:
            logger.info(f"엑셀 파일 로딩 중: {self.file_path}")
            self._df = pd.read_excel(self.file_path, engine='openpyxl')
            logger.info(f"총 {len(self._df)}개 행 로드 완료")
            logger.info(f"컬럼 목록: {list(self._df.columns)}")
        return self._df

    def get_golf_companies(self) -> List[CompanyData]:
        """
        골프장 운영업 회사만 필터링하여 반환

        Returns:
            CompanyData 객체 리스트
        """
        df = self.load()

        # 엑셀 파일의 컬럼명을 기반으로 필터링
        # 일반적인 컬럼명: 업종명, 법인명, 고유번호, 사업자등록번호 등
        # 실제 컬럼명은 파일에 따라 다를 수 있으므로 유연하게 처리

        industry_col = self._find_column(df, ['업종명', '업종', '업태'])
        corp_name_col = self._find_column(df, ['법인명', '회사명', '상호', '기업명'])
        corp_code_col = self._find_column(df, ['고유번호', '법인등록번호', '기업코드'])
        business_num_col = self._find_column(df, ['사업자등록번호', '사업자번호'])

        if not industry_col:
            raise ValueError("업종명 컬럼을 찾을 수 없습니다.")
        if not corp_name_col:
            raise ValueError("회사명 컬럼을 찾을 수 없습니다.")
        if not corp_code_col:
            raise ValueError("고유번호 컬럼을 찾을 수 없습니다.")

        logger.info(f"사용할 컬럼 - 업종: {industry_col}, 회사명: {corp_name_col}, 고유번호: {corp_code_col}")

        # 골프장 운영업만 필터링
        filtered_df = df[df[industry_col] == config.TARGET_INDUSTRY].copy()
        logger.info(f"골프장 운영업 회사: {len(filtered_df)}개 발견")

        # CompanyData 객체 리스트로 변환
        companies = []
        for _, row in filtered_df.iterrows():
            corp_code = str(row[corp_code_col]).strip()
            corp_name = str(row[corp_name_col]).strip()
            business_number = str(row[business_num_col]).strip() if business_num_col else None

            # 고유번호가 8자리가 아니면 0으로 패딩
            if len(corp_code) < 8:
                corp_code = corp_code.zfill(8)

            companies.append(CompanyData(
                corp_code=corp_code,
                corp_name=corp_name,
                business_number=business_number
            ))

        logger.info(f"총 {len(companies)}개 회사 정보 추출 완료")
        return companies

    @staticmethod
    def _find_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
        """
        후보 컬럼명 중 실제 존재하는 컬럼명을 찾음

        Args:
            df: 데이터프레임
            candidates: 후보 컬럼명 리스트

        Returns:
            찾은 컬럼명 또는 None
        """
        for col in candidates:
            if col in df.columns:
                return col
        return None


def load_golf_companies() -> List[CompanyData]:
    """
    골프장 운영업 회사 목록을 로드하는 헬퍼 함수

    Returns:
        CompanyData 객체 리스트
    """
    loader = ExcelLoader()
    return loader.get_golf_companies()


if __name__ == "__main__":
    # 테스트 코드
    logging.basicConfig(level=logging.INFO)

    try:
        companies = load_golf_companies()
        print(f"\n총 {len(companies)}개 골프장 회사 발견")
        print("\n처음 5개 회사:")
        for company in companies[:5]:
            print(f"  - {company.corp_name} (코드: {company.corp_code})")
    except Exception as e:
        logger.error(f"에러 발생: {e}")
