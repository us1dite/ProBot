import asyncio

from aiogram.filters import Command, CommandStart
from aiogram import Bot, Dispatcher
from aiogram.types import Message

bot = Bot(token='6417290102:AAGt-p23cTBXdKQ3ZTmw7p08JzjxH2VHTBc')
dp = Dispatcher()

TEACHERS = [5610944959]

@dp.message(CommandStart())
async def start(message: Message):
    if message.from_user.id in TEACHERS:
        await message.answer("Добро пожаловать в бота по напоминаниям и уведомлениям. Вы зарегестрированы как учитель")
    elif message.from_user.id not in TEACHERS:
        await message.answer("Добро пожаловать в бота по напоминаниям и уведомлениям. Вы зарегестрированы как ученик")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
