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


def get_shops():
    day = 1
    add = ''
    shops = get_currency_table(day)
    if shops["Дата"] != str(date.today()):
        shops = get_currency_table(day + 1)
        add = '(за сегодня данных еще нет)'
        # shops.pop("Дата")
    shops = dict(sorted(shops.items(), key=lambda x: x[1]))
    shops.pop("ЦБ РФ")
    answer = f'И так, на {shops.pop("Дата")} {add}, самый выгодный магазин: <b>{list(shops.keys())[0]}</b> с курсом ' \
             f'<b>{list(shops.values())[0]}</b> ₽. \n\n<b>Aliexpress</b> - <b> {shops["Aliexpress.ru"]}' \
             f'</b> ₽.\n\n{central_bank()}\n\nВесь список в порядке возрастания курса выглядит следующим образом:\n\n'
    for k, v in shops.items():
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

    answer = f'Курс центробанка составляет {cb_rate}₽ ' + add
    return answer