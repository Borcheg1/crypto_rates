import re
import time

import requests
from bs4 import BeautifulSoup
from art import tprint


URL = 'https://www.google.com/search?q=eth+usdt'
flag = False
max_change = None


def get_cur_value(url=URL):
    """
    Search Google for the required currency ratio and extract the value.

    :param url: link to google with search params (https://www.google.com/search?q={search_params} -> str
    :return: string with current value -> float
    """
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser').text.split('=')[1]
    current_value = re.search(r'\b\d+.+[,]\d{2}\b', soup)[0]  # Find string as "12.3456,78" or "123,45"
    current_value = float(current_value.replace('.', '').replace(',', '.'))
    return current_value


if __name__ == '__main__':
    tprint('Hello!', 'starwars')
    time.sleep(1.5)
    print("I'll tell you if the value of ETH / USDT changes by 1% or more\n")
    start_value = get_cur_value()
    time.sleep(1.5)
    date = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())
    print(f"Now {date} the value of 1 ETH is {start_value} USDT")

    while True:
        cur_time = time.time()
        start_time = time.time()
        if flag:
            start_value = save_cur_value
            max_change = None
            flag = False

        while cur_time - start_time < 3600:  # 3600
            time.sleep(60)  # 60
            cur_value = get_cur_value()
            time.sleep(5)
            change_value = round((abs(start_value - cur_value) * 100) / start_value, 2)
            if change_value > round(start_value / 100, 2):
                flag = True
                if not max_change:
                    max_change = change_value
                    change_time = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())
                    save_cur_value = cur_value
                elif max_change < change_value:
                    max_change = change_value
                    change_time = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())
                    save_cur_value = cur_value
            cur_time = time.time()
            date = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())
        else:
            if flag:
                tprint('Attention!', 'starwars')
                print(f'Maximum price change was at {change_time} by {max_change}%, the cost was {save_cur_value}')
                print(f"Now {date} the value of 1 ETH is {cur_value} USDT")
