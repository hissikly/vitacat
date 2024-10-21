import requests
from aiogram import types
import uuid
import random
from langchain_community.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv


load_dotenv()


async def get_message_by_gigachain(message: types.Message):
    chat = GigaChat(credentials=os.getenv("CREDENTIALS"), verify_ssl_certs=False)

    pipeline = [SystemMessage(content="Ты эксперт в области фармацевтики и нутрициологии. Тебя зовут ВитаКошка. Ты должна по жалобам пользователей, их самочувствию порекомендовать им витамины или пищевые добавки. Ты должна советовать витамины либо пищевые добавки людям. Витамины не должны нести в себе сильных эффектов, рекомендуй только то, что можно каждому человеку.")]
    pipeline.append(HumanMessage(content=message.text))
    return chat(pipeline).content



def get_access_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload='scope=GIGACHAT_API_PERS'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': str(uuid.UUID(int=random.getrandbits(128), version=4)),
    'Authorization': 'Basic ' + os.getenv("CREDENTIALS")
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    response_json = response.json()

    return response_json["access_token"]