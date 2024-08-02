import asyncio

from aiogram import Bot, Dispatcher

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

dp = Dispatcher()

kbrd_pupil = [
        [KeyboardButton(text="Записаться на занятие")]
    ]

kbrd_teacher = [
    [KeyboardButton(text="Изменить дату/время"), KeyboardButton(text="Отменить занятие")],
    [KeyboardButton(text="Изменить кабинет")]
]

keyboard = ReplyKeyboardMarkup(keyboard=kbrd_pupil, resize_keyboard=True, one_time_keyboard=True)
keyboard1 = ReplyKeyboardMarkup(keyboard=kbrd_teacher, resize_keyboard=True, one_time_keyboard=True)


