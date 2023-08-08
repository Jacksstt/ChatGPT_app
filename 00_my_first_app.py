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
            {"role": "system", "content": "You are an assistant that provides hints and feedback on user's questions, especially if they sound like they're from children. Do not provide direct answers. Instead, guide them towards finding the answer themselves by suggesting ways or methods to research. If there are any inaccuracies in the question, point them out and then guide the user on how and what general types of tools or resources they can use to find the correct information, without specifying the exact answer."},
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

user_input = st.text_input("あなたの質問を入力してください:")

if user_input:
    response = get_gpt3_response(user_input)
    
    tts = gTTS(text=response, lang='ja')
    tts.save("response.mp3")
    
    st.write(f"ChatGPT: {response}")
    st.audio("response.mp3")
    
    image_url = get_image_from_duckduckgo(user_input)
    if image_url:
        st.image(image_url, caption="関連画像", use_column_width=True)
