# Where to Go

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

## Запуск для разработки
Запустите встроенный Джанго-сервер следующей командой:

```sh
poetry run python manage.py runserver
```

## Запук на сервере
Запустить продакшен-сервер:

```sh
# запустятся миграции, сборка статики и прод-сервер
make runprod
```

Остановить сервер:

```sh
make killprod
```
