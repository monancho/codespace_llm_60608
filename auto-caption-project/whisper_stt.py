import os
from dotenv import load_dotenv
from openai import OpenAI

# 1) .env 파일 로드
load_dotenv()

# 2) 환경 변수 확인
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# 3) OpenAI 클라이언트 생성
#    OPENAI_API_KEY 환경 변수를 자동으로 사용합니다.
client = OpenAI()

def transcribe_audio(audio_path: str) -> str:
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return transcript
