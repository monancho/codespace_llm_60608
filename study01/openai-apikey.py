from dotenv import load_dotenv
import os

# .env 파일 내용을 환경변수로 등록한다.
load_dotenv()

# API Key가 정상적으로 등록되었는지 일부만 출력한다.
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    print("OPENAI_API_KEY가 설정되지 않았습니다.")
else:
    print(f"OpenAI API Key: {api_key[:20]}{'*' * 30}")