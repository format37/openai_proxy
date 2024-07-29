# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import logging
from openai import OpenAI
import tiktoken
import json
import pprint

app = FastAPI() 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def decode_unicode_json(encoded_string):
    # First, parse the JSON string
    parsed_json = json.loads(encoded_string)
    
    # If the result is a string, it might be another layer of JSON
    if isinstance(parsed_json, str):
        try:
            # Try to parse it again
            return json.loads(parsed_json)
        except json.JSONDecodeError:
            # If it's not valid JSON, return the string as is
            return parsed_json
    
    # If it's already a dictionary or list, return it
    return parsed_json

@app.get("/test")
async def test_handler():
    return {"test": "OK"}

@app.post("/request_full")
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
    logger.info(f"response type: {type(response)}")
    # response type: <class 'str'>
    json_content = json.loads(response)
    logger.info(f"json_content type: {type(json_content)}")
    # json_content type: <class 'dict'>
    
    # Log the JSON content
    logger.info(pprint.pformat(json_content, indent=2))
    # Return as JSON
    # return JSONResponse(content=json_content, media_type="application/json")
    # Return JSON as string
    # return Response(content=json.dumps(json_content), media_type="application/json")
    return json_content

    # 
    # json_content = json.loads(response.body.decode('utf-8'))
    # # logger.info(pprint.pformat(json_content, indent=2))
    # decoded_output = decode_unicode_json(json_content)
    # # print(json.dumps(decoded_output, ensure_ascii=False, indent=2))
    # # return JSONResponse(content=json.dumps(decoded_output), media_type="application/json")
    # formatted_output = json.dumps(decoded_output, ensure_ascii=False, indent=2)
    # logger.info(f"formatted_output: {formatted_output}")
    # # return Response(content=formatted_output, media_type="application/json")    
    # return JSONResponse(content=formatted_output, media_type="application/json")

def text_chat_gpt(api_key, model, messages, temperature=0.9):
    try:
        client = OpenAI(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature
        )
        
        # Convert ChatCompletion to a dictionary
        response_dict = {
            "id": chat_completion.id,
            "object": chat_completion.object,
            "created": chat_completion.created,
            "model": chat_completion.model,
            "choices": [{
                "index": choice.index,
                "message": {
                    "role": choice.message.role,
                    "content": choice.message.content
                },
                "finish_reason": choice.finish_reason
            } for choice in chat_completion.choices],
            "usage": {
                "prompt_tokens": chat_completion.usage.prompt_tokens,
                "completion_tokens": chat_completion.usage.completion_tokens,
                "total_tokens": chat_completion.usage.total_tokens
            }
        }
        
        message = response_dict['choices'][-1]['message']['content']
        # Replace ```json\n with ""
        message = message.replace("```json\n", "")
        # Replace ``` with ""
        message = message.replace("```", "")
        # return JSONResponse(content=json.dumps(message), media_type="application/json")
        # Return classic json
        return message
    except Exception as e:
        # return JSONResponse(content=json.dumps({"error": str(e)}), media_type="application/json")
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
            logger.warning(f"Model {model} not recognized. Using default encoding.")
            enc = tiktoken.get_encoding("cl100k_base")
        
        tokens = enc.encode(text)
    except Exception as e:
        logger.error(f"Exception: {e}")
    logger.info(f"tokens: {len(tokens)}")

    return Response(content=json.dumps({"tokens": len(tokens)}), media_type="application/json")