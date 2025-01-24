from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import  State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import asyncio
from crud_functions import *



api='8052186009:AAH65LHw7AqMqtMfbHy_Lxh26cvBb5W39rk'
bot=Bot(token=api)
dp=Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb=ReplyKeyboardMarkup(resize_keyboard=True)
buttons1=['Рассчитать', 'Информация']
buttons2=KeyboardButton(text='Купить')
kb.add(*buttons1)
kb.add(buttons2)







kb1=InlineKeyboardMarkup(resize_keyboard=True)
kb2=InlineKeyboardMarkup(resize_keyboard=True)
button1=InlineKeyboardButton(text='Рассчитать норму калорий',callback_data='calories')
button2=InlineKeyboardButton(text='Формулы расчёта',callback_data='formulas')
button3=InlineKeyboardButton(text='Product1',callback_data='product_buying')
button4=InlineKeyboardButton(text='Product2',callback_data='product_buying')
button5=InlineKeyboardButton(text='Product3',callback_data='product_buying')
button6=InlineKeyboardButton(text='Product4',callback_data='product_buying')
kb1.add(button1)
kb1.add(button2)
kb2.row(button3, button4, button5,button6)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! я бот помогающий твоему здоровью',reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def start(message):
    await message.answer('Выберите опцию:',reply_markup=kb1)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'{i}.png', "rb") as img:
            await message.answer_photo(img,f'Название: Продукт{i} | Описание: описание {i} | Цена: {i*100}')




        await message.answer("Выберите продукт для покупки:", reply_markup=kb2)


@dp.callback_query_handler(text='product_buying')
async  def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт')



@dp.callback_query_handler(text='formulas')
async  def get_formulas(call):
    await call.message.answer('10 x вес(кг) + 6.25 x рост(см) -  x возраст(г) - 161')



@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first = message.text)
    await  message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await  message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await  state.get_data()

    await  message.answer(f"Ваша норма калорий "
                          f"{int(data['first'])*5+int(data['second'])*6.25+int(data['third'])*10-161}")

    await  state.finish()

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)