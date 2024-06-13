import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 로컬에 저장된 모델 경로 설정
local_model_path = "C:/Temp"

# 모델과 토크나이저 로드
model = AutoModelForCausalLM.from_pretrained(local_model_path)
tokenizer = AutoTokenizer.from_pretrained(local_model_path)

# 더미 입력 생성
dummy_input = torch.tensor([tokenizer.encode("Hello, how are you?", return_tensors="pt").input_ids])

# ONNX로 변환
torch.onnx.export(
    model, 
    dummy_input, 
    "llama_model.onnx", 
    input_names=["input_ids"], 
    output_names=["output"],
    dynamic_axes={"input_ids": {0: "batch_size"}, "output": {0: "batch_size"}},
    opset_version=11
)