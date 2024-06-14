import os
import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = 'beomi/Llama-3-Open-Ko-8B-Instruct-preview'
offload_folder = './offload'  # 오프로드 폴더 경로 지정

# 오프로드 폴더 생성
os.makedirs(offload_folder, exist_ok=True)

# 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 모델 로드 및 배포
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
    offload_folder=offload_folder
)
model.eval()

PROMPT = '''당신은 유용한 AI 어시스턴트입니다. 사용자의 질의에 대해 친절하고 정확하게 답변해야 합니다.'''
instruction = "다음 제목의 논문을 요약해줘 'Optimizing Language Augmentation for Multilingual Large Language Models: A Case Study on Korean'"

messages = [
    {"role": "system", "content": f"{PROMPT}"},
    {"role": "user", "content": f"{instruction}"}
]

input_ids = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("")
]

# 대답 시간 측정 시작
start_time = time.time()

outputs = model.generate(
    input_ids,
    max_new_tokens=512,
    eos_token_id=terminators,
    do_sample=True,
    temperature=1,
    top_p=0.9,
)

# 대답 시간 측정 종료
end_time = time.time()
response_time = end_time - start_time

response = outputs[0][input_ids.shape[-1]:]
print(tokenizer.decode(response, skip_special_tokens=True))

# 대답 시간 출력
print(f"Response time: {response_time:.2f} seconds")

# 불필요한 변수 해제 및 GPU 메모리 최적화
del input_ids
del outputs
torch.cuda.empty_cache()