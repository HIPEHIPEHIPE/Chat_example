from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from optimum.intel.openvino import OVModelForCausalLM
from langchain_community.llms import Ollama


model_id = "llama3-ko:latest"


model = OVModelForCausalLM.from_pretrained(model_id, export=True, device="GPU")
tokenizer=AutoTokenizer.from_pretrained(model_id)

pipe = pipeline(
  task="text-generation",
  model=model,
  tokenizer=tokenizer,
  model_kwargs={"torch_dtype": torch.bfloat16},
)

k = pipe("Hey how are you doing today?")
print(k)