from transformers import AutoConfig, AutoTokenizer
from optimum.intel.openvino import OVModelForCausalLM

ov_config = {"PERFORMANCE_HINT": "LATENCY", "NUM_STREAMS": "1", "CACHE_DIR": "", "INFERENCE_PRECISION_HINT": "f16"}

tok = AutoTokenizer.from_pretrained("xriminact/llama-3-8b-instruct-openvino-int4", trust_remote_code=True)

ov_model = OVModelForCausalLM.from_pretrained(
    "xriminact/llama-3-8b-instruct-openvino-int4",
    device="GPU",
    ov_config=ov_config,
    config=AutoConfig.from_pretrained("xriminact/llama-3-8b-instruct-openvino-int4", trust_remote_code=True),
    trust_remote_code=True,
)

test_string = "What is OpenVino?"
input_tokens = tok(test_string, return_tensors="pt")
answer = ov_model.generate(**input_tokens, max_new_tokens=200)
print(tok.batch_decode(answer, skip_special_tokens=True)[0])