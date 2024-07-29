from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from openai import OpenAI
import tiktoken
import json

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/test")
async def test_handler():
    return JSONResponse(content={"test": "OK"})

@app.post("/request")
async def request_handler(request: Request):
    try:
        data = await request.json()
        
        api_key = data['api_key']
        model = data['model']
        prompt = data['prompt']
        temperature = float(data.get('temperature', 0.5))
        
        logger.info(f"Received request - model: {model}, temperature: {temperature}")
        response = text_chat_gpt(api_key, model, prompt, temperature)
        
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Error in request_handler: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

def text_chat_gpt(api_key, model, messages, temperature=0.9):
    try:
        client = OpenAI(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature
        )
        
        # Extract the content of the last message
        last_message_content = chat_completion.choices[-1].message.content

        # Replace ```json\n with ""
        last_message_content = last_message_content.replace("```json\n", "")
        # Replace ``` with ""
        last_message_content = last_message_content.replace("```", "")
        
        # Try to parse the content as JSON
        try:
            json_response = json.loads(last_message_content)
            return json_response
        except json.JSONDecodeError:
            # If it's not valid JSON, return it as a string in a JSON object
            return {"response": last_message_content}

    except Exception as e:
        logger.error(f"Error in text_chat_gpt: {str(e)}")
        return {"error": str(e)}

@app.post("/token_counter")
async def token_counter_handler(request: Request):
    try:
        data = await request.json()
        text = data['text']
        model = data['model']
        
        try:
            enc = tiktoken.encoding_for_model(model)
        except KeyError:
            logger.warning(f"Model {model} not recognized. Using default encoding.")
            enc = tiktoken.get_encoding("cl100k_base")
        
        tokens = enc.encode(text)
        return JSONResponse(content={"tokens": len(tokens)})
    except Exception as e:
        logger.error(f"Error in token_counter_handler: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)