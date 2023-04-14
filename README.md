# OpenAI API proxy
API proxy
# Installation
```
git clone https://github.com/format37/openai_proxy.git
cd openai_proxy
docker-compose up --build -d
```
# Using
Obtain you key at [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
```
python client/call.py
```
Output:
```
Status code: 200
JSON: {'choices': [{'finish_reason': 'stop', 'index': 0, 'message': {'content': 'The capital of Britain is London.', 'role': 'assistant'}}], 'created': 1681381660, 'id': 'chatcmpl-74oSyDjFxbLOKYHUCbJ9I7Y8HC8RQ', 'model': 'gpt-3.5-turbo-0301', 'object': 'chat.completion', 'usage': {'completion_tokens': 7, 'prompt_tokens': 23, 'total_tokens': 30}}
```