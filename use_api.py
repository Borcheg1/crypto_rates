import time
from configparser import ConfigParser

import requests
from art import tprint


conf = ConfigParser()
conf.read('config.ini')
key = conf['keys']['api_key']

main_cur = 'ETH'  # currency code (ISO 4217) of which you want to know the value
sec_cur = 'USDT'  # currency code (ISO 4217) for calculating the main
while_time = 60  # After these seconds, a message will be displayed in the console if the price changes by more than 1%
rate_freq = 20  # Frequency of requesting a new rate (seconds)
percent = 0.7  # Percentage, when changing the rate by this percentage, a message will be displayed in the console

url = f'https://rest.coinapi.io/v1/exchangerate/{main_cur}/{sec_cur}'
headers = {
    'X-CoinAPI-Key': key
}
flag = False
max_change = None


def get_cur_value(url=url):
    """
    Request to api and get currency rate.

    :param url: link to api -> str
    :return: current rate -> float
    """
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        raise Exception('\nPlease try again!\n')
    while response.status_code != [200, 201, 202]:
        response = requests.get(url, headers=headers)
        time.sleep(10)
    else:
        data = response.json()
        current_value = round(data['rate'], 2)
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
            time.sleep(1)
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
                print(f'Maximum price change was at {change_time} by {max_change}%, the cost was {save_cur_value}\n')
                print(f"Now {date} the value of 1 {main_cur} is {cur_value} {sec_cur}\n")
