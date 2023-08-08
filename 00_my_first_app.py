import streamlit as st
from gtts import gTTS
import openai
import os

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

