# Atomic Habit

## Запуск проекта через Docker Compose

### Требования
- Docker
- Docker Compose

### Команда для запуска проекта
```bash

# Создать .env файл
cp .env.example .env

# Запустить проект
docker-compose up -d --build
```
## Проверить работоспособность

### Проверка web

1. Открыть в браузере
http://localhost:8000

2. Проверить логи
```bash
docker-compose logs web
```

### Проверка PostgreSQL

1. Подключиться к БД


2. Посмотреть таблицы (в psql)
```bash
\dt
```

3. Выйти
```bash
\q
```

### Проверка Redis

1. Проверить соединение
```bash
docker-compose exec redis redis-cli ping
```
Должен ответить: PONG

### Проверка Celery Worker

1. Проверить логи
```bash
docker-compose logs celery_worker
```
2. Проверить статус
```bash
docker-compose ps | grep celery_worker
```

### Проверка Celery Beat

1. Проверить логи
```bash
docker-compose logs celery_beat
```

2. Проверить статус
```bash
docker-compose ps | grep celery_beat
```

### Проверить статус всех контейнеров
```bash
docker-compose ps
```

### Проверить логи всех сервисов
```bash
docker-compose logs -f
```

### Проверить использование ресурсов
```bash
docker stats
```

## Остановка проекта
```bash
docker-compose down -v
```

## Подготовка удаленного сервера
1. Создайте виртуальную машину на сервере(например Yandex Cloud)
2. Создайте ssh-ключ
3. Вставьте ssh-ключ в виртуальную машину 
4. Заполните все Git secrets(DOCKER_HUB_USERNAME, DOCKER_HUB_ACCESS_TOKEN, SSH_KEY, SSH_USER, SERVER_IP, SECRET_KEY(ключ django))

### Подключитесь к серверу через команду (в командной строке)
```bash
ssh -l (SSH_USER) (SERVER_IP)
```

### Обновите пакеты (в командной строке)
```bash
sudo apt update && sudo apt upgrade -y
```

### Установите докер (в командной строке)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

## Запуск workflow

1. Сделайте коммит в ветку и запушьте
2. Git actions автоматически запустит workflow

## Проверка деплоя

### Подключитесь к серверу (в командной строке)
```bash
ssh -l (YOUR_SSH_USER) (YOUR_SERVER_IP)
```

### Проверьте запущенные контейнеры (в командной строке)
```bash
docker ps
```

### Проверьте логи (в командной строке)
```bash
docker logs myapp
```

### Проверьте доступность сайта (в командной строке)
```bash
curl http://localhost:80
```