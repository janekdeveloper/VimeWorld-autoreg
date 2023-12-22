# -*- coding: utf8 -*-
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from vimeautoreg.reger import RegistrationRequest

API_TOKEN = '' # TELEGRAM BOT API TOKEN
CAPMONSTER_KEY = '' # CAPMONSTER API KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
	name = State()
	age = State()
	gender = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	await message.answer('Привет! Нажми кнопку ниже и я создам для тебя новый аккаунт на VimeWorld.com',
						 reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/create 9')))


@dp.message_handler(commands=['create'])#(text='Получить новый аккаунт')
async def create_account_bot(message: types.Message):
	arguments = message.get_args().split()
	num_accounts = int(arguments[0])
	await message.answer('Приступил к созданию аккаунта, ожидайте')
	acc = RegistrationRequest(_client_key=CAPMONSTER_KEY).register_account(numlet=num_accounts, passlength=15)
	await message.answer(acc, parse_mode='HTML', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Получить новый аккаунт')))
	with open('gen.txt', 'a') as file:
		file.write(acc + '\n')
		file.close()



if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)