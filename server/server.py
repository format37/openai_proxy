import os
import logging
from flask import Flask, request, jsonify
import openai
import tiktoken
import pickle
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def test_handler():
    logger.info("Received test request")
    return jsonify({"test": "OK"})


def text_chat_gpt(api_key, model, prompt, temperature=0.9):
    try:
        openai.api_key = api_key
        answer = openai.ChatCompletion.create(
            model=model,
            messages=prompt,
            temperature=temperature
            # max_tokens=2048
        )
    except Exception as e:
        answer = str(e)
    return answer

# Token counter endpoint
@app.route("/token_counter", methods=["POST"])
def token_counter_handler():
    # logger.info("Received token_counter request: "+str(request))
    # Extract text from request
    data = request.get_json(force=True)
    logger.info("Received token_counter: %s", data)
    text = data['text']
    model = data['model']
    # To get the tokeniser corresponding to a specific model in the OpenAI API:
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    return jsonify({"tokens": len(tokens)})


@app.route("/request", methods=["POST"])
def request_handler():
    try:
        # Forces the parsing of JSON data, even if the content type header is not set
        data = request.get_json(force=True)
        
        # Debug ++
        # Create folder logs if not exists
        """logger.info("Creating folder logs if not exists")
        if not os.path.exists('logs'):
            os.makedirs('logs')
            logger.info("Folder logs created")
        # Save date in a pickle file
        with open('logs/'+str(datetime.datetime.now())+'.pickle', 'wb') as f:
            logger.info("Saving data in pickle file")
            pickle.dump(data, f)
            logger.info("Data saved in pickle file")"""
        # Debug --

        logger.info("Received request: %s", data)
        api_key = data['api_key']
        model = data['model']
        prompt = data['prompt']
        try:
            temperature = float(data['temperature'])
        except KeyError:
            temperature = 0.5
        openai_response = text_chat_gpt(api_key, model, prompt, temperature)
    except Exception as e:
        logger.error(e)
        openai_response = str(e)
    return openai_response


def main():
    app.run(
        host='0.0.0.0',
        debug=False,
        port=int(os.environ.get("PORT", 4714))
    )


if __name__ == "__main__":
    main()
