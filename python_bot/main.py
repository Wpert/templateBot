from logic.core import *
from logic import *

import asyncio

# регистрируем команды
from logic.handlers import user_cmd
from logic.handlers import qna_cmd
from logic.handlers import admin_cmd
dp.include_router(user_cmd.router)
dp.include_router(qna_cmd.router)
dp.include_router(admin_cmd.router)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
