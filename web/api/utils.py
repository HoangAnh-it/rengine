from reNgine import settings
import minify_html
import requests



def preprocess_url(url):
    return url


def preprocess_html(html):
    return minify_html.minify(html)


def preprocess_input(url, html=None):
    if html is not None:
        return preprocess_url(url) + preprocess_html(html)
    else:
        return preprocess_url(url)


def predict(input):
    API_URL = "https://api-inference.huggingface.co/models/ealvaradob/bert-finetuned-phishing"
    headers = {"Authorization": f"Bearer {settings.HUGGING_FACE_API_KEY}"}

    payload = {
        "inputs": input,
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.json())
    return response.json()