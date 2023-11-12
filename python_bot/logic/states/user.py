from aiogram.fsm.state import State, StatesGroup


class UserMainMenu(StatesGroup):
    """Состояния пользователей вашего бота
    
    menu -- пользователь в главном меню
    question -- пользователь спрашивает вопрос
    answer -- админ отвечает на вопрос
    """

    menu = State()
    question = State()
    answer = State()
