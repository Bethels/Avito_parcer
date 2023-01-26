import requests
from bs4 import BeautifulSoup
from datetime import date


def get_currency_table(day):
    url = 'https://helpix.ru/currency/'
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    columns = 10
    cells = [i.text for i in soup.find_all(class_='b-tabcurr__td')]
    cells = [cells[i] for i in range((day - 1) * columns, day * columns)]
    headers = [i.text for i in soup.find_all(class_='b-tabcurr__th')]
    result = dict(zip(headers, cells))
    return result


def update_value(shops_list: dict):
    not_updated = []
    for i in shops_list:
        if shops_list[i] == '-':
            not_updated.append(i)
    if not_updated:
        prev_day = get_currency_table(2)
        for i in not_updated:
            shops_list[i] = prev_day[i]
    return shops_list, not_updated


def check_date(shops_list: dict):
    day = 1
    if shops_list["Дата"] != str(date.today()):
        shops_list = get_currency_table(day + 1)

    return shops_list


def get_shops():
    day = 1
    date_message = ''
    shops_message = ''
    shops_list = get_currency_table(day)
    if shops_list["Дата"] != str(date.today()):
        shops_list = get_currency_table(day + 1)
        add = '(за сегодня данных еще нет)'
        # shops_list.pop("Дата")
    shops_list = dict(sorted(shops_list.items(), key=lambda x: x[1]))
    check = update_value(shops_list)
    shops_list = check[0]
    if check[1]:
        shops_message += f'Для следующих магазинов показаны данные за вчера (еще не обновились):   ' \
                         f'{", ".join(map(str, check[1]))}\n\n '
    shops_list.pop("ЦБ РФ")
    answer = f'{shops_message}И так, на {shops_list.pop("Дата")} {date_message}, самый выгодный магазин: ' \
             f'<b>{list(shops_list.keys())[0]}</b> с курсом  <b>{list(shops_list.values())[0]}</b> ₽. ' \
             f'\n\n<b>Aliexpress</b> - <b> {shops_list["Aliexpress.ru"]} </b> ₽.\n\n{central_bank()}\n\nВесь список ' \
             f'в порядке возрастания курса выглядит следующим образом:\n\n '
    for k, v in shops_list.items():
        answer += f"-{k}:  {v} ₽\n"
    return answer


def central_bank():
    day = 1
    table = get_currency_table(day)
    cb_rate = table["ЦБ РФ"]
    add = '.'
    if cb_rate == '':
        while cb_rate == '':
            day += 1
            table = get_currency_table(day)
            cb_rate = table["ЦБ РФ"]
        cb_date = table["Дата"]
        add = f'(последнее обновление за {cb_date}, скорее всего из-за выходных, ведь биржа простаивает)'

    answer = f'Курс центробанка: <b>{cb_rate}₽</b> ' + add
    return answer
