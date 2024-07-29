from fastapi import FastAPI, Request, Response
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
    return {"test": "OK"}

@app.post("/request")
async def request_handler(request: Request):
    data = await request.json()
    
    api_key = data['api_key']
    model = data['model']
    prompt = data['prompt']
   
    try:
        temperature = float(data['temperature']) 
    except KeyError:
        temperature = 0.5
    
    logger.info(f"api_key: {api_key}\nmodel: {model}\ntemperature: {temperature}\nprompt: {prompt}")
    response = text_chat_gpt(api_key, model, prompt, temperature).json()
    logger.info(f"response: {response}")
    return JSONResponse(content=response)

def text_chat_gpt(api_key, model, messages, temperature=0.9):
    try:
        client = OpenAI(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature
        )
        # Extract the relevant information from the response
        response = {
            "id": chat_completion.id,
            "choices": [
                {
                    "finish_reason": choice.finish_reason,
                    "index": choice.index,
                    "message": {
                        "content": choice.message.content,
                        "role": choice.message.role
                    }
                } for choice in chat_completion.choices
            ],
            "usage": {
                "completion_tokens": chat_completion.usage.completion_tokens,
                "prompt_tokens": chat_completion.usage.prompt_tokens,
                "total_tokens": chat_completion.usage.total_tokens
            }
        }
        return response
    except Exception as e:
        return {"error": str(e)}

@app.post("/token_counter")
async def token_counter_handler(request: Request):
    data = await request.json()
    logger.info(f"token_counter data: {data}")
    tokens = ""
    try:
        text = data['text']
        model = data['model']
        
        try:
            enc = tiktoken.encoding_for_model(model)
        except KeyError:
            # If the model is not recognized, fall back to a default encoding
            logger.warning(f"Model {model} not recognized. Using default encoding.")
            enc = tiktoken.get_encoding("cl100k_base")  # Default to GPT-4 encoding
        
        tokens = enc.encode(text)
    except Exception as e:
        logger.error(f"Exception: {e}")
    logger.info(f"tokens: {len(tokens)}")

    return Response(content=json.dumps({"tokens": len(tokens)}), media_type="application/json")
