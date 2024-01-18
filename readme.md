# voice-illustration chatbot

## 음성으로 대화하고 그림을 그려주는 챗봇

### 🚀Quick setup

```bash
# clone project
git clone https://github.com/DimensionSTP/voillust-chatbot.git
cd voillust-chatbot

# [OPTIONAL] create conda environment
conda create -n myenv python=3.8
conda activate myenv

# install requirements
pip install -r requirements.txt
```

### 반드시 .env 파일에 결제 정보가 등록된 아이디의 api key 입력(그림과 음성은 결제 필요)

```bash
$ streamlit run app.py
```

### 앱 실행 후, 마이크 아이콘을 누르고 마이크에 말하기

![example](https://github.com/DimensionSTP/voillust-chatbot/assets/65501090/3d2d4d5c-4d68-42a6-aa9f-047cc8959c9c)