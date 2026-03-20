# Atomic Habit

Приложение развернуто и доступно по адресу: **http://178.154.198.7:8000**

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
4. Заполните все Git secrets(
SECRET_KEY	- Django секретный ключ,
ALLOWED_HOSTS - Разрешенные хосты (через запятую),
DB_NAME - Имя базы данных,
DB_USER - Пользователь БД,
DB_PASSWORD - Пароль БД,
POSTGRES_DB - Имя БД для Postgres,
POSTGRES_USER - Пользователь Postgres,
POSTGRES_PASSWORD - Пароль Postgres,
EMAIL - Email для уведомлений,
WEB_PASSWORD - Пароль от email,
TELEGRAM_BOT_TOKEN - Токен Telegram бота,
DOCKER_HUB_USERNAME - Имя пользователя Docker Hub,
DOCKER_HUB_ACCESS_TOKEN - Токен доступа Docker Hub,
SERVER_IP - IP адрес сервера,
SSH_USER - Пользователь SSH,
SSH_KEY)


### Подключитесь к серверу через команду (в командной строке)
```bash
ssh -l (SSH_USER) (SERVER_IP)
```

### Обновите пакеты (в командной строке)
```bash
sudo apt update && sudo apt upgrade -y
```

## Установите Docker и Docker Compose:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Выход и повторный вход
```bash
exit
ssh user@your-server-ip
```
### Проверка установки
```bash
docker --version
docker compose version
```
## Создайте .env файл:
```bash
cat > .env << 'EOF'
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-server-ip,localhost,127.0.0.1
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=postgres
DB_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=postgres
EMAIL=your-email@example.com
WEB_PASSWORD=your-email-password
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
REDIS_URL=redis://redis:6379/0
EOF
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
curl http://localhost:8000
```