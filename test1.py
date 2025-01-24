import logging

from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import  State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import asyncio
from config import *
from keyboards import *
from admin import *
from db import *
import text



logging.basicConfig(level=logging.INFO)
bot=Bot(token=api)
dp=Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Hello, {message.from_user.username}'+ text.start,reply_markup=start_kb)

#message.answer_photo
#message.answer_video
#message.answer_file

@dp.message_handler(text = 'О нас')
async def price(message):
    with open('4.png',"rb") as img:
        await message.answer_photo(img,text.about,reply_markup=start_kb)


@dp.message_handler(text = 'cost')
async def price(message):
    await message.answer('Что вас интересует',reply_markup=catalog_kb)

@dp.callback_query_handler(text='small')
async def buy1(call):
    await  call.message.answer(text.game1, reply_markup = buy_kb)
    await call.answer()

@dp.callback_query_handler(text='medium')
async def buy2(call):
    await  call.message.answer(text.price2, reply_markup = buy_kb)
    await call.answer()

@dp.callback_query_handler(text='big')
async def buy3(call):
    await  call.message.answer(text.price3, reply_markup = buy_kb)
    await call.answer()



@dp.callback_query_handler(text='other')
async  def buy_other(call):
    await call.message.answer(text.other, reply_markup = buy_kb)
    await call.answer()

@dp.callback_query_handler(text='back to catalog')
async  def back(call):
    await call.message.answer('Что вас интересует',reply_markup=catalog_kb)
    await call.answer()





if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)