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

def get_image_from_duckduckgo(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://duckduckgo.com/?q={query}&t=h_&iax=images&ia=images"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    img_tag = soup.find("img", {"class": "tile--img__img"})
    return img_tag["src"] if img_tag else None

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
    for item in conversation_history:
        if item["role"] == "user":
            st.write(f"あなた: {item['content']}")
        else:
            st.write(f"ChatGPT: {item['content']}")
    
    st.write(f"ChatGPT: {response}")
    st.audio("response.mp3")
    