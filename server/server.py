# -*- coding: utf-8 -*-
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
    response = text_chat_gpt(api_key, model, prompt, temperature)
    logger.info(f"response: {response}")
    # return JSONResponse(content=json.dumps(response), media_type="application/json")
    return response

def text_chat_gpt(api_key, model, messages, temperature=0.9):
    try:
        client = OpenAI(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature
        ).json()
        logger.info(f"chat_completion type: {type(chat_completion)}")
        
        # Convert ChatCompletion to a dictionary
        # response_dict = {
        #     "id": chat_completion.id,
        #     "object": chat_completion.object,
        #     "created": chat_completion.created,
        #     "model": chat_completion.model,
        #     "choices": [{
        #         "index": choice.index,
        #         "message": {
        #             "role": choice.message.role,
        #             "content": choice.message.content
        #         },
        #         "finish_reason": choice.finish_reason
        #     } for choice in chat_completion.choices],
        #     "usage": {
        #         "prompt_tokens": chat_completion.usage.prompt_tokens,
        #         "completion_tokens": chat_completion.usage.completion_tokens,
        #         "total_tokens": chat_completion.usage.total_tokens
        #     }
        # }
        
        # return JSONResponse(content=json.dumps(response_dict), media_type="application/json")
        return chat_completion
    except Exception as e:
        return JSONResponse(content=json.dumps({"error": str(e)}), media_type="application/json")

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
            logger.warning(f"Model {model} not recognized. Using default encoding.")
            enc = tiktoken.get_encoding("cl100k_base")
        
        tokens = enc.encode(text)
    except Exception as e:
        logger.error(f"Exception: {e}")
    logger.info(f"tokens: {len(tokens)}")

    return Response(content=json.dumps({"tokens": len(tokens)}), media_type="application/json")