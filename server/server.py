import os
from flask import Flask, request, jsonify
import logging
import openai


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

# Get test
@app.route("/test", methods=["GET"])
def test_handler():
	logger.info("Received test request")
	return jsonify({"test": "OK"})


def text_chat_gpt(prompt, api_key=""):
	try:
		openai.api_key = api_key
		answer = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			# model = 'gpt-4-32k-0314',
			messages=prompt
		)
	except Exception as e:
		answer = str(e)
	return answer


# Post request with JSON data
@app.route("/request", methods=["POST"])
def request_handler():
	data = request.get_json()
	logger.info("Received request: %s", data)
	api_key = data['api_key']
	prompt = data['prompt']
	openai_response = text_chat_gpt(prompt, api_key)
	# logger.info("Response code: %s", openai_response.status_code)
	# logger.info("Response: %s", openai_response)
	# return jsonify(openai_response)
	return openai_response


if __name__ == "__main__":
	app.run(
		host='0.0.0.0',
		debug=False,
		port=int(os.environ.get("PORT", 4714))
		)
