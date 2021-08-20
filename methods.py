from lxml import etree
import requests
from datetime import datetime

def get_xml(url):
    try:
        list_of_curriencies_xml = requests.get(url)
        list_of_curriencies_xml.raise_for_status()
        return list_of_curriencies_xml.text
    except(requests.RequestException, ValueError):
        print("Сервис Банка России недоступен")
        return False

def get_curriencies():
    url = "http://www.cbr.ru/scripts/XML_valFull.asp"
    if get_xml(url):
        list_of_curriencies_xml = get_xml(url)
        root = etree.fromstring(bytes(list_of_curriencies_xml, encoding='windows-1251'))
        curriencies = {}
        for curriency in root:
            curriencies[curriency[5].text] = curriency[0].text
        return curriencies

def get_exchange_rate(char_code, first_date, second_date):
    try:
        first_date = datetime.strptime(first_date, "%Y.%m.%d")
        first_date = datetime.strftime(first_date, "%d/%m/%Y")
        second_date = datetime.strptime(second_date, "%Y.%m.%d")
        second_date = datetime.strftime(second_date, "%d/%m/%Y")
    except(ValueError):
        return "Дата должна быть в формате YYYY.mm.dd"
    url_for_first_date = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={first_date}"
    url_for_second_date = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={second_date}"
    first_date_exchange_rate = 0
    second_date_exchange_rate = 0
    if get_xml(url_for_first_date) and get_xml(url_for_second_date):
        first_date_exchange_rate_xml = etree.fromstring(bytes(get_xml(url_for_first_date), encoding='windows-1251'))
        for element in first_date_exchange_rate_xml:
            if element[1].text == char_code:
                first_date_exchange_rate = float(element[4].text.replace(",","."))
                break
            else:
                first_date_exchange_rate = None
        second_date_exchange_rate_xml = etree.fromstring(bytes(get_xml(url_for_second_date), encoding='windows-1251'))
        for element in second_date_exchange_rate_xml:
            if element[1].text == char_code:
                second_date_exchange_rate = float(element[4].text.replace(",","."))
                break
            else:
                second_date_exchange_rate = None
        if first_date_exchange_rate is None or second_date_exchange_rate is None:
            return f"Валюта {char_code} не найдена"
        difference = abs(first_date_exchange_rate - second_date_exchange_rate)
        return f"""Курс RUB относительно {char_code} на {first_date} составляет {first_date_exchange_rate}\nКурс RUB относительно {char_code} на {second_date} составляет {second_date_exchange_rate}\nРазность составила {round(difference, 3)}"""

# print(get_echange_rate("GBP", "2021.08.19", "2021.08.20"))