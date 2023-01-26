from bot_setup import dp
from aiogram import types
from data.keyboards import *
import data.get_currency as get_currency



def display_main():
    greetings = 'Я могу присылать свежие объявления с Aвито по заданным параметрам, а так же выводить курс рубля в ' \
                'популярных онлайн-магазинах. \n\nДля продолжения, выберите нужную команду ниже: '
    return greetings
@dp.message_handler(commands=['start', 'help'])
async def start_menu(message: types.Message):
    await message.answer(display_main(), reply_markup=get_keyboard())


@dp.callback_query_handler(text="show_currency")
async def show_currency(call: types.CallbackQuery):
    # await call.message.answer(get_data.get_shops(), parse_mode=types.ParseMode.HTML, reply_markup=get_keyboard(1))
    await call.message.edit_text(get_currency.get_shops(), parse_mode=types.ParseMode.HTML,
                                 reply_markup=get_keyboard(2))
    await call.answer()


@dp.callback_query_handler(text="back")
async def get_back(call: types.CallbackQuery):
    await call.message.edit_text(display_main(), reply_markup=get_keyboard())


