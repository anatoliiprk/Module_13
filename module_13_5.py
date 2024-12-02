from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weigth = State()

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button1 = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
kb.row(button1, button2)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = 'Рассчитать')
async def set_gender(message):
    await message.answer('Введите свой пол (м/ж)')
    await UserState.gender.set()

@dp.message_handler(state = UserState.gender)
async def set_age(message, state):
    await state.update_data(gender = message.text)
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weigth(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес')
    await UserState.weigth.set()

@dp.message_handler(state = UserState.weigth)
async def send_calories(message, state):
    await state.update_data(weigth = message.text)
    data = await state.get_data()
    a = int(data['age'])
    g = int(data['growth'])
    w = int(data['weigth'])
    calories = 0
    if data['gender'] == 'м':
        calories = 10 * w + 6.25 * g - 5 * a + 5
    else:
        calories = 10 * w + 6.25 * g - 5 * a - 161
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

