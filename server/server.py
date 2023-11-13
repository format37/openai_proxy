from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import logging
# import openai
from openai import OpenAI
import tiktoken
import pickle
import datetime

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
        
    response = text_chat_gpt(api_key, model, prompt, temperature)
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
    text = data['text']
    model = data['model']
    
    enc = tiktoken.encoding_for_model(model) 
    tokens = enc.encode(text)
    
    return {"tokens": len(tokens)}
