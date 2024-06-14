from huggingface_hub import hf_hub_download

# 모델과 관련된 파일 다운로드
repo_id = 'beomi/Llama-3-Open-Ko-8B'
model_files = ['config.json', 'pytorch_model.bin', 'tokenizer_config.json', 'vocab.txt']

# 모델 파일을 저장할 로컬 디렉토리
local_dir = './local_model'

# 각 파일 다운로드
for file in model_files:
    hf_hub_download(repo_id=repo_id, filename=file, local_dir=local_dir)