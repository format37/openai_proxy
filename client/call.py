import requests


def main():
    url = 'http://localhost:4714/request'

    user_text = 'The capital of Britain'
    prompt = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt.append({"role": "user", "content": str(user_text)})
    request = {
        "api_key": "YOUR_KEY",
        "prompt": prompt
        }
    # Request
    response = requests.post(url, json=request)
    # Response code
    print(response.status_code)
    try:
        print('JSON:', response.json())
    except Exception as e:
        print(response.text)


if __name__ == '__main__':
    main()
