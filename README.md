# Foodgram Project
## Описание
Сайт «Продуктовый помощник».

Онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Стек
Сайт написан на Python 3, с использованием фрейморвка Django 3. База данных на PostgreSQL. 

Шаблоны страниц на HTML с использованием CSS и JavaScript.

Сайт развернут на сервисе Яндекс.Облако в контейнерах Docker с использованием nginx и gunicorn.

## Запуск проекта локально
На локальном компьютере должен быть установлен Docker.

1. Склонировать данный репозиторий на свой локальный компьютер.
2. В директории ./foodgram_project создать файл .env и прописать в нем переменные окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_PASSWORD=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<секретный ключ Django проекта>
EMAIL_HOST_USER=<почтовый сервер>
EMAIL_HOST_PASSWORD=<пароль от почтового сервера>
```
3. В терминале в корневой директории приложения выполнить команду `docker-compose up`.
4. После запуска контейнера в новой вкладке терминала выполнить команду `docker exec -it foodgram-project_web_1 bash`.
5. Внутри контейнера выполнить команды `python manage.py migrate` и `python manage.py collectstatic`.

Сайт будет доступен на локальном сервере - http://localhost/
