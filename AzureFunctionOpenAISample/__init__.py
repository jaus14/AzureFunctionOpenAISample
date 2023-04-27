import os
import openai

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    openai.api_type = "azure"
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    message = req.params.get('message')
    if not message:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            message = req_body.get('message')

    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo-v0301",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that helps people find information."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.7,
        max_tokens=1000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    if response:
        return func.HttpResponse(str(response.choices[0].message.content))
    else:
        return func.HttpResponse(status_code=500)
