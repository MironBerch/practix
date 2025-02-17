## **Admin Panel**

### **Описание**

Микросервис представляет собой административную панель для загрузки фильмов и редактирования информации о них.

### **Технологии**

```Python``` ```Django``` ```PostgreSQL``` ```NGINX``` ```Gunicorn``` ```Docker``` ```Docker Compose```

### **Как запустить проект:**

В локальной среде:

```shell
cd infra/local/
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
# secret key
SECRET_KEY=

# django superuser
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_PASSWORD=

# movies db
DB_HOST=movies_db
DB_PORT=5432
DB_NAME=
DB_USER=
DB_PASSWORD=

```

Запустите проект:

```shell
docker-compose build
docker-compose up
```

### **Как использовать проект:**

В локальной среде:

Перейдите в админ-панель и введите логин (admin) и пароль (root):

```
http://127.0.0.1:8000/admin/
```

В производственной среде:

Перейдите в админ-панель и введите логин и пароль:

```
http://0.0.0.0/admin/
```
