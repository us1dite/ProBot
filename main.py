import asyncio

from aiogram.filters import Command, CommandStart
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram import F

from databases.tables import create_connection

from keyboards import keyboard, keyboard1

bot = Bot(token='6417290102:AAGt-p23cTBXdKQ3ZTmw7p08JzjxH2VHTBc')
dp = Dispatcher()

TEACHERS = [5610944959]


# регистрация пользователей
@dp.message(CommandStart())
async def start(message: Message):
    conn = create_connection()
    curs = conn.cursor()

    if message.from_user.id in TEACHERS:
        teacher_id = message.from_user.id
        username = message.from_user.username
        curs.execute("INSERT INTO teachers (user_id, username, role) VALUES (?, ?, ?)", (user_id, username, role))

        await message.answer("Добро пожаловать в бота по напоминаниям и уведомлениям. Вы зарегестрированы как учитель", reply_markup=keyboard1)

    elif message.from_user.id not in TEACHERS:
        user_id = message.from_user.id
        username = message.from_user.username
        role = 'student'
        curs.execute("INSERT INTO users (user_id, username, role) VALUES (?, ?, ?)", (user_id, username, role))

        await message.answer("Добро пожаловать в бота по напоминаниям и уведомлениям. Вы зарегестрированы как ученик", reply_markup=keyboard)

    conn.commit()
    conn.close()

@dp.message(F.text == "Записаться на занятие", "Я заболел")
async def pupil_funcs(message: Message):
    conn = create_connection()
    curs = conn.cursor()

    if message.text == "Записаться на занятие":
        await message.answer("На какую специальность вы хотите записаться?")
    elif "Я заболел":
       curs.execute("""
            SELECT teacher_id FROM users_and_teachers WHERE user_id = ?
    """, (message.from_user.id))
       teachers = curs.fetchall()
       for teacher_id in teachers:
           await bot.send_message(teacher_id, f"kldajglkajgklj")
       await message.answer("Мы проинформируем учителя об этом")

    conn.commit()
    conn.close()

def is_teacher(user_id):
    conn = create_connection()
    curs = conn.cursor()

    curs.execute("""
        SELECT role FROM users WHERE user_id = ?
    """, (user_id))

    user = curs.fetchone()
    conn.close()
    return user and user[0] == 'teacher'




async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())