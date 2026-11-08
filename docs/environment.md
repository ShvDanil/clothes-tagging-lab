# Окружение и диагностика

## Через Docker

Основной путь описан в [README](../README.md). Docker Desktop/Engine должен быть запущен. Compose поднимает PostgreSQL 17 и API, дожидается готовности БД, затем создает недостающие таблицы. Платные API и S3 для старта инфраструктуры не нужны.

```bash
docker compose ps
docker compose logs --tail=100 api db
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\d item_annotations"'
```

После старта есть таблица `item_annotations`; записей разметки каркас не создает. Перезапуск не удаляет таблицы. `create_all` не изменяет уже существующие столбцы: при изменении схемы используйте миграцию или намеренно пересоздайте только локальную учебную БД.

Если порт занят, измените `API_PORT` или `POSTGRES_PORT` в `.env`. Если меняете порт/реквизиты БД, обновите `DATABASE_URL` для запуска Python с хоста. В Compose URL строится из `POSTGRES_*` автоматически. Пример пароля предназначен для локального запуска; при специальных символах в новых реквизитах корректно кодируйте URL подключения.

Изменение пароля в `.env` не меняет пользователя внутри уже созданного PostgreSQL volume. Используйте прежние реквизиты или осознанно пересоздайте локальный volume. Внешние сервисы и общие БД для тестов не используйте.

## Python на хосте

Нужен Python 3.12. В проекте есть lock-файл `uv.lock` и экспортированные зависимости для pip; для обычного запуска uv не обязателен.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
docker compose up -d --wait db
uvicorn app.main:app --reload
```

Не запускайте второй API на том же порту одновременно с контейнером. Для разработки на хосте достаточно контейнера `db`. Переменные читаются из `.env`; начните с `cp .env.example .env`.

```bash
ruff check .
ruff format --check .
pytest
```

`pytest` по умолчанию запускает тесты без PostgreSQL. Интеграционные тесты требуют отдельный `TEST_DATABASE_URL`; пример для локального контейнера:

```bash
TEST_DATABASE_URL='postgresql+psycopg://clothes:local-development-only@localhost:5433/clothes' pytest -m integration
```

Они создают случайную изолированную схему и удаляют только ее. Тесты выбранной модели должны работать с подменой HTTP-клиента/провайдера и не требовать реального API.

## Изменение зависимостей и конфигурации

Зависимости задаются в `pyproject.toml`. При добавлении SDK или библиотек обновляйте lock и оба экспорта; здесь использован uv 0.11.3:

```bash
uv lock
uv export --frozen --no-dev --no-emit-project --format requirements-txt --output-file requirements.txt
uv export --frozen --no-emit-project --format requirements-txt --output-file requirements-dev.txt
```

Затем повторите сборку контейнеров и проверки. Для сравнения подходов могут потребоваться несколько ключей; выбранному сервису нужен только его провайдер. Дополните `.env.example` без секретов и `compose.yaml`, чтобы нужные переменные попадали в контейнер. Резервные `MODEL_API_KEY` и `MODEL_ID` уже передаются в API, но каркас их не использует.

Для S3 в `.env.example` зарезервированы параметры выдачи данных. Самостоятельной загрузки при запуске приложения нет; порядок скачивания — в [описании датасета](../data/README.md).
