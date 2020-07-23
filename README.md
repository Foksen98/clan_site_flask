# clan_site_flask
Site for LT88 clan (WoT)

## Инструкция по локальному запуску
* Активировать виртуальное окружение (в проекте используется интерпретатор Python 3.6)
`virtualenv venv -p python3 && source venv/bin/activate`
* Установить зависимости
`pip install -r requirements.txt`
* Запустить mongodb
`service mongodb start`
* Запустить сервер
`python manage.py runserver -p 8000`
* Перейти по адресу http://localhost:8000

### timestamp --> datetime
`dt.datetime.fromtimestamp(1595299456).strftime('%d.%m.%Y %H:%M'))`
