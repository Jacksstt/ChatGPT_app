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

# 音声入力のためのHTMLを追加
html = """
    <div>
        <button onclick="startDictation()" type="button">音声入力開始</button>
        <textarea id="result" rows="10" cols="50"></textarea>
    </div>
    <script>
        function startDictation() {
            if (window.hasOwnProperty('webkitSpeechRecognition')) {
                var recognition = new webkitSpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = "ja-JP";  # 日本語に設定
                recognition.start();
                recognition.onresult = function(e) {
                    document.getElementById('result').value = e.results[0][0].transcript;
                    recognition.stop();
                };
                recognition.onerror = function(e) {
                    recognition.stop();
                }
            }
        }
    </script>
"""

st.markdown(html, unsafe_allow_html=True)

# ユーザーからの音声入力を取得
user_input = st.text_area("あなたの質問を入力してください:")

if user_input:
    # ChatGPTからの応答を取得
    response = get_gpt3_response(user_input)
    
    # 応答を音声に変換
    tts = gTTS(text=response, lang='ja')
    tts.save("response.mp3")
    
    # 応答を表示と音声再生
    st.write(f"ChatGPT: {response}")
    st.audio("response.mp3")
    