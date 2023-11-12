from typing import List

from aiogram import html, types, Router
from aiogram.filters import Command, CommandObject
# from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from logic import states
from logic.texts import *
from logic.keyboards.user_kb import startKB
from logic.chat_logger import *

router = Router()

@router.message(
    Command('start')
    )
@loggerChat(AccessStatus.default)
async def start(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    if (command.args) and userDataBase[msg.from_user.id]["status"] > 1:
        await state.set_state(states.UserMainMenu.answer)

        adminId: int = msg.from_user.id
        # user id | msg id
        userId = int(command.args)
        userName: str = userDataBase[userId]["username"]

        userDataBase[adminId]["QnAStatus"] = "answer"
        userDataBase[adminId]["QnAInfo"] = f"{userId}"

        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Отмена",
            callback_data=f"QnA_cancel"
            ))

        await bot.send_message(
            adminId,
            text=f"Вы хотите отправить ответ пользователю {userName}({userId}), если это так, то отправьте сообщение, иначе нажмите 'Отмена'.",
            parse_mode="HTML",
            reply_markup=builder.as_markup()
            )

        return

    await msg.answer(userStartText)
    await msg.answer(
        f'Ты написал:\n<b>"{html.quote(str(command.args))}"</b>',
        reply_markup=startKB(),
        parse_mode="HTML"
        )
    await state.set_state(states.UserMainMenu.menu)

@router.message(Command('help'))
@loggerChat(AccessStatus.default)
async def userhelp(msg: types.Message, command: CommandObject, state: FSMContext) -> None:  
    await msg.answer(userHelpText, parse_mode="HTML")
    await state.set_state(states.UserMainMenu.menu)

@router.message(Command('zeroaccess'))
@loggerChat(AccessStatus.default)
async def zeroAccess(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    await msg.reply('Функция с нулевым уровнем доступа.')
    await state.set_state(states.UserMainMenu.menu)

@router.message(Command('moderaccess'))
@loggerChat(AccessStatus.moderator)
async def moderatorAccess(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    await msg.reply('Функция с уровнем доступа модератора.')
    await state.set_state(states.UserMainMenu.menu)

@router.message(Command('adminaccess'))
@loggerChat(AccessStatus.admin)
async def adminAccess(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    await msg.reply('Функция с уровнем доступа админа.')
    await state.set_state(states.UserMainMenu.menu)
