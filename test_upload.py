# 이건 나중에 회사 코드에 붙여넣을 연습용 코드입니다.
# 지금은 가짜 데이터를 DB로 쏴보는 역할만 합니다.

import json
from datetime import datetime

# 가상의 골프장 데이터 (회사 코드에서는 DART에서 긁어온 데이터가 되겠죠?)
fake_data = {
    "company_name": "테스트CC",
    "report_name": "감사보고서 (2024.12)",
    "rcept_no": "12345678", # 가짜 접수번호
    "submission_date": datetime.now().strftime("%Y-%m-%d"),
    "industry": "골프장 운영업",
    "memo": "이 데이터가 보이면 연결 성공입니다!"
}

print("데이터 전송 준비 끝:", fake_data)
print("이제 Supabase(DB) 주소만 있으면 전송할 수 있습니다.")