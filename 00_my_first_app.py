import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def init_page():
    st.set_page_config(
        page_title="My Great ChatGPT",
        page_icon="🤗"
    )
    st.header("My Great ChatGPT 🤗")
    st.sidebar.title("Options")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.session_state.costs = []


def select_model():
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo"
    else:
        model_name = "gpt-4"

    # サイドバーにスライダーを追加し、temperatureを0から2までの範囲で選択可能にする
    # 初期値は0.0、刻み幅は0.1とする
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.01)

    return ChatOpenAI(temperature=temperature, model_name=model_name, streaming=True)


def main():
    init_page()

    llm = select_model()
    init_messages()

    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            st.write('assistant: ' + message.content)
        elif isinstance(message, HumanMessage):
            st.write('user: ' + message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")

    # ユーザーの入力を監視
    user_input = st.text_input("聞きたいことを入力してね！")
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.write("user: " + user_input)
        with st.spinner("ChatGPT is typing ..."):
            st_callback = StreamlitCallbackHandler(st.container())
            response = llm(st.session_state.messages, callbacks=[st_callback])
        st.session_state.messages.append(AIMessage(content=response.content))
        st.write("assistant: " + response.content)


if __name__ == '__main__':
    main()
