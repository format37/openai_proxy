import requests


def send_request(user_text):
    url = 'http://localhost:4714/request'
    prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_text}
    ]
    request_data = {
        "api_key": input('Please, input your Openai API key:'),
        "model": "gpt-3.5-turbo",
        "prompt": prompt
    }

    response = requests.post(url, json=request_data)
    return response


def main():
    user_text = 'The capital of Britain'
    response = send_request(user_text)

    print("Status code:", response.status_code)

    try:
        print('JSON:', response.json())
    except Exception as e:
        print("Text:", response.text)


if __name__ == '__main__':
    main()
