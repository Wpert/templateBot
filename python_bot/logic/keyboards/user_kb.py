from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
# тут планируется расположить клавиатуру после команды старт, но пока мне так лень....
# надо бы вообще к qna приступить

def startKB():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Первая кнопка"),
        types.KeyboardButton(text="Вторая кнопка")
    )
    builder.row(
        types.KeyboardButton(text="Задать вопрос")
    )
    builder.row(
        types.KeyboardButton(text="Четвертая кнопка"),
        types.KeyboardButton(text="Пятая кнопка")
    )

    return builder.as_markup()


def qnaDefaultKB(userId: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Взяться за ответ",
            callback_data=f"QnA_answer_{userId}",
            )
    )
    
    return builder.as_markup()

def qnaChooseAnswerKB(userId: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Ответить анонимно",
            url=f"https://t.me/latexMEPhI_bot?start={userId}"
            ),
        types.InlineKeyboardButton(
            text="Ответить в личку",
            url=f"tg://user?id={userId}"
            )
    )

    return builder.as_markup()

def qnaAnswerKB(adminId: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Переписать ответ",
            callback_data=f"QnA_edit",
            ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Отправить ответ",
            callback_data=f"QnA_send_{adminId}",
            ),
    )
    
    return builder.as_markup()

