from bot_setup import dp
from aiogram import types, Dispatcher
from data.keyboards import *
from aiogram.dispatcher.filters.state import State, StatesGroup

#
# @dp.callback_query_handler(text="new_ad")
# async def start_tracking(call: types.CallbackQuery):
#     await call.message.answer('Отправьте ссылку на поиск с сортировкой по дате')
#     await call.answer()


# @dp.callback_query_handler(text="show_ads", state=)
# async def show_all_ads(call: types.CallbackQuery):
#     user_data = await st
#     await call.message.answer('Здесь пока пусто, добавьте новое объявление, используя кнопку ниже',
#                               reply_markup=get_keyboard(1))
#     await call.answer()



