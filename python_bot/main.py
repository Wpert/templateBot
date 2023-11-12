from logic.core import *
from logic import *

import asyncio

from aiogram.filters.command import Command

# регистрируем команды пользователя
from logic.handlers import user_cmd
dp.include_router(user_cmd.router)

# регистрируем qna блок
from logic.handlers import qna_cmd
dp.include_router(qna_cmd.router)

# регистрируем команды админа
from logic.handlers import admin_cmd
dp.include_router(admin_cmd.router)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())