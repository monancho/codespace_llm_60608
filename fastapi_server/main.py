import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

# 실습용 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

cars = [
    {"id": 1, "name": "Sonata", "company": "HYUNDAI", "price": 2500, "year": 2023},
    {"id": 2, "name": "Avante", "company": "HYUNDAI", "price": 2200, "year": 2024},
    {"id": 3, "name": "K5", "company": "KIA", "price": 2900, "year": 2023},
]


class CarCreate(BaseModel):
    name: str
    company: str
    price: int
    year: int


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "FastAPI 서버 실행 중"
    }


@app.get("/cars")
def get_cars():
    return {
        "message": "자동차 목록 조회 성공",
        "data": cars
    }


@app.get("/cars/{car_id}")
def get_car(car_id: int):
    for car in cars:
        if car["id"] == car_id:
            return {
                "message": "자동차 상세 조회 성공",
                "data": car
            }

    return {
        "message": "해당 자동차를 찾을 수 없습니다.",
        "data": None
    }


@app.post("/cars")
def create_car(car: CarCreate):
    new_car = {
        "id": len(cars) + 1,
        "name": car.name,
        "company": car.company,
        "price": car.price,
        "year": car.year
    }

    cars.append(new_car)

    return {
        "message": "자동차 등록 성공",
        "data": new_car
    }


@app.post("/api/ai/chat")
def ai_chat(request: ChatRequest):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=request.message
    )

    return {
        "message": "AI 응답 생성 성공",
        "data": {
            "question": request.message,
            "answer": response.output_text
        }
    }