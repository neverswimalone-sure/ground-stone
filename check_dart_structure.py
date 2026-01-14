"""Check DART corpCode.xml structure to find business registration number field."""
import requests
import zipfile
import io
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os

load_dotenv()

DART_API_KEY = os.getenv("DART_API_KEY")

print("Downloading DART corpCode.xml...")
url = "https://opendart.fss.or.kr/api/corpCode.xml"
params = {"crtfc_key": DART_API_KEY}

response = requests.get(url, params=params, timeout=60)
response.raise_for_status()

# Extract ZIP file
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    xml_content = z.read('CORPCODE.xml')

# Parse XML
root = ET.fromstring(xml_content)

# Check structure of first 5 companies
print("\n" + "="*80)
print("First 5 companies structure:")
print("="*80)

for i, company in enumerate(list(root.findall('.//list'))[:5], 1):
    print(f"\nCompany {i}:")
    print("-" * 40)
    for elem in company:
        value = elem.text if elem.text else ""
        if len(value) < 200:  # Only show short values
            print(f"  {elem.tag}: {value}")

# Search for companies with specific keywords
print("\n" + "="*80)
print("Searching for golf-related companies...")
print("="*80)

golf_companies = []
for company in root.findall('.//list'):
    corp_name = company.find('corp_name')
    if corp_name is not None:
        name = corp_name.text or ""
        if "골프" in name or "컨트리" in name or "cc" in name.lower():
            golf_companies.append(company)
            if len(golf_companies) <= 10:
                print(f"\n{len(golf_companies)}. {name}")
                for elem in company:
                    if elem.text and len(elem.text) < 100:
                        print(f"   {elem.tag}: {elem.text}")

print(f"\n\nTotal golf-related companies found: {len(golf_companies)}")
