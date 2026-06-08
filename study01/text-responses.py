from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

load_dotenv()
client = OpenAI()

class VulnerabilityReport(BaseModel):
    title: str
    severity: str
    vulnerability_type: str
    target: str
    description: str
    affected_parameter: str
    proof_of_concept: str
    impact: str
    remediation: List[str]

raw_data = """
대상: https://test.example.com
발견 내용:
- 로그인 페이지에서 SQL Injection 의심
- 파라미터: user_id
- payload: ' OR 1=1 --
- 관리자 계정 정보 노출 가능
- 재현 성공
"""

response = client.responses.parse(
    model="gpt-5.4-mini",
    input=[
        {
            "role": "system",
            "content": """
당신은 침투테스트 보고서 작성 전문가입니다.
사용자가 제공한 취약점 정보를 분석해 정형화된 취약점 보고서를 작성하세요.
severity는 반드시 다음 중 하나를 사용하세요:
Critical, High, Medium, Low, Informational
""",
        },
        {
            "role": "user",
            "content": raw_data,
        },
    ],
    text_format=VulnerabilityReport,
)

report = response.output_parsed

from pathlib import Path
from datetime import datetime

markdown = f"""
# 취약점 보고서

## 1. 기본 정보

| 항목 | 내용 |
|------|------|
| 취약점명 | {report.title} |
| 위험도 | {report.severity} |
| 취약점 유형 | {report.vulnerability_type} |
| 대상 시스템 | {report.target} |

---

## 2. 취약점 설명

{report.description}

---

## 3. 영향받는 파라미터

{report.affected_parameter}

---

## 4. 재현 코드(PoC)

{report.proof_of_concept}

---

## 5. 영향도

{report.impact}

---

## 6. 조치 방안

"""

for item in report.remediation:
    markdown += f"- {item}\n"

output_dir = Path("./output")
output_dir.mkdir(parents=True, exist_ok=True)

report_date = datetime.now().strftime("%Y%m%d")
filename = output_dir / f"vulnerability_report_{report_date}.md"

with open(filename, "w", encoding="utf-8") as file:
    file.write(markdown)

print(f"보고서 생성 완료 >>> {filename}")

print(report.model_dump_json(indent=2))