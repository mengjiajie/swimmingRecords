import streamlit as st
from openai import OpenAI

st.title("多模态 简单chatBot 应用")
st.header("欢迎来到多模态 聊天机器人")
question = st.chat_input("请输入你的问题：")

client  = OpenAI()

def send_question(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个智能聊天机器人"},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content

if question:
    st.write("用户：", question)
    st.write("机器人：", "正在思考...") 
    st.write("机器人：", "我正在思考...")
    response = send_question(question);
    st.write("机器人：", response)

