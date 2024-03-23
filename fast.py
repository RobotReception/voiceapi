import json

import aiofiles
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from Dataclass import GeminiAssistant

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/send-message/")
def send_message(message: Message):
    last_update = {
        "msg": "null",
        "opration_number": 0,
        "wallet_name": "null",
        "phone_number": "null",
        "amount": "null",
        "mobile_companay": "null"
    }
    assistant = GeminiAssistant()
    question = message.message  # Correctly extract the message string
    print(question)
    file_name = "data.json"
    with open(file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    datalast = {}

    if data["opration_number"] == 0:  # Assuming typo correction
        assistant.updeat_data(question)  # Assuming this is an async method
        datalast =  assistant.read_json()  # Assuming this is an async method

    elif data["opration_number"] == 1:
        assistant.secound_op(question)  # Assuming typo correction and async method
        datalast =  assistant.read_json()
        # assistant.update_json_file("data.json", last_update)



    elif data["opration_number"] == 2:
        datalast =  assistant.read_json()
        assistant.update_json_file("data.json", last_update)

    elif data["opration_number"] == 3:
        datalast =  assistant.read_json()

    else:
        datalast =  assistant.read_json()



    return datalast
