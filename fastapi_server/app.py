import requests
import streamlit as st

st.title("FastAPI AI 호출 실습")

question = st.text_area("질문을 입력하세요")

if st.button("FastAPI에 질문하기"):
    if not question:
        st.write("질문을 입력하세요.")
    else:
        response = requests.post(
            "http://localhost:8000/api/ai/chat",
            json={
                "message": question
            }
        )

        result = response.json()

        st.subheader("AI 응답")
        st.write(result["data"]["answer"])