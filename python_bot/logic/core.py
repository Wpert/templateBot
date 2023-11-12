'''Объявляет все объекты для работы.

Подключает нужные модули для бота, настраивает базовые настройки
для отправки и получения данных.'''

import typing
from typing import Dict, Any
import json

with open("/home/vpert/gitproj/templatebot/templatebot/python_bot/logic/variables.json", "r") as variables:
    variables_json = variables.read()
vars = json.loads(variables_json)

TOKEN: str = vars["token"]
loggerChat_id: int = vars["logChat"]
qnaChat_id: int = vars["qnaChat"]
bot_id: int = 0

import logging
from aiogram import Bot, Dispatcher, types

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

#  {
#     id1 : {data about user_id1},
#     id2 : {data about user_id2},
#     ...
#  }
userDataBase: Dict[int, Dict[str, Any]] = {1413950580 : {'username' : 'Vpert', 'status' : 4}}

# {
#     id1 : "Well, answer to your question...",
#     id2 : "Mgph, mmm amm can you ask anybody else?.."
# }
adminAnswers: Dict[int, str]= {}