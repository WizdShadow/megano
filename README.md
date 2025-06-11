Перед запуска приложение ОБЕЗАТЕЛЛЬНО ВЫПОЛНИТЕ ЭТИ УСЛОВИЯ:

1. Установить зависимости
    
    1.1 pip install megano/megano/diploma_frontend/dist/diploma-frontend-0.6.tar.gz

    1.2 pip install -r megano/reg.txt

2. Устноавить тестовые данные для БАЗЫ

    sqlite3 megano/megano/db.sqlite3 < megano/megano/date.sql

3. Запуск приложения

    python megano/megano/manage.py runserver


ПРИМЕЧАНИЕ

Данные тестовый пользователь данные:

Login: DesGun
Password: test