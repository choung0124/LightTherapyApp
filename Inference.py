import requests
import json
from InitialPrompts import AgePrompt, Introduction

def GetValue(prompt):
    # Your API endpoint URL
    api_url = "http://192.168.100.131:5005/v1/completions"

    # Replace these with your actual header values
    headers = {
        "x-api-key": "67d8ece657b29e5219190ee2ba7eb2db",
        "Content-Type": "application/json"
        }

    # Example request body with parameters as described
    request_body = {
    "max_tokens": 150,
    "generate_window": 512,
    "stop": "string",
    "token_healing": True,
    "temperature": 1,
    "temperature_last": True,
    "smoothing_factor": 0,
    "top_k": 0,
    "top_p": 1,
    "top_a": 0,
    "min_p": 0,
    "tfs": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "repetition_penalty": 1,
    "repetition_decay": 0,
    "mirostat_mode": 0,
    "mirostat_tau": 1.5,
    "mirostat_eta": 0.3,
    "add_bos_token": True,
    "ban_eos_token": False,
    "logit_bias": {"1": 10},
    "negative_prompt": "string",
    "typical": 1,
    "penalty_range": 0,
    "cfg_scale": 1,
    "max_temp": 1,
    "min_temp": 1,
    "temp_exponent": 1,
    "model": "string",
    "stream": False,
    "logprobs": 0,
    "best_of": 0,
    "echo": False,
    "n": 1,
    "suffix": "string",
    "user": "string",
    "prompt": prompt
    }

    response = requests.post(api_url, headers=headers, json=request_body)
    response_body = response.json()
    text_result = response_body['choices'][0]['text']
    text_result_dict = json.loads(text_result)
    for key, value in text_result_dict.items():
        if value is None:
            print(f"{key} is not mentioned.")
            return None
        else:
            print(f"{key}: {value}")
            return key, value
