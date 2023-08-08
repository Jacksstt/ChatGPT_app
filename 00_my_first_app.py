import streamlit as st
from gtts import gTTS
import openai
import os
from bs4 import BeautifulSoup
import requests

# OpenAIのAPIキーを設定
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_gpt3_response(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
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

# ユーザーからの入力を受け取る
user_input = st.text_input("あなたの質問を入力してください:")

if user_input:
    # ChatGPTからの応答を取得
    response = get_gpt3_response(user_input)
    
    # 応答を音声に変換
    tts = gTTS(text=response, lang='ja')
    tts.save("response.mp3")
    
    # 応答を表示と音声再生
    st.write(f"ChatGPT: {response}")
    st.audio("response.mp3")
    
    # DuckDuckGoから関連する画像を取得
    image_url = get_image_from_duckduckgo(user_input)
    if image_url:
        st.image(image_url, caption="関連画像", use_column_width=True)
