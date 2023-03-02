import re
import time

import requests
from bs4 import BeautifulSoup
from art import tprint


main_cur = 'ETH'  # currency code (ISO 4217) of which you want to know the value
sec_cur = 'USDT'  # currency code (ISO 4217) for calculating the main
while_time = 3600  # After these seconds, a message will be displayed in the console if the price changes by more than 1%
rate_freq = 20  # Frequency of requesting a new rate (seconds)
percent = 1  # Percentage, when changing the rate by this percentage, a message will be displayed in the console
URL = f'https://www.google.com/search?q={main_cur}+{sec_cur}'
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
    print(f"I'll tell you if the value of {main_cur} / {sec_cur} changes by {percent}% or more within an {round(while_time / 60, 1)} minutes\n")
    start_value = get_cur_value()
    time.sleep(1.5)
    date = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())
    print(f"Now {date} the value of 1 {main_cur} is {start_value} {sec_cur}\n")

    while True:
        cur_time = time.time()
        start_time = time.time()
        if flag:
            start_value = save_cur_value
            max_change = None
            flag = False

        while cur_time - start_time < while_time:
            time.sleep(rate_freq)
            cur_value = get_cur_value()
            time.sleep(5)
            change_value = round((abs(start_value - cur_value) * 100) / start_value, 2)
            if change_value > round(start_value * (percent / 100), 2):
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
                print(f'Maximum price changed at {change_time} by {max_change}%, the cost was {save_cur_value}\n')
                print(f"Now {date} the value of 1 {main_cur} is {cur_value} {sec_cur}\n")
