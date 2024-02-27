import requests
import json
from InitialPrompts import AgePrompt, Introduction
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI()
# 67d8ece657b29e5219190ee2ba7eb2db

def GetValue(prompt):
    # Your API endpoint URL
    api_url = "http://192.168.100.116:5000/v1/completions"

    # Replace these with your actual header values
    headers = {
        "x-api-key": "469d6ea84d28a773fbcffdf25e9d2616",
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


def EntityInference(prompt):
    # Your API endpoint URL
    api_url = "http://192.168.100.116:5000/v1/completions"

    # Replace these with your actual header values
    headers = {
        "x-api-key": "469d6ea84d28a773fbcffdf25e9d2616",
        "Content-Type": "application/json"
        }

    # Example request body with parameters as described
    request_body = {
    "max_tokens": 16000,
    "stop": "*end",
    "token_healing": True,
    "temperature": 1,
    "temperature_last": True,
    "smoothing_factor": 0,
    "top_k": 1,
    "min_p": 0.02,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "repetition_penalty": 1,
    "repetition_decay": 0,
    "mirostat_mode": 0,
    "mirostat_tau": 1.5,
    "mirostat_eta": 0.3,
    "add_bos_token": True,
    "ban_eos_token": False,
    "typical": 1,
    "penalty_range": 8192,
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
    ### Find "*start" and "*end" in the text_result
    start_marker = "*start"
    end_marker = "*end"
    start_pos = text_result.find(start_marker) + len(start_marker)
    end_pos = text_result.find(end_marker, start_pos)
    json_content = text_result[start_pos:end_pos].strip()

    return json_content
    # Step 3: Parse the JSON string
    #try:
    #    json_data = json.loads(json_content)
    #    return json_content
    #except json.JSONDecodeError as e:
    #    print(f"Failed to parse JSON: {e}")

def FilterInference(prompt):
    # Your API endpoint URL
    api_url = "http://192.168.100.116:5000/v1/completions"

    # Replace these with your actual header values
    headers = {
        "x-api-key": "469d6ea84d28a773fbcffdf25e9d2616",
        "Content-Type": "application/json"
        }

    # Example request body with parameters as described
    request_body = {
    "max_tokens": 16000,
    "stop": "*end",
    "token_healing": True,
    "temperature": 1,
    "temperature_last": True,
    "smoothing_factor": 0,
    "top_k": 1,
    "min_p": 0.02,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "repetition_penalty": 1,
    "repetition_decay": 0,
    "mirostat_mode": 0,
    "mirostat_tau": 1.5,
    "mirostat_eta": 0.3,
    "add_bos_token": True,
    "ban_eos_token": False,
    "typical": 1,
    "penalty_range": 8192,
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
    ### Find "*start" and "*end" in the text_result
    start_marker = "*start"
    end_marker = "*end"
    start_pos = text_result.find(start_marker) + len(start_marker)
    end_pos = text_result.find(end_marker, start_pos)
    json_content = text_result[start_pos:end_pos].strip()

    # Step 3: Parse the JSON string
    try:
        json_data = json.loads(json_content)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return "Failed to parse JSON."

'''

json_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Entity Cluster Labeling Result",
  "description": "A schema for validating the result of entity cluster labeling",
  "type": "object",
  "properties": {
    "Labels": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "label": {
            "type": "string",
            "description": "The label representing a group of similar entities"
          },
          "entities": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "The list of entities represented by the label"
          },
          "entityIDs": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "The IDs of entities represented by the label"
          }
        },
        "required": ["label", "entities", "entityIDs"],
        "additionalProperties": False
      },
      "description": "An array of labels and their corresponding entities and IDs"
    }
  },
  "required": ["Labels"],
  "additionalProperties": False
}


def FilterInference(prompt):
    api_url = "http://192.168.100.116:8000/generate"
    headers = {
        "x-api-key": "469d6ea84d28a773fbcffdf25e9d2616",
        "Content-Type": "application/json"
    }
    request_body = {
        "max_tokens": 16000,
        "stop": "*end",
        "temperature": 1,
        "top_k": 1,
        "min_p": 0.02,
        "repetition_penalty": 1,
        "prompt": prompt,
        "schema": json.dumps(json_schema)
    }

    response = requests.post(api_url, headers=headers, json=request_body)
    response_body = response.json()
    print(response_body)  # Debugging: print the entire response body

    # Ensure 'text' field exists and is not empty
    if 'text' in response_body and len(response_body['text']) > 0:
        # Extract the first element of 'text' list which contains the response
        text_response = response_body['text'][0]

        # Find the starting position of the JSON content
        json_start_pos = text_response.find("*start") + len("*start")
        if json_start_pos > -1:
            # Extract the JSON string from the response
            json_str = text_response[json_start_pos:].strip()

            try:
                # Attempt to parse the JSON string
                json_data = json.loads(json_str)
                return json_data
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
        else:
            print("JSON start marker not found.")
    else:
        print("Response 'text' field is missing or empty.")
    
    return "Failed to parse JSON."

'''

def EntityInferenceOpenAI(prompt):
    # Your API endpoint URL
    completion = client.chat.completions.create(
        model="gpt-4-0125-preview",
        #model="gpt-4-0125-preview",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a domain expert in everything related to light and its relations to neurological disorders. Please response in the language of the user's question."},
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message.content)
    try:
        entities = json.loads(completion.choices[0].message.content)
        return entities
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")