from transformers import AutoProcessor, AutoModelForCausalLM

MODEL_ID = "google/gemma-4-26B-A4B-it"

# Load model
processor = AutoProcessor.from_pretrained(MODEL_ID)

from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-4-31B-it",
    trust_remote_code=True,
    device_map="auto"
)

print("Model loaded successfully.")