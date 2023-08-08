import streamlit as st
from gtts import gTTS
import openai
import os
from bs4 import BeautifulSoup
import requests

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_gpt3_response(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are an assistant that specializes in Japanese logic and is an expert in presenting in Japanese.Please point out only the mistakes in Japanese logical expressions, such as conjunctions, particles, sequential expressions, and paradoxical expressions."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# CSS for the chat bubbles
chat_style = """
<style>
    .chat-bubble {
        padding: 10px;
        border-radius: 15px;
        margin: 5px 0;
    }
    .user {
        background-color: #e1ffc7;
        align-self: flex-start;
    }
    .chatgpt {
        background-color: #c7c7ff;
        align-self: flex-end;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        width: 50%;
        margin: auto;
    }
</style>
"""

st.markdown(chat_style, unsafe_allow_html=True)

st.title('ChatGPTとの音声会話')

# 会話の履歴を保存するリスト
conversation_history = []

user_input = st.text_input("あなたの質問を入力してください:")

if user_input:
    response = get_gpt3_response(user_input)
    
        # ユーザーの質問とChatGPTの応答を履歴に追加
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "ChatGPT", "content": response})

    tts = gTTS(text=response, lang='ja')
    tts.save("response.mp3")

    # 会話の履歴を表示
    with st.markdown('<div class="chat-container">', unsafe_allow_html=True):
        for item in conversation_history:
            if item["role"] == "user":
                st.markdown(f'<div class="chat-bubble user">{item["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble chatgpt">{item["content"]}</div>', unsafe_allow_html=True)
    
    st.write(f"ChatGPT: {response}")
    st.audio("response.mp3")
    