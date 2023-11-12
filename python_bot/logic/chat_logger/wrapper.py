from typing import Callable, Union, Any
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from datetime import datetime

from logic import loggerChat_id, dp, bot, userDataBase, bot_id
from logic.texts.base import wrapperFunctionText, wrapperAccessText

import enum

@enum.unique
class AccessStatus(enum.IntEnum):
    default = 0
    active = 1
    moderator = 2
    admin = 3

def loggerChat(access_level: AccessStatus, loggingFlag: bool = True):
    # func : Callable[[Union[Message, CallbackQuery], Union[CommandObject, FSMContext]], Any]
    def accessor_inner(func: Callable[[Union[Message, CallbackQuery]], Any]):
        # *args: Union[Message, CallbackQuery]
        async def wrapper(*args, **kwargs):
            msg = args[0]
            fsmState = kwargs['state']
            commandObj = None

            try:
                commandObj = kwargs['command']
            except:
                pass

        # можно посмотреть что именно передаётся в сообщении aiogram
            # print('\n')
            # print(args)
            # print('\n')
            # print(kwargs)
            # print()
            if msg.from_user is None:
                return
            
            userId = msg.from_user.id
            username = msg.from_user.username
            userFirstname = msg.from_user.first_name.replace('<', '&lt;').replace('>', '&gt;')

            # Если человек ещё не был зарегистрирован в базе данных, то регистрируем
            # добавляем AccessStatus default
            if not userId in userDataBase.keys():
                userDataBase[userId] = {'username' : username, 'status' : AccessStatus.active}
                await bot.send_message(
                    loggerChat_id,
                    wrapperAccessText.format(
                        msg.from_user.id,
                        userFirstname,
                        msg.from_user.id,
                        datetime.now()
                        ),
                    parse_mode='HTML'
                    )
            
            # помечена ли функция как та, которую нужно логгировать
            if loggingFlag:
                await bot.send_message(
                    loggerChat_id, 
                    wrapperFunctionText.format(
                        func.__name__,
                        msg.from_user.id,
                        userFirstname,
                        msg.from_user.id,
                        userDataBase[userId]['status'],
                        access_level,
                        datetime.now()
                        ),
                    parse_mode='HTML'
                    )
                if isinstance(msg, Message):
                    await bot.forward_message(loggerChat_id, userId, msg.message_id)
                elif isinstance(msg, CallbackQuery):
                    print(msg.answer(msg.data))
                
            # проверяем acces_level функции, которую пользователь взял
            # соответственно запускаем / либо не запускаем функцию
            if access_level <= userDataBase[userId]['status']:
                try:
                    rslt = await func(*args, commandObj, fsmState)
                    return rslt
                except Exception as rslt:
                    await bot.send_message(
                        loggerChat_id,
                        f'#баг\nВ вызове функции <b>{func.__name__}</b> произошла ошибка:\n{str(rslt.args)}',
                        parse_mode="HTML")
                    return None
            else:
                await msg.reply(
                    f"Недостаточно прав на использование функции <b>{func.__name__}</b>.",
                    parse_mode="HTML"
                    )
                return None
        
        return wrapper
    return accessor_inner
