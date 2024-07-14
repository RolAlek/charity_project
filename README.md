# FastAPI Donation service with PostgreSQL/Docker/GoogleSpreadsheet-API
___
## DESC:
Данный проект представляет собой краудфандинговый сервис, в котором администратором создаются проекты для сбора средств на различные цели с автоматическим распределением донатов.
Распределение производится по принциыпу FIFO - донат получает тот проект который был раньше открыт.
Если сумма средств доната `>=` чем необходимая или оставшаяся для закрытия проекта - оставшаяся сумма распределятеся в следующий проект или проекты.

Есть система пользователей и разграничения доступа к эндпоинтам.

Генерируйте удобные отчеты с помощью Google Таблиц.

Приложение упаковано в docker-контейнеры c использованием Docker-compose, что позвоолит развернуть сервис на Вашем VPS в несколько команд в CLI - "Просто добавь воды").
___
## Технологии:
- Язык: Python3.12
- Менеджер зависимостей: Poetry 1.8.3
- Фреймворк: FastAPI
- СУБД: PostgreSQL 16.3
- ORM: SQAlchemy + asyncpg
- Миграции: асинхронный Alembic 1.13.2
- Дополнительные сервисы: Aiogoogle 5.12.0
- Docker
___
> [!WARNING]
> Убедитесь, что у Вас установлен Python версии 12.

>[!WARNING]
> Убедитесь, что у Вас есть google-аккаунт для работы с Google Cloud Platform

<details>
<summary>
Установка для разработчиков:
</summary>

#### Создайте и активируйте виртуальное окружение:

* Для Linux/macOS

    ```sh
    python3.12 -m venv venv
    source venv/bin/activate
    ```

* Для Windows

    ```sh
    source venv/scripts/activate
    ```

#### В корне проекта создайте `.env`-файл с переменными окружения и заполните всоответствии с `.env.example`.

  ```
  APP__DB__URL=postgresql+asyncpg://<ваш_pg_user>:<ваш_pg_password>@localhost:5432/<ваш_pg_db>
  
  APP__USER__INIT_ROOT=1
  APP__USER__SECRET=YOURSECRETPHRASE
  APP__USER__LIFETIME=3600
  
  APP__USER__ROOT__LOGIN=<youremail@admin.ru>
  APP__USER__ROOT__PASSWORD=<your_admin_password>
  APP__USER__ROOT__FIRST_NAME=Иван
  APP__USER__ROOT__LAST_NAME=Иванов
  APP__USER__ROOT__BIRTHDAY=01-01-2000
  
  APP__GOOGLE__TYPE=
  APP__GOOGLE__PROJECT_ID=
  APP__GOOGLE__PRIVATE_KEY_ID=
  APP__GOOGLE__PRIVATE_KEY=
  APP__GOOGLE__CLIENT_EMAIL=
  APP__GOOGLE__CLIENT_ID=
  APP__GOOGLE__AUTH_URI=
  APP__GOOGLE__TOKEN_URI=
  APP__GOOGLE__AUTH_PROVIDER_X509_CERT_URL=
  APP__GOOGLE__CLIENT_X509_CERT_URL=
  APP__GOOGLE__EMAIL=
  
  POSTGRES_USER=<your_pg_user>
  POSTGRES_PASSWORD=<your_pg_password>
  POSTGRES_DB=<your_pg_db_name>
  ```

#### Установите менеджер зависимостей Poetry и примените необходимые зависимости:

```sh
pip install poetry
```
```sh
poetry install
```

#### Создайте сервисный аккаунт Google Cloud Platform. Получите ключ и JSON-файл с данными сервисного аккаунта, чтобы управлять подключёнными API из вашего Python-приложения и укажите эти данные в вашем .env.

   * `TYPE=<type>`
   * `PROJECT_ID=<project_id>`
   * `PRIVATE_KEY_ID=<private_key_id>`
   * `PRIVATE_KEY=<private_key>`
   * `CLIENT_EMAIL=<client_email>`
   * `CLIENT_ID=<client_id>`
   * `AUTH_URI=<auth_uri>`
   * `TOKEN_URI=<token_uri>`
   * `AUTH_PROVIDER_X509_CERT_URL=<auth_provider_x509_url>`
   * `CLIENT_X509_CERT_URL=<client_x509_cert_url>`
   * `EMAIL=<ваш_gmail>`

** данные переменные можно заполнить непосредственно в `class Config(BaseConfig)`, кроме `DATABASE_URL`, но помните что подобное хранение секретов не безопасно, создатели проекта рекомендую хранить секреты в переменных окружения.

#### Примените миграции и запустите приложение:
   ```
   alembic upgrade head
   uvicorn app.main:app --reload
   ```
</details>

> [!WARNING]
> Убедитесь, что у вас установлен Docker, если нет то Вам [сюда](https://docs.docker.com/desktop/)

<details>
<summary>
Развертывание и демонстрация:
</summary>

После создания и заполнения `.env`-файла, предварительной установки и настройки `docker` находясь в корне проекта выполните:
```sh
docker compose up -docker

```

> Да - это так легко!
</details>


## Использование

> [!NOTE]
> Если вы запустили проект с использование стандартного ASGI-сервера Uvicorn то все эндпоинты будут доступны по http://127.0.0.1:8000/api/

> [!NOTE]
> Если вы запустили проект с использование docker-compose то все эндпоинты будут доступны по http://localhost:8000/api/ или http://0.0.0.0:8000/api

### projects/:
* Получение списка всех проектов: - доступно абсолютно любому пользователю.
  Пример ответа:

  ```json
  [
    {
      "name": "string",
      "description": "string",
      "full_amount": 0,
      "create_date": "2024-01-28T03:45:52.682Z",
      "id": 0,
      "invested_amount": 0,
      "fully_invested": true,
      "close_date": "2024-01-28T03:45:52.682Z"
    }
  ]
  ```
* Создание, редактирование и удаление благотварительных проектов доступно только суперпользователю.
* Изменение и удаление закрытых проектов запрещено.
* Как только создается новый проект нераспределенные донаты автоматически поступят в него в пределах необходимой | доступной суммы.

### /donation/:
* Доступно только зарегистрированным пользователям и суперпользователям
* Изменение доната недоступно, даже root'у
* Также пользователям доступен просмотр всех своих пожертвования по адресу: `donation/my/`. Пример ответа:
  ```json
  [
    {
      "full_amount": 0,
      "comment": "string",
      "id": 0,
      "create_date": "2024-01-28T05:17:35.741Z"
    }
  ]
  ```
* Доступ ко всем пожертвованиям всех пользователей доступен только root-пользователю. Также ему доступны вся информация о донатах:
  ```json
  [
    {
      "full_amount": 0,
      "comment": "string",
      "id": 0,
      "create_date": "2024-01-28T05:50:37.965Z",
      "user_id": 0,
      "invested_amount": 0,
      "fully_invested": true,
      "close_date": "2024-01-28T05:50:37.965Z"
    }
  ]
  ```

### /users/:
* Просмотр и изменение пользователя

### /auth/:
* Регистрация и авторизация пользователя.

### /google/:
* Получение администратором отчета по закрытым проектам.
```json
  [
    {
      "name": "string",
      "rate": "1 day, 0:34:59.516646",
      "description": "string"
    }
  ]
  ```

Более подробно с эндпоинтами можно ознакомиться в интерактивной документации после запуска проекта:
* [ReDoc](http://127.0.0.1:8000/docs)
* [Swagger](http://127.0.0.1:800/redoc)
