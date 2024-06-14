import os
import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
from accelerate import init_empty_weights, load_checkpoint_and_dispatch, dispatch_model, infer_auto_device_map

model_id = 'beomi/Llama-3-Open-Ko-8B'
offload_folder = './offload'  # 오프로드 폴더 경로 지정
os.makedirs(offload_folder, exist_ok=True)

# 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 빈 가중치로 모델 초기화
with init_empty_weights():
    model = AutoModelForCausalLM.from_config(
        AutoModelForCausalLM.from_pretrained(model_id).config
    )

# 모델 로드 및 배포
model = load_checkpoint_and_dispatch(
    model, model_id, device_map="auto", offload_folder=offload_folder, offload_state_dict=True
)
model.eval()