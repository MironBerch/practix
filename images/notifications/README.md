## **Notifications**

### **Описание**

Микросервисы представляют собой асинхронный API, административную панель и worker для отправки уведомлений.

### **Технологии**

```Python``` ```Django``` ```FastAPI``` ```PostgreSQL``` ```RabbitMQ``` ```Gunicorn``` ```NGINX``` ```Docker```

### **Как запустить проект:**

В локальной среде:

Перейдите в директорию с инфраструктурой:

```shell
cd infra/local/
```

Создайте файл .env и добавьте настройки для проекта:

```dotenv
# SMTP
SMTP_SERVER=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=

```

Запустите проект:

```shell
docker-compose build
docker-compose up
```

В производственной среде:

Перейдите в директорию с инфраструктурой:

```shell
cd infra/
```

Создайте файл .env и добавьте настройки для проекта:

```dotenv
# SECRET KEYS
SECRET_KEY=
JWT_SECRET_KEY=

# NOTIFICATIONS DB
NOTIFICATIONS_DB_USER=
NOTIFICATIONS_DB_PASSWORD=
NOTIFICATIONS_DB_NAME=

# SMTP
SMTP_SERVER=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=

# RABBITMQ
RABBITMQ_DEFAULT_USER=
RABBITMQ_DEFAULT_PASS=

# DJANGO SUPERUSER
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_PASSWORD=

```

Запустите проект:

```shell
docker-compose build
docker-compose up
```
