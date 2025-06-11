Запуск проекта на локальном компьютере

Перед запуска приложение ОБЕЗАТЕЛЛЬНО ВЫПОЛНИТЕ ЭТИ УСЛОВИЯ:


1. Установить зависимости
    
    pip install megano/megano/diploma_frontend/dist/diploma-frontend-0.6.tar.gz

    pip install -r megano/reg.txt

2. Устноавить тестовые данные для БАЗЫ

    sqlite3 megano/megano/db.sqlite3 < megano/megano/date.sql

3. Запуск приложения

    python megano/megano/manage.py runserver