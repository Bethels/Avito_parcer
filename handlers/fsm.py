import requests.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_setup import dp
from get_data import *


class NewAd(StatesGroup):
    waiting_for_link = State()
    waiting_for_price = State()
    waiting_for_name = State()


@dp.callback_query_handler(text="new_ad")
async def add_new_ad(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Отправьте ссылку на поиск нужного объявления с сортировкой по дате')
    await state.set_state(NewAd.waiting_for_link.state)
    await call.answer()
    user_data = await state.get_data()
    print(user_data)


@dp.message_handler(state=NewAd.waiting_for_link)
async def write_link(message: types.Message, state: FSMContext):
    try:
        get_last_ad(message.text)
    except requests.exceptions.MissingSchema:
        await message.answer('С ссылкой что-то не так, проверьте, все ли вы скопировали')
        return
    if 'https://www.avito.ru' not in message.text:
        await message.answer('Ссылка должна вести на официальный сайт Авито')
        return
    await state.update_data(link=message.text)
    await NewAd.next()
    await message.answer(
        'Теперь введите диапазон цен, от нижней границе к верхней (в рублях, через запятую. Например:\n\n 25000, 35000')


# создает лист price_range, состоящий из нижней и верхней цены
@dp.message_handler(state=NewAd.waiting_for_price)
async def write_price(message: types.Message, state: FSMContext):
    try:
        prices = [int(i) for i in message.text.replace(' ', '').split(',')]
    except ValueError:
        await message.answer('Введите цену цифрами как было показано в примере выше.')
        return
    if prices[0] > prices[1]:
        await message.answer('Видимо, вы ввели цены не в том порядке, попробуйте еще раз.')
        return
    await state.update_data(price_range=prices)
    await NewAd.next()
    await message.answer('Отлично. А теперь придумайте имя для этого трека:')


@dp.message_handler(state=NewAd.waiting_for_name)
async def write_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    await state.finish()
    print(user_data)
    await message.answer(
        f'И так, новое отслеживание "{user_data["name"]}"мы ищем {extract_name_from_url(user_data["link"])} в ценовом '
        f'диапазоне от {user_data["price_range"][0]} до {user_data["price_range"][1]}')
    await message.answer()

