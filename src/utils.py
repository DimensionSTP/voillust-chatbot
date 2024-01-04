from openai import OpenAI
import base64
import streamlit as st


class Utils():
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def stt(self, audio_file_path: str) -> str:
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                response_format="text",
                file=audio_file
            )
        return transcript

    def get_answer(self, messages: str) -> str:
        system_message = [
            {
                "role": "system", 
                "content": "You are a helpful AI chatbot, that answers questions asked by User. In particular, answer in the direction of specifying the picture that the user wants to draw."
            }
        ]
        messages = system_message + messages
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
        return response.choices[0].message.content

    def tts(self, input_text: str) -> str:
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=input_text
        )
        webm_file_path = "temp_audio_play.mp3"
        with open(webm_file_path, "wb") as f:
            response.stream_to_file(webm_file_path)
        return webm_file_path

    def autoplay_audio(self, file_path: str) -> None:
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode("utf-8")
        md = f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)

    def get_image(self, prompt: str) -> None:
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        st.image(response.data[0].url)