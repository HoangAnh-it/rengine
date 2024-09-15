from reNgine import settings
import minify_html
import requests


def preprocess_url(url):
    url = url.strip("/")
    if url.startswith('https://'):
        url = url[8:]
    elif url.startswith('http://'):
        url = url[7:]
    return url


def preprocess_html(html):
    return minify_html.minify(html)


def preprocess_input(url, html=None):
    if html is not None:
        return preprocess_url(url) + preprocess_html(html)
    else:
        return preprocess_url(url)


# def predict(input):
#     API_URL = f"https://api-inference.huggingface.co/models/{settings.HUGGING_FACE_MODEL}"
#     headers = {"Authorization": f"Bearer {settings.HUGGING_FACE_API_KEY}"}

#     payload = {
#         "inputs": input,
#     }
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

def predict(input):
    model_path = settings.HUGGING_FACE_MODEL
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    MAX_LENGTH = 512
    tokens = tokenizer(input, truncation=False)
    probs = []
    for i in range(0, len(tokens['input_ids']), MAX_LENGTH):
        
        input_dict = {
            "input_ids": tokens['input_ids'][i:i+MAX_LENGTH],
            "token_type_ids": tokens['token_type_ids'][i:i+MAX_LENGTH],
            "attention_mask": tokens['attention_mask'][i:i+MAX_LENGTH],
        }
        input_tensors = {key: torch.tensor(val).unsqueeze(0) for key, val in input_dict.items()}
#             chunked_tokens = tokens[i:i+ MAX_LENGTH]
#             chunked_text = tokenizer.convert_tokens_to_string(chunked_tokens)
#             outputs = model(**tokenizer(chunked_text, return_tensors="pt", max_length=tokenizer.model_max_length, truncation=False))
#             probs.append(prob)
        outputs = model(**input_tensors)
        prob = torch.softmax(outputs.logits, dim=-1).flatten().tolist()
        probs.append(prob)
        if len(probs) == 3:
            break

    probs_transposed = np.array(probs).T.tolist()
    mean_benign = np.mean(probs_transposed[0])
    mean_phishing = np.mean(probs_transposed[1])
    return mean_benign,mean_phishing