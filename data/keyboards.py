from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

buttons = [
    InlineKeyboardButton(text="Показать курс валют", callback_data="show_currency"),
    InlineKeyboardButton(text="Добавить товар для отслеживания", callback_data="new_ad"),
    InlineKeyboardButton(text="Посмотреть отслеживаемые объявления", callback_data="show_ads")
]
back_button = InlineKeyboardButton(text="Вернуться назад", callback_data="back")
cancel_button = InlineKeyboardButton(text='Отмена', callback_data="cancel")


def get_cancel_button():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    return keyboard.add(cancel_button)


def get_keyboard(
        action=0):  # 0 - вызов полной клавиатуры, 1 - не показывать курс валют, 2 - только назад, 3 - только отмена
    keyboard = InlineKeyboardMarkup(row_width=1)
    match action:
        case 0:
            keyboard.add(*buttons)
        case 1:
            keyboard.add(*buttons[1:]).add(back_button)
        case 2:
            keyboard.add(back_button)
    return keyboard

# buttons = ['Показать курс валют', 'Добавить товар для отслеживания']
# kb_client = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
# kb_client.add(*buttons)
# kb_client.add(buttons[i]) for
