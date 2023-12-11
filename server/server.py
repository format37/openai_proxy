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
        temperature = 1
        
    response = text_chat_gpt(api_key, model, prompt, temperature).json()
    logger.info(f"response: {response}")
    return JSONResponse(content=response)

def text_chat_gpt(api_key, model, messages, temperature=0.9):
    try:
        """openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=prompt,
            temperature=temperature
        )"""
        client = OpenAI(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
        )
        return chat_completion
    
    except Exception as e:
        return str(e)

@app.post("/token_counter")
async def token_counter_handler(request: Request):
    data = await request.json()
    logger.info(f"token_counter data: {data}")
    try:
        text = data['text']
        model = data['model']
        
        enc = tiktoken.encoding_for_model(model) 
        tokens = enc.encode(text)
    except Exception as e:
        logger.error(f"Exception: {e}\ndata: {data}")    
    logger.info(f"tokens: {len(tokens)}")

    # return {"tokens": str(len(tokens))}
    return Response(content=json.dumps({"tokens": len(tokens)}), media_type="application/json")
