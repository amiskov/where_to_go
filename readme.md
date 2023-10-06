# Where to Go
Сайт про интересные места на карте:

- [Рабочая версия](http://v1131340.hosted-by-vdsina.ru:5001).
- [Панель администратора](http://v1131340.hosted-by-vdsina.ru:5001/admin) (логин и пароль отправлен в сообщении к ревью).

## Установка и запуск
Установка через [Poetry](https://python-poetry.org). Склонируйте репозиторий и запустите установку. Poetry сама создать окружение:

```sh
poetry install
```

Создайте файл `.env` со следующими параметрами:

```ini
DEBUG=False # True для локальной разработки
SECRET_KEY='...'
ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1,...
```

Далее, накатите миграции:

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
На сервере сайт запускается на [Gunicorn](https://gunicorn.org) с реверс-прокси через Nginx. Рекомендуемый порядок действий:

```sh
# перейти в директорию проекта
cd <project dir>

# установить зависимости
poetry install

# запустить миграции
poetry run python manage.py migrate

# собрать статику
poetry run python manage.py collectstatic

# создать администратора
poetry run python manage.py createsuperuser

# узнать путь к созданному окружению (Executable в выводе)
poetry env info
# Virtualenv
# ...
# Executable: /home/USERNAME/.../bin/python
# ...
```

Запустить Django-приложение через Gunicorn можно следующей командой, которую для удобства можно сохранить в директории проекта в файле `start.sh`:

```sh
#!/usr/bin/env bash
/home/USERNAME/.../bin/python \
    -m gunicorn -w 3 \
    --chdir /var/www/projects/where_to_go \
    -b localhost:5551 \
    where_to_go.wsgi:application
```

`start.sh` можно использовать при [создании сервиса](https://dvmn.org/encyclopedia/deploy/systemd/) для `systemd`. Рекомендуемый конфиг:

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

За отдачу статики (JS, CSS, иконки) отвечает [Whitenoise](https://whitenoise.readthedocs.io/en/latest/), для отдачи загружаемых фотографий нужно [настроить nginx](https://dvmn.org/encyclopedia/web-server/deploy-django-nginx-gunicorn/).

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
