import requests
import json


def token_counter(text, model):
    url = 'http://localhost:4714/token_counter'
    data = {
        "text": text,
        "model": model
    }

    response = requests.post(url, json=data)
    # response = requests.post(url, kwargs=data)
    return response


def send_request(user_text, model):
    url = 'http://localhost:4714/request'
    prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_text}
    ]
    request_data = {
        "api_key": input('Please, input your Openai API key:'),
        "model": model,
        "prompt": prompt
    }
    # Json dumps prompt
    prompt_dumped = json.dumps(prompt)
    print(
        'Token count forecast:', 
        token_counter(prompt_dumped, model).json()['tokens']
        )
    response = requests.post(url, json=request_data)
    return response


def main():
    model = 'gpt-3.5-turbo'
    user_text = 'The capital of Britain'
    response = send_request(user_text, model)
    print("Status code:", response.status_code)

    try:
        print('JSON:', response.json())
    except Exception as e:
        print("Text:", response.text)


if __name__ == '__main__':
    main()
