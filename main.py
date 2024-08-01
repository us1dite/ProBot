import asyncio

from aiogram.filters import Command, CommandStart
from aiogram import Bot, Dispatcher
from aiogram.types import Message

bot = Bot(token='')
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Добро пожаловать в бота по напоминаниям и уведомлениям")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())