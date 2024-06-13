import streamlit as st
from streamlit_chat import message
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 모델과 토크나이저 불러오기
model_id = 'MLP-KTLim/llama-3-Korean-Bllossom-8B'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
model.eval()

now = str(datetime.now())
st.title("★선녀보살 무료사주★")
st.image("image.png", width=500)
message("무엇이 궁금해 나를 찾아왔는가?")

model_loaded = True

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 앱 재실행 시 채팅 메시지 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 반응
if prompt := st.chat_input("물어보거라!"):
    # 사용자 메시지를 채팅 메시지 컨테이너에 표시
    st.chat_message("user").markdown(prompt)
    # 사용자 메시지를 채팅 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("대답 생성 중..."):
        try:
            # 모델을 이용한 텍스트 생성
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(**inputs)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            st.chat_message("assistant").markdown(response)
            # 응답 메시지를 채팅 기록에 추가
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"대답 생성에 실패했습니다: {e}")
else:
    st.error("모델을 불러오지 못했습니다. 다시 시도해주세요.")