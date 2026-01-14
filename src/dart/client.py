"""DART Open API client for fetching corporate disclosures."""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
import zipfile
import io
import xml.etree.ElementTree as ET
from config.settings import DART_API_KEY, DART_BASE_URL, INDUSTRY_CODE

logger = logging.getLogger(__name__)


class DARTClient:
    """Client for interacting with DART Open API."""

    def __init__(self, api_key: str = DART_API_KEY):
        """Initialize DART client with API key."""
        self.api_key = api_key
        self.base_url = DART_BASE_URL
        self.session = requests.Session()
        self.golf_companies = {}  # Cache for golf course companies

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

    def get_golf_companies(self) -> Dict[str, Dict]:
        """
        Get list of golf course operation companies from DART.
        Downloads corpCode.xml and filters by industry.

        Returns:
            Dictionary mapping corp_code to company info
        """
        if self.golf_companies:
            # Return cached result
            return self.golf_companies

        logger.info("Downloading company list from DART...")

        url = f"{self.base_url}/corpCode.xml"
        params = {"crtfc_key": self.api_key}

        try:
            response = self.session.get(url, params=params, timeout=60)
            response.raise_for_status()

            # Extract ZIP file
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                xml_content = z.read('CORPCODE.xml')

            # Parse XML
            root = ET.fromstring(xml_content)

            golf_companies = {}
            total_companies = 0

            # Find companies with golf course industry
            for company in root.findall('.//list'):
                total_companies += 1
                corp_name = company.find('corp_name')
                corp_code = company.find('corp_code')
                stock_code = company.find('stock_code')
                induty_code = company.find('induty_code')  # Note: DART uses 'induty' not 'industry'

                if all([corp_name is not None, corp_code is not None, induty_code is not None]):
                    # Check if industry code contains golf course operation
                    # DART uses multiple formats: "91221", "골프장 운영업", etc.
                    induty_text = induty_code.text or ""

                    if ("91221" in induty_text or
                        "골프" in induty_text or
                        "golf" in induty_text.lower()):

                        golf_companies[corp_code.text] = {
                            "corp_name": corp_name.text,
                            "corp_code": corp_code.text,
                            "stock_code": stock_code.text if stock_code is not None else "",
                            "induty_code": induty_text
                        }

            logger.info(f"Found {len(golf_companies)} golf course companies out of {total_companies} total")
            logger.info(f"Golf companies: {list(golf_companies.values())[:5]}")  # Log first 5

            self.golf_companies = golf_companies
            return golf_companies

        except Exception as e:
            logger.error(f"Failed to download company list: {e}")
            return {}

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
        Get recent audit reports from golf course companies only.

        Args:
            days: Number of days to look back

        Returns:
            List of audit report disclosures from golf course companies
        """
        # First, get list of golf course companies
        golf_companies = self.get_golf_companies()

        if not golf_companies:
            logger.warning("No golf course companies found!")
            return []

        logger.info(f"Monitoring {len(golf_companies)} golf course companies")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")

        logger.info(f"Fetching disclosures from {start_str} to {end_str}")

        result = self.get_disclosure_list(start_str, end_str)
        disclosures = result.get("list", [])

        # Filter for audit reports only
        audit_reports = self.filter_audit_reports(disclosures)

        # Filter for golf course companies only
        golf_audit_reports = []
        for report in audit_reports:
            corp_code = report.get("corp_code")
            if corp_code in golf_companies:
                # Add company info to report
                report["induty_code"] = golf_companies[corp_code].get("induty_code", "")
                golf_audit_reports.append(report)
                logger.info(f"Found golf course audit report: {report.get('corp_name')} - {golf_companies[corp_code].get('induty_code')}")

        logger.info(f"Found {len(golf_audit_reports)} audit reports from golf course companies (out of {len(audit_reports)} total)")
        return golf_audit_reports

    def get_document_url(self, rcept_no: str) -> str:
        """
        Generate URL to view the document on DART.

        Args:
            rcept_no: Receipt number of the disclosure

        Returns:
            URL string
        """
        return f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"
