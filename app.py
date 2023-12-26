import os

from dotenv import load_dotenv
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

from src.utils import Utils


load_dotenv()
api_key = os.getenv("openai_api_key")
utils = Utils(api_key=api_key)

float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "오늘도 도와드릴게요!"}
        ]
initialize_session_state()

st.title("일러스트를 도와주는 음성 챗봇 🤖")
st.info("마이크 버튼을 누르고 마이크에 말해주세요.")
st.info("그림을 보고싶으면 그려줘! 혹은 그려줄래!라고 말해보세요.")

footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    with st.spinner("음성 인식 중..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = utils.stt(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        if ("그려줘" in transcript) or ("그려줄래" in transcript):
            with st.spinner("그림을 그리는 중이에요!"):
                final_response = "어때요? 마음에 드시나요?"
                utils.get_image(transcript)
                audio_file = utils.tts(final_response)
                utils.autoplay_audio(audio_file)
        else:
            with st.spinner("생각 중이에요🤔..."):
                final_response = utils.get_answer(st.session_state.messages)
            with st.spinner("곧 답변해드릴게요!..."):    
                audio_file = utils.tts(final_response)
                utils.autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

footer_container.float("bottom: 0rem;")