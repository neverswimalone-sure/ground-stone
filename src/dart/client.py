"""DART Open API client for fetching corporate disclosures."""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from config.settings import DART_API_KEY, DART_BASE_URL, INDUSTRY_CODE

logger = logging.getLogger(__name__)


class DARTClient:
    """Client for interacting with DART Open API."""

    def __init__(self, api_key: str = DART_API_KEY):
        """Initialize DART client with API key."""
        self.api_key = api_key
        self.base_url = DART_BASE_URL
        self.session = requests.Session()

    def get_disclosure_list(
        self,
        start_date: str,
        end_date: str,
        corp_code: Optional[str] = None,
        page_no: int = 1,
        page_count: int = 100
    ) -> Dict:
        """
        Get list of disclosures from DART.

        Args:
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            corp_code: Optional corporation code
            page_no: Page number
            page_count: Number of items per page (max 100)

        Returns:
            Dictionary containing disclosure information
        """
        url = f"{self.base_url}/list.json"
        params = {
            "crtfc_key": self.api_key,
            "bgn_de": start_date,
            "end_de": end_date,
            "page_no": page_no,
            "page_count": page_count
        }

        if corp_code:
            params["corp_code"] = corp_code

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "000":
                logger.error(f"DART API error: {data.get('message')}")
                return {"status": "error", "list": []}

            return data

        except requests.RequestException as e:
            logger.error(f"Failed to fetch disclosures: {e}")
            return {"status": "error", "list": []}

    def get_company_info(self, corp_code: str) -> Dict:
        """
        Get company information.

        Args:
            corp_code: Corporation code

        Returns:
            Dictionary containing company information
        """
        url = f"{self.base_url}/company.json"
        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "000":
                logger.error(f"DART API error: {data.get('message')}")
                return {}

            return data

        except requests.RequestException as e:
            logger.error(f"Failed to fetch company info: {e}")
            return {}

    def filter_audit_reports(self, disclosures: List[Dict]) -> List[Dict]:
        """
        Filter disclosures to get only audit reports.

        Args:
            disclosures: List of disclosure dictionaries

        Returns:
            Filtered list containing only audit reports
        """
        audit_keywords = ["감사보고서", "audit"]
        filtered = []

        for disclosure in disclosures:
            report_nm = disclosure.get("report_nm", "").lower()
            if any(keyword in report_nm for keyword in audit_keywords):
                filtered.append(disclosure)

        return filtered

    def get_recent_audit_reports(self, days: int = 1) -> List[Dict]:
        """
        Get recent audit reports from the last N days.

        Args:
            days: Number of days to look back

        Returns:
            List of audit report disclosures
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")

        logger.info(f"Fetching disclosures from {start_str} to {end_str}")

        result = self.get_disclosure_list(start_str, end_str)
        disclosures = result.get("list", [])

        # Filter for audit reports only
        audit_reports = self.filter_audit_reports(disclosures)

        logger.info(f"Found {len(audit_reports)} audit reports")
        return audit_reports

    def get_document_url(self, rcept_no: str) -> str:
        """
        Generate URL to view the document on DART.

        Args:
            rcept_no: Receipt number of the disclosure

        Returns:
            URL string
        """
        return f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"
