# Where to Go
Сайт про интересные места на карте:

- [Рабочая версия](http://v1131340.hosted-by-vdsina.ru:5001).
- [Панель администратора](http://v1131340.hosted-by-vdsina.ru:5001/admin) (логин и пароль отправлен в сообщении к ревью).

## Установка и запуск
Этот раздел актуален и для локальной разработки и для деплоя.

Установка через [Poetry](https://python-poetry.org). Склонируйте репозиторий и запустите установку:

```sh
poetry install
```

Создайте файл `.env` со следующими параметрами:

```ini
DEBUG=False # True для локальной разработки
SECRET_KEY='...'
ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1,... # добавье ваш домен или IP
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
Запустите встроенный Джанго-сервер следующей командой:

```sh
poetry run python manage.py runserver
```

## Запук на сервере
На сервере сайт запускается на [Gunicorn](https://gunicorn.org) с реверс-прокси через Nginx.

Рекомендуемый порядок действий после выполнения команд из раздела «Установка и запуск»:

```sh
# собрать статику
poetry run python manage.py collectstatic

# узнать путь к Python-окружению (Executable в выводе)
poetry env info
# Virtualenv
# ...
# Executable: /home/USERNAME/.../bin/python
# ...
```

Запустить Django-приложение через Gunicorn можно следующей командой, которую для удобства мы сохраним в файле `start.sh` в директории проекта:

```sh
#!/usr/bin/env bash
/home/USERNAME/.../bin/python \
    -m gunicorn -w 3 \
    --chdir /var/www/projects/where_to_go \
    -b localhost:5551 \
    where_to_go.wsgi:application
```

Используем `start.sh` [сервисе](https://dvmn.org/encyclopedia/deploy/systemd/) для `systemd`:

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

За отдачу статики (JS, CSS, иконки) отвечает [Whitenoise](https://whitenoise.readthedocs.io/en/latest/), он работает без дополнительных настроек. Для отдачи загружаемых фотографий нужно [настроить Nginx](https://dvmn.org/encyclopedia/web-server/deploy-django-nginx-gunicorn/).

Прмер конфига для Nginx, где Django-приложение запускается на `localhost:5551` с реверс-прокси на `http://<YOUR-ADDRESS>`:

```nginx
server {
  listen <YOUR-ADDRESS>:80;

  location /media/ {
    alias /var/www/projects/where_to_go/media/;
  }

  location / {
    include '/etc/nginx/proxy_params';
    proxy_pass http://localhost:5551/;
  }
}
```
