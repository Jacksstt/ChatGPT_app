import streamlit as st
from gtts import gTTS
import openai

# OpenAIのAPIキーを設定
openai.api_key = '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'

def get_gpt3_response(prompt):
    response = openai.Completion.create(
      engine="gpt-3.5-turbo",  # engineをgpt-3.5-turboに変更
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

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

