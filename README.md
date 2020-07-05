# stepik-flask-teachers
Решение заданий пятой главы курса "Flask с нуля".

Приложение для своей работы использует следующие переменные окружения:

- `FLASK_APP` - должна принимать значение `wsgi.app`.
- `FLASK_ENV` - определяет настройки плоложения, может принимать либо значение `development`, либо `production`.
- `SECRET_KEY` - секретный ключ, используемый для безопасности сессий.
- `APP_STATIC_DIR` - путь к статическим файлам приложения, должен изменяться только в случае нестандартного расположения статических файлов при деплое приложения.
- `DATABASE_URL` - URL для подключения к базе данных.
- `ORDERS_PER_PAGE` - количество заказов на одной стринице в личном кабинете пользователя, по умолчанию принимает значение 1.
- `ADMIN_ROWS_PER_PAGE` - количество строк в таблицах для административных страниц, по умолчанию принимает значение 10.

Перед запуском проложения в случае использования PostgreSQL необходимо удостовериться в том, что база данных имя которой задано в переменной окружения `DATABASE_URL` существует и она пуста.

После чего необходимо выполнить команду для запуска миграций применительно к выбранной базе данных:
```shell script
$ python -m flask db upgrade
``` 

Далее необходимо создать пользователя с правами суперпользователя для доступа к административным функциям приложения:
```shell script
$ python -m flask create-superuser
```
В результате чего будут затребованы адрес электронной почты и пароль суперпользователя.

При деплое в **Docker** необходимо сначала создать том, в котором будет располагаться файлы базы данных, посредством команды:
```shell script
$ docker volume create stepik_flask_shop_data
```
и том, в котором будут располагаться статические файлы приложения
```shell script
$ docker volume create stepik_flask_shop_static
```

Далее необходимо построить контейнеры с помощью команды
```shell script
$ docker-compose build
```
и выполнить запуск приложения
```shell script
$ docker-compose up
```

При первом запуске необходимо выполнить команду запуска миграций:
```shell script
$ docker-compose exec web python -m flask db upgrade
```

Далее необходимо создать пользователя с правами суперпользователя для доступа к административным функциям приложения:
```shell script
$ python -m flask create-superuser
```
После чего будут затребованы адрес электронной почты и пароль суперпользователя.

В результате данное приложение будет доступно посредством порта 8080.

При деплое на **Heroku** после создания приложения и связи его с GitHub необходимо проверить значение переменной окружения `DATABASE_URL`.
Помимо этого необходимо установить значения переменных окружения `FLASK_APP` и `FLASK_ENV`.

После настройки конфигурации необходимо выполнить в командной строке следующую команду для применения миграций к базе данных:
```shell script
$ heroku run python -m flask db upgrade --app=<имя приложения>
```

Далее необходимо создать пользователя с правами суперпользователя для доступа к административным функциям приложения:
```shell script
$ heroku run python -m flask create-superuser
```
В результате чего будут затребованы адрес электронной почты и пароль суперпользователя.

После чего требуется выполнить перезапуск приложения Heroku:
```shell script
$ heroku restart --app=<имя приложения>
```
