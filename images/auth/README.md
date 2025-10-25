## **Auth**

### **Описание**

Микросервис представляет собой реализацию авторизации для онлайн-кинотеатра.

### **Технологии**

```Python``` ```FastAPI``` ```PostgreSQL``` ```Redis``` ```NGINX``` ```Uvicorn``` ```Docker``` ```Docker Compose```

### **Как запустить проект:**

В локальной среде:

Перейдите в директорию с инфраструктурой:

```shell
cd infra/local/
```

Создайте файл .env и добавьте настройки для проекта:

```dotenv
# NOTIFICATIONS RECEIVER
NOTIFICATIONS_RECEIVER_HOST=
NOTIFICATIONS_RECEIVER_PORT=

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

# AUTH DB
AUTH_DB_NAME=
AUTH_DB_USER=
AUTH_DB_PASSWORD=

# NOTIFICATIONS RECEIVER
NOTIFICATIONS_RECEIVER_HOST=
NOTIFICATIONS_RECEIVER_PORT=

```

Запустите проект:

```shell
docker-compose build
docker-compose up
```
