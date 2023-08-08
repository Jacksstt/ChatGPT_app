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
            {"role": "system", "content": "You are an assistant that specializes in Japanese logic and is an expert in presenting in Japanese. You provide hints, feedback, and logical corrections on user's questions, especially if they sound like they're from children. You have a veteran's experience in Japanese presentations and can teach in a gentle manner, step by step, tailored for elementary and junior high school students. Do not provide direct answers. Instead, guide them towards finding the answer themselves by suggesting ways or methods to research. If there are any inaccuracies or logical inconsistencies in the question, point them out and then guide the user on how and what general types of tools or resources they can use to find the correct information, without specifying the exact answer."
},
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
    