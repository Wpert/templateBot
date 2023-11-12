from typing import List, Dict

from aiogram import types, Router
from aiogram.filters import Command, CommandObject, Text
from aiogram.fsm.context import FSMContext

from logic import states
from logic.texts import qnaSendText
from logic.chat_logger import *

from logic import qnaChat_id, adminAnswers, userDataBase, dp
from logic.keyboards import startKB, qnaDefaultKB, qnaChooseAnswerKB, qnaAnswerKB

router = Router()

@router.message(Text("Задать вопрос"))
@router.message(Command('question'))
@loggerChat(AccessStatus.default)
async def startQuestion(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    """Старт обработки вопроса от пользователя после регистрации команды /question"""
    await msg.answer(
        "Следующим сообщением введите свой вопрос.",
        reply_markup=types.ReplyKeyboardRemove()
        )
    await state.set_state(states.UserMainMenu.question)

@router.message(
        states.UserMainMenu.question
)
@loggerChat(AccessStatus.default)
async def makeQuestion(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    """Отправка вопроса на рассмотрение модераторами

    Отправляем сообщение пользователю, меняем состояние пользователя
    Отправляем сообщение в чат QnA, добавляем к сообщению кнопки
    """
    await msg.reply(
        "Вопрос принят на рассмотрение.",
        reply_markup=startKB(),
        parse_mode="HTML"
        )

    await state.set_state(states.UserMainMenu.menu)

    # Дальше сообщение отсылается в чат QnA

    await bot.send_message(
        qnaChat_id,
        text=qnaSendText.format(
            msg.message_id,
            msg.from_user.username,
            msg.from_user.id,
            userDataBase[msg.from_user.id]['status'],
            msg.text
            ),
        parse_mode="HTML",
        )

    await bot.send_message(
        qnaChat_id,
        text="Ответил(-а): None",
        parse_mode="HTML",
        reply_markup=qnaDefaultKB(msg.from_user.id)
        )

@dp.callback_query(Text(startswith="QnA_"))
@loggerChat(AccessStatus.moderator)
async def callbacks_qna(callback: types.CallbackQuery, command: CommandObject, state: FSMContext):
    """Обработка вопроса от пользователя в чате qna"""
    cbData = callback.data.split("_")

    if cbData[1] == "answer":
        await callback.message.edit_text(
            f"Ответил(-а): {callback.from_user.username}",
            reply_markup=qnaChooseAnswerKB(int(cbData[2]))
        )
        await state.set_state(states.UserMainMenu.answer)

    elif cbData[1] == "edit":
        await callback.answer(text="Напишите новое сообщение.")

    elif cbData[1] == "send":
        adminId: int = int(cbData[2])

        ansInfo: List[str] = userDataBase[adminId]["QnAInfo"].split("_")
        userId: int = int(ansInfo[0])

        await bot.send_message(
            userId,
            text=("Вам пришёл ответ на вопрос:\n\n" + adminAnswers[adminId]),
            parse_mode="HTML")

        del adminAnswers[adminId]

        await callback.answer(text="Сообщение отправлено пользователю.")
        await state.set_state(states.UserMainMenu.menu)

    elif cbData[1] == "cancel":
        await callback.answer(text="Отмена успешно произошла.")
        await state.set_state(states.UserMainMenu.menu)

    await callback.answer()

@router.message(
    states.UserMainMenu.answer
    )
@loggerChat(AccessStatus.moderator)
async def answerQuestionText(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    """Переспрашиваем хотим ли отправить ЭТУ версию текста или поменять её"""
    adminId: int = msg.from_user.id
    questionAnswer: str = msg.text

    adminAnswers[adminId] = questionAnswer

    await msg.answer(
        text=("Вы точно хотите отправить это сообщение?\n\n" + questionAnswer),
        parse_mode="HTML",
        reply_markup=qnaAnswerKB(adminId))
