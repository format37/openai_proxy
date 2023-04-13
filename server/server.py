import os
import logging
from flask import Flask, request, jsonify
import openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def test_handler():
    logger.info("Received test request")
    return jsonify({"test": "OK"})


def text_chat_gpt(api_key, model, prompt):
    try:
        openai.api_key = api_key
        answer = openai.ChatCompletion.create(
            model=model,
            messages=prompt
        )
    except Exception as e:
        answer = str(e)
    return answer


@app.route("/request", methods=["POST"])
def request_handler():
    data = request.get_json()
    logger.info("Received request: %s", data)
    api_key = data['api_key']
    model = data['model']
    prompt = data['prompt']
    openai_response = text_chat_gpt(api_key, model, prompt)
    return openai_response


def main():
    app.run(
        host='0.0.0.0',
        debug=False,
        port=int(os.environ.get("PORT", 4714))
    )


if __name__ == "__main__":
    main()
