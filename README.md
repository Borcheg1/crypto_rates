# Приложение, позволяющее получать текущую стоимость валют
### В приложении присутствуют два файла scrap_google.py и use_api.py, работающие независимо друг от друга.
#### Описание ***scrap_google.py***:
Приложение делает запрос к сайту Google.com и получает текущую стоимость запрашиваемой валюты (переменные **main_cur** и **sec_cur**).

> Из минусов: скорость обновления стоимости валют на сайте Google.com низкая, порядка 3-5 минут.

> Из плюсов: неограниченное количество запросов, что не может предоставить API.


При изменении стоимости валюты на указанный в переменной **percent** процент по истечении времени, указанного в переменной **while_time** будет выведено
сообщение в консоль с информацией о максимальном изменении стоимости валюты.

В переменной **rate_freq** указывается количество секунд, по истечении которых будет выполнятся новый запрос для обновления текущей стоимости валюты.

#### Описание ***use_api.py***:
Приложение делает все тоже самое, за исключением выполениния запроса не к Google.com, а к сервису CoinAPI.

> Из минусов: лимитированние количество запросов.

> Из плюсов: скорость обновления стоимости валют может доходить до одного раза в секунду.

