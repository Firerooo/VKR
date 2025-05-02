# Базовый образ с Miniconda
FROM continuumio/miniconda3

# Устанавливаем необходимые системные пакеты:
# netcat-openbsd вместо netcat для проверки подключения к базе данных
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    apt-get clean

# Указываем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл environment.yml в контейнер
COPY environment.yml .

# Создаём conda-окружение на основе файла environment.yml и очищаем кэш
RUN conda env create -f environment.yml && \
    conda clean -afy

# Копируем все содержимое проекта в рабочую директорию контейнера
COPY . .

# Копируем скрипт ожидания подключения к базе данных в контейнер и делаем его исполняемым
COPY wait-for-db.sh /usr/local/bin/wait-for-db.sh
RUN chmod +x /usr/local/bin/wait-for-db.sh

# Открываем порт приложения (для Django – 8000)
EXPOSE 8000

# Запускаем приложение через conda run с ожиданием готовности базы данных.
# Скрипт wait-for-db.sh ожидает, пока сервис с именем "db" станет доступен на порту 5432, затем запускается Django.
CMD ["conda", "run", "-n", "myenv_rental", "wait-for-db.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"]
