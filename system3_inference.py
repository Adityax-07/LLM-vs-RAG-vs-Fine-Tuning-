"""
Run inference with the fine-tuned model.
After running system3_finetune_colab.ipynb on Google Colab:
  1. Download finetuned_model.zip from Colab
  2. Unzip into this project root as finetuned_model/
  3. Then run this file
"""
import os
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
FINETUNED_PATH = "./finetuned_model"

_model = None
_tokenizer = None


def load_model():
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer

    print("Loading fine-tuned model (this takes ~30s first time)...")
    _tokenizer = AutoTokenizer.from_pretrained(FINETUNED_PATH)
    base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float32)
    _model = PeftModel.from_pretrained(base, FINETUNED_PATH)
    _model.eval()
    print("Fine-tuned model ready.")
    return _model, _tokenizer


def ask_finetuned(question: str) -> dict:
    if not os.path.exists(FINETUNED_PATH):
        return {
            "system": "Fine-tuned",
            "question": question,
            "answer": "Fine-tuned model not found. Run system3_finetune_colab.ipynb on Google Colab first, then unzip finetuned_model.zip here.",
            "response_time": 0,
        }

    model, tokenizer = load_model()
    start = time.time()

    prompt = f"### Instruction:\n{question}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = full_output.split("### Response:\n")[-1].strip()
    elapsed = round(time.time() - start, 2)

    return {
        "system": "Fine-tuned",
        "question": question,
        "answer": answer,
        "response_time": elapsed,
    }


if __name__ == "__main__":
    test_q = "What is binary search?"
    print(f"Question: {test_q}\n")
    result = ask_finetuned(test_q)
    print(f"Answer:\n{result['answer']}")
    print(f"\nResponse time: {result['response_time']}s")
