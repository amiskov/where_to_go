# Where to Go
Сайт про интересные места на карте:

- [Рабочая версия](http://v1131340.hosted-by-vdsina.ru:5001).
- [Панель администратора](http://v1131340.hosted-by-vdsina.ru:5001/admin) (логин и пароль отправлен в сообщении к ревью).

## Установка и запуск
Этот раздел актуален и для локальной разработки и для деплоя.

Склонируйте репозиторий и запустите установку через [Poetry](https://python-poetry.org):

```sh
# для локальной разработки
poetry install

# для прода, без вспомогательных зависимостей
poetry install --without dev
```

Создайте файл `.env` со следующими параметрами:

```ini
DEBUG=False # True для локальной разработки
SECRET_KEY='...'
ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1,... # добавьте ваш домен или IP
LOGGING_CONFIG_FILE=logging.ini # опционально
```

- `DEBUG=True` включает режим отладки: Django будет выводить подробные сообщения об ошибках прямо в браузере. Критически важно [при деплое указать](https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-DEBUG) `DEBUG=False`. По умолчанию установлен в `False.`
- `SECRET_KEY` - уникальный набор символов, используется при генерации кук, токенов и пр. важных для безопасности сущностей. сгенерировать его [можно так](https://stackoverflow.com/a/57678930). Указать нужно обязательно, без него сайт не запустится.
- `ALLOWED_HOSTS` - хосты (домены или IP), которые может обслуживать данный сайт. Указание конкретных разрешённых хостов важно для предотвращения некоторых видов атак, параметр обязателен для заполнения для обслуживания любых клиентов, отличных от `localhost`.
- `LOGGING_CONFIG_FILE` - путь к [файлу с дополнительными настройками логгера](https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig) относительно корня проекта. В этом файле можно расширить настройки логирования Django по-умолчанию.

Пример файла `logging.ini` с дополнительной конфигурацией логирования:

```ini
[loggers]
keys=root

[handlers]
keys=fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=fileHandler

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=("file.log",)

[formatter_simpleFormatter]
format=%(asctime)s %(name)s - %(levelname)s:%(message)s
```

Запустите миграции:

```sh
poetry run python manage.py migrate
```

Создайте главного администратора:

```sh
poetry run python manage.py createsuperuser
```

## Запуск для разработки
Запустите встроенный Джанго-сервер:

```sh
poetry run python manage.py runserver
```

## Запуск на сервере
На сервере сайт работает на [Gunicorn](https://gunicorn.org) с реверс-прокси через Nginx.

Рекомендуемый порядок действий после выполнения команд из раздела «Установка и запуск»:

```sh
# собрать статику
poetry run python manage.py collectstatic

# узнать путь к Python-окружению проекта (Executable в выводе)
poetry env info
# ...
# Executable: /home/USERNAME/.../bin/python
# ...
```

Запустить Django-приложение через Gunicorn следующей командой, которую для удобства мы сохраним в файле `start.sh` в директории проекта:

```sh
#!/usr/bin/env bash
/home/USERNAME/.../bin/python \
    -m gunicorn -w 3 \
    --chdir /var/www/projects/where_to_go \
    -b localhost:5551 \
    where_to_go.wsgi:application
```

Используем `start.sh` в [юните](https://dvmn.org/encyclopedia/deploy/systemd/) для `systemd`:

```ini
; /etc/systemd/system/where_to_go.service
[Unit]
Description=Where to Go Site

[Service]
Type=simple
WorkingDirectory=/var/www/projects/where_to_go
ExecStart=/var/www/projects/where_to_go/start.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

За [отдачу статики и загружаемых фотографий](https://dvmn.org/encyclopedia/web-server/deploy-django-nginx-gunicorn/) на сервере отвечает Nginx.

Пример конфига, где Django-приложение запускается на `localhost:5551` с Nginx в качестве реверс-прокси на `http://<YOUR-ADDRESS>`:

```nginx
server {
  listen <YOUR-ADDRESS>:80;

  location /media/ {
    alias /path/to/where_to_go/media/;
  }

  location = /favicon.ico { access_log off; log_not_found off; }

  location /static/ {
    alias /path/to/where_to_go/staticfiles/;
  }

  location / {
    include '/etc/nginx/proxy_params';
    proxy_pass http://localhost:5551/;
  }
}
```

## Загрузка данных из JSON
Предусмотрена команда для загрузки данных о местах в JSON по URL ([пример](https://github.com/devmanorg/where-to-go-places/blob/master/places/Водопад%20Радужный.json)). У каждого места должно быть уникальное название. При расхождении в описании и координатах сохранятся уже существующие данные (данные из JSON проигнорируются).

Примеры использования:

```sh
# загрузить данные об одном месте
poetry run python manage.py load_place http://.../place.json

# можно передать несколько URL-ов
poetry run python manage.py load_place http://.../place1.json http://.../place1.json

# удобно сохранить все URL-ы в текстовом файле (здесь places.txt)
# каждый на отдельной строке и одной командой загрузить их все
poetry run python manage.py load_place $(cat places.txt)
```
