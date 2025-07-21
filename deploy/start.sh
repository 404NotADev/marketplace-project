#!/bin/bash

# Активируем виртуальное окружение (укажи свой путь)
source /path/to/venv/bin/activate

# Применяем миграции
python manage.py migrate

# Собираем статику
python manage.py collectstatic --noinput

# Запускаем Gunicorn
gunicorn marketplace.wsgi:application --bind 0.0.0.0:8000 --workers 3

# 1. Сделай start.sh исполняемым

# В терминале (в корне проекта):

# chmod +x deploy/start.sh

# 2. Отредактируй путь к виртуальному окружению

# В файле deploy/start.sh замени строку:

# source /path/to/venv/bin/activate

# на реальный путь к твоему виртуальному окружению. Например:

# source /home/username/venv/bin/activate

# Если виртуального окружения ещё нет — создай:

# python3 -m venv ~/venv
# source ~/venv/bin/activate
# pip install -r requirements.txt

# 3. Запусти скрипт локально для проверки

# В терминале выполни:

# ./deploy/start.sh

# Это должно:

#     активировать виртуальное окружение

#     применить миграции

#     собрать статику

#     запустить Gunicorn на 0.0.0.0:8000

# 4. Проверь, что сервер запустился

# Открой браузер по адресу:

# http://localhost:8000

# или, если это сервер — по IP сервера на порту 8000.


