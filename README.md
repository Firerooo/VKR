# Web-app on django

Краткое описание проекта. Например, "Django‑приложение для аренды недвижимости".

Перед запуском убедитесь, что у вас установлены:
- [Docker](https://docs.docker.com/engine/install/) (рекомендуется Docker Desktop для Windows/macOS или Docker Engine для Linux)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Установка Docker и Docker Compose

1. **Установка Docker:**
   - Windows/macOS: Загрузите [Docker Desktop](https://docs.docker.com/desktop/) и следуйте инструкциям установки.
   - Linux: Ознакомьтесь с [инструкциями по установке Docker Engine](https://docs.docker.com/engine/install/).

2. **Проверка установки:**

   Откройте терминал и выполните команды:
   ```bash
   docker --version
   docker-compose --version

3. **Клонирование репозитория**
    Склонируйте репозиторий и перейдите в его каталог:
    ``` bash
    git clone https://github.com/Firerooo/VKR
    Через cd переместитесь в папку репозитория.

4. **Настройка переменных окружения**
    В репозитории присутствует шаблон файла окружения — .env.example. Для корректной работы приложения:
    Переименуйте файл:
    ``` bash
   cp .env.example .env
   ```
    Отредактируйте .env, задав значения для всех требуемых переменных (например, SECRET_KEY, настройки подключения к базе данных, и т.п.).

## Запуск проекта

1. **Пересборка и запуск контейнеров**
    Если вы вносили изменения в код или конфигурацию, рекомендуется полностью пересобрать контейнеры:
    ``` bash
    docker-compose down --volumes
    docker-compose up --build -d

3. **Проверка работы приложения**
    После успешного запуска откройте веб-браузер и перейдите по адресу: http://localhost:8000

## Дополнительные команды
1. **Применение миграций**
    Для применения миграций выполните:
    ``` bash
    docker-compose exec web conda run -n myenv_rental python manage.py migrate

3. **Создание суперпользователя**
    Чтобы создать администратора:
    ``` bash
    docker-compose exec web conda run -n myenv_rental python manage.py createsuperuser

5. **Просмотр логов**
    Чтобы просмотреть логи контейнеров:
    ``` bash
    docker-compose logs web
    docker-compose logs db

7. **Подключение к контейнеру**
    Если необходимо выполнить команду внутри контейнера:
    ``` bash
    docker-compose exec web bash
    ```

## Дополнительная информация
    Шаблоны проекта и другие файлы, например, для загрузки дампа базы данных, содержатся в соответствующих каталогах (init-db и т.д.).

    Не забудьте добавить файлы с конфиденциальными данными (например, .env) в ваш .gitignore.
