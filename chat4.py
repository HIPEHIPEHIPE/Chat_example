
import streamlit as st
from streamlit_chat import message
from datetime import datetime
from transformers import AutoConfig, AutoTokenizer
from optimum.intel.openvino import OVModelForCausalLM

# OpenVINO 모델 설정
ov_config = {
    "PERFORMANCE_HINT": "LATENCY",
    "NUM_STREAMS": "1",
    "CACHE_DIR": "",
    "INFERENCE_PRECISION_HINT": "f16"
}

# 토크나이저 및 모델 로드
model_id = "xriminact/llama-3-8b-instruct-openvino-int4"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
ov_model = OVModelForCausalLM.from_pretrained(
    model_id,
    device="CPU",
    ov_config=ov_config,
    config=AutoConfig.from_pretrained(model_id, trust_remote_code=True),
    trust_remote_code=True,
)

now = str(datetime.now())
st.title("★선녀보살 무료사주★")
#st.image("image.png", width=500)
message("무엇이 궁금해 나를 찾아왔는가?")

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
            inputs = tokenizer(prompt, return_tensors="pt")
            outputs = ov_model.generate(**inputs)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            st.chat_message("assistant").markdown(response)
            # 응답 메시지를 채팅 기록에 추가
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"대답 생성에 실패했습니다: {e}")