import asyncio

from aiogram.filters import Command, CommandStart
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from databases.tables import create_connection, create_tables

from keyboards import keyboard1, keyboard, kbrd_pupil

bot = Bot(token='6417290102:AAGt-p23cTBXdKQ3ZTmw7p08JzjxH2VHTBc')
dp = Dispatcher()

class STATES(StatesGroup):
    cancel_less = State()
    update_class = State()
    update_class1 = State()
    update_room = State()
    update_time = State()
    update_time1 = State()

TEACHERS = [5610944959, 852523963]
GROUPS = {
    5: "Биологическая школа «Биосфера»",
    6: "Биология для знатаков. 9 класс",
    7: "Биология с основами генетикой",
    8: "Химия. Старт в науку",
    9: "Олимпиадная химия для старшеклассников",
    10: "Современная энергетика",
    11: "Информатика. Юниоры",
    12: "Информатика",
    13: "Умники и Умницы",
    14: "Общая химия",
    15: "Онлайн-школа по информатике",
    16: "Онлайн-школа по математике",
    17: "Олимпиадный математический тренинг",
    18: "Тренинг по физике",
    19: "Шахматы. Совершенство мастерства",
    20: "Основы классического танца",
    21: "Студия ювелирного дизайна",
    22: "Юные дизайнеры",
    23: "Эстрадный ансамбль",
    24: "Основы рисунка и живописи",
    25: "Основы графического дизайна",
    26: "Проектный тренинг по химии и нанотехнологиям",
    27: "В такт с музыкой",
    28: "Цирковая студия «Арлекино»"

}

create_tables()

print(GROUPS.keys())

conn = create_connection()
curs = conn.cursor()

curs.execute("SELECT * FROM groups")
groups = curs.fetchall()
print(groups)
if groups == []:
    for item in GROUPS.items():
        curs.execute(f"""
            INSERT INTO groups
            (id, name)
            VALUES (?, ?)
            """, item)

conn.commit()
conn.close()

@dp.message(CommandStart())
async def start(message: Message):
    conn = create_connection()
    curs = conn.cursor()

    if message.from_user.id in TEACHERS:
        user_id = message.from_user.id
        username = message.from_user.username
        curs.execute("INSERT INTO teachers (user_id, username) VALUES (?, ?)", (user_id, username))
        await message.answer("Добро пожаловать в бота по напоминаниям и уведомлениям. Вы зарегестрированы как учитель", reply_markup=keyboard1)

    elif message.from_user.id not in TEACHERS:
        user_id = message.from_user.id
        username = message.from_user.username
        role = 'student'
        curs.execute("INSERT INTO users (user_id, username, role) VALUES (?, ?, ?)", (user_id, username, role))

        await message.answer("Добро пожаловать в бота по напоминаниям и уведомлениям. Вы зарегестрированы как ученик", reply_markup=keyboard)

    conn.commit()
    conn.close()

@dp.message(F.text=='Записаться на занятие')
async def add_fak(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Да, готов",
        callback_data="next")
    builder.button(
        text="Нет, не готов",
        callback_data="cancel")
    builder.adjust(1)
    await message.answer(
        "Ты готов выбрать факультет?",
        reply_markup=builder.as_markup()
    )


def name_of_group(group_id):
    conn = create_connection()
    curs = conn.cursor()

    name = curs.execute("""
        SELECT name
        FROM groups
        WHERE id = ?
    """, [group_id]).fetchone()[0]

    conn.commit()
    conn.close()
    
    return name

def id_of_group(name):
    conn = create_connection()
    curs = conn.cursor()

    id = curs.execute("""
        SELECT id
        FROM groups
        WHERE name = ?
    """, [name]).fetchone()[0]

    conn.commit()
    conn.close()
    
    return id
    

@dp.message(F.text=='Изменить дату/время')
async def update_data(message: Message, state: FSMContext):
    await state.set_state(STATES.update_time)
    await message.answer("Введите название занятия дату/время которого вы хотите изметить")
    for item in GROUPS.values():
        await message.answer(item)

@dp.message(STATES.update_time)
async def update_data(message: Message, state: FSMContext): 
    if message.text in GROUPS.values():
        await state.update_data(name=message.text)
        name = message.text
        id = id_of_group(name)

        conn = create_connection()
        curs = conn.cursor()

        curs.execute("""
            SELECT user_id
            FROM user_groups
            WHERE group_id = ?
        """, [id])

        global ides_time
        ides_time = curs.fetchall()
        
        await state.set_state(STATES.update_time1)
        await message.answer("Введите время/дату на которое хотите изменить занятие")

        conn.commit()
        conn.close()

@dp.message(STATES.update_time1)
async def update_data1(message: Message, state: FSMContext):
    await state.update_data(number_room = message.text)
    data = await state.get_data()

    for user in ides_time:
        await message.bot.send_message(user[0], f"Занятие {data['name']} было перенесено на {message.text}")

    await message.answer(f"Вы перенесли занятие {data['name']} на {message.text}")

    await state.clear()


@dp.message(F.text=='Изменить кабинет')
async def update_data(message: Message, state: FSMContext):
    await state.set_state(STATES.update_class)
    await message.answer("Введите название занятия кабинет которого вы хотите изменить:")
    for item in GROUPS.values():
        await message.answer(item)
    await message.answer(str(item))

@dp.message(STATES.update_class)
async def update_data(message: Message, state: FSMContext): 
    if message.text in GROUPS.values():
        await state.update_data(name=message.text)
        name = message.text
        id = id_of_group(name)

        conn = create_connection()
        curs = conn.cursor()

        curs.execute("""
            SELECT user_id
            FROM user_groups
            WHERE group_id = ?
        """, [id])

        global ides
        ides = curs.fetchall()
        
        await state.set_state(STATES.update_class1)
        await message.answer("Введите кабинет на который хотите изменить")

        conn.commit()
        conn.close()

@dp.message(STATES.update_class1)
async def update_data1(message: Message, state: FSMContext):
    await state.update_data(number_room = message.text)
    data = await state.get_data()

    for user in ides:
        await message.bot.send_message(user[0], f"Занятие {data['name']} было перенесено в кабинет {message.text}")

    await message.answer(f"Вы перенесли занятие {data['name']} в кабинет {message.text}")

    await state.clear()

@dp.message(F.text=='Отменить занятие')
async def update_data(message: Message, state: FSMContext):
    await state.set_state(STATES.cancel_less)
    await message.answer("Введите название занятия которое вы хотите отменить:")
    for item in GROUPS.values():
        await message.answer(item)


@dp.message(STATES.cancel_less)
async def teacher_commands(message: Message, state: FSMContext):
    if message.text in GROUPS.values():
        name = message.text
        id = id_of_group(name)

        conn = create_connection()
        curs = conn.cursor()

        curs.execute("""
            SELECT user_id
            FROM user_groups
            WHERE group_id = ?
        """, [id])

        for user in curs.fetchall():
            await message.bot.send_message(user[0], f'Занятие "{name} было отменено')

        await message.answer(f'Вы отменили занятие "{name}"')
        
        await state.clear()

        conn.commit()
        conn.close()



@dp.message(Command("1"))
async def krug(message: types.Message):
    ...

@dp.callback_query(F.data.split()[0] == "accept")
async def send_random_value(callback: types.CallbackQuery):
    conn = create_connection()
    curs = conn.cursor()
    
    curs.execute(f"""
        INSERT INTO user_groups 
        (user_id, group_id)
        VALUES ({callback.from_user.id}, {callback.data.split()[1]})
""")

    new = ReplyKeyboardMarkup(keyboard=kbrd_pupil, resize_keyboard=True, one_time_keyboard=True)
    await callback.message.delete()
    await callback.message.answer("Вы были приняты", reply_markup=new)

    conn.commit()
    conn.close()

@dp.callback_query(F.data == "cancel")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.edit_text('Уточни названия программы у педагога и возвращайся к нам')

@dp.callback_query(F.data == "group")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="1 группа",
        callback_data="accept 1")
    builder.button(
        text="2 группа",
        callback_data="accept 2")
    builder.adjust(1)
    await callback.message.edit_text('Выберите группу, в которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "group_tan")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Основной состав",
        callback_data="accept 3")
    builder.button(
        text="Младшая группа",
        callback_data="accept 4")
    builder.adjust(1)
    await callback.message.edit_text('Выберите группу, в которой обучаетесь', reply_markup=builder.as_markup())


@dp.callback_query(F.data == "next")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Биологическая школа «Биосфера»",
        callback_data="accept 5")
    builder.button(text="Биология для знатаков. 9 класс",
        callback_data="accept 6")
    builder.button(text="Далее",
        callback_data="next2")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next2")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Биология с основами генетикой",
        callback_data="accept 7")
    builder.button(
        text="Химия. Старт в науку",
        callback_data="accept 8")
    builder.button(
        text="Далее",
        callback_data="next3")
    builder.button(
        text="Назад",
        callback_data="next")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next3")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Олимпиадная химия для старшеклассников",
        callback_data="accept 9")
    builder.button(
        text="Современная энергетика",
        callback_data="accept 10")
    builder.button(
        text="Далее",
        callback_data="next4")
    builder.button(
        text="Назад",
        callback_data="next2")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next4")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Основы графического дизайна",
        callback_data="accept 25")
    builder.button(
        text="Информатика. Юниоры",
        callback_data="accept 11")
    builder.button(
        text="Далее",
        callback_data="next5")
    builder.button(
        text="Назад",
        callback_data="next3")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next5")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Информатика",
        callback_data="accept 12")
    builder.button(
        text="Проектный тренинг по химии и нанотехнологиям",
        callback_data="accept 26")
    builder.button(
        text="Далее",
        callback_data="next6")
    builder.button(
        text="Назад",
        callback_data="next4")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next6")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Умники и Умницы",
        callback_data="accept 13")
    builder.button(
        text="Общая химия",
        callback_data="accept 14")
    builder.button(
        text="Далее",
        callback_data="next7")
    builder.button(
        text="Назад",
        callback_data="next5")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next7")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Онлайн-школа по информатике",
        callback_data="accept 15")
    builder.button(
        text="Онлайн-школа по математике",
        callback_data="accept 16")
    builder.button(
        text="Далее",
        callback_data="next8")
    builder.button(
        text="Назад",
        callback_data="next6")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next8")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Олимпиадный математический тренинг",
        callback_data="accept 17")
    builder.button(
        text="Тренинг по физике",
        callback_data="accept 18")
    builder.button(
        text="Далее",
        callback_data="next9")
    builder.button(
        text="Назад",
        callback_data="next7")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next9")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Шахматы. Совершенство мастерства",
        callback_data="accept 19")
    builder.button(
        text="Основы классического танца",
        callback_data="accept 20")
    builder.button(
        text="Далее",
        callback_data="next10")
    builder.button(
        text="Назад",
        callback_data="next8")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next10")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="В такт с музыкой",
        callback_data="accept 27")
    builder.button(
        text="Цирковая студия «Арлекино»",
        callback_data="accept 28")
    builder.button(
        text="Далее",
        callback_data="next11")
    builder.button(
        text="Назад",
        callback_data="next9")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next11")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Студия ювелирного дизайна",
        callback_data="accept 21")
    builder.button(
        text="Юные дизайнеры",
        callback_data="accept 22")
    builder.button(
        text="Далее",
        callback_data="next12")
    builder.button(
        text="Назад",
        callback_data="next10")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())

@dp.callback_query(F.data == "next12")
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Эстрадный ансамбль",
        callback_data="accept 23")
    builder.button(
        text="Основы рисунка и живописи",
        callback_data="accept 24")
    builder.button(
        text="Назад",
        callback_data="next11")
    builder.adjust(1)
    await callback.message.edit_text('Выберите программу, на которой обучаетесь', reply_markup=builder.as_markup())
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())