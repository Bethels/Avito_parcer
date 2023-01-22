from bot_setup import dp
from aiogram import types, Dispatcher
from keyboards import *
#
# @dp.callback_query_handler(text="new_ad")
# async def start_tracking(call: types.CallbackQuery):
#     await call.message.answer('Отправьте ссылку на поиск с сортировкой по дате')
#     await call.answer()


@dp.callback_query_handler(text="show_ads")
async def show_all_ads(call: types.CallbackQuery):
    await call.message.answer('Здесь пока пусто, добавьте новое объявление, используя кнопку ниже',
                              reply_markup=get_keyboard(1))
    await call.answer()



