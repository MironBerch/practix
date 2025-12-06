# practix

### **Описание**

[PRACTIX](https://github.com/MironBerch/practix) — это микросервисы для онлайн-кинотеатра:
- [Панель администратора](https://github.com/MironBerch/practix/tree/main/images/admin-panel) на фреймворке Django
- [Загрузка данных](https://github.com/MironBerch/practix/tree/main/images/admin-panel/scripts/load_db) в базу данных PostgreSQL
- [ETL](https://github.com/MironBerch/practix/tree/main/images/etl) для переноса данных из PostgreSQL в Elasticsearch
- [Асинхронный API](https://github.com/MironBerch/practix/tree/main/images/async-api) на фреймворке FastAPI
- [Авторизация пользователей](https://github.com/MironBerch/practix/tree/main/images/auth) на фреймворке FastAPI
- [Пользовательский контент](https://github.com/MironBerch/practix/tree/main/images/ugc) c помощью NoSQL базы данных MongoDB
- [Система нотификаций](https://github.com/MironBerch/practix/tree/main/images/notifications) в связке Django + FastAPI
- [Пользовательский интерфейс](https://github.com/MironBerch/practix/tree/main/images/notifications) на фреймворке Vue

### **Технологии**

```Python``` ```TypeScript``` ```FastAPI``` ```Django``` ```Vue``` ```PostgreSQL``` ```Elasticsearch``` ```Redis``` ```MongoDB``` ```SQLite``` ```RabbitMQ``` ```Docker``` ```Docker Compose``` ```Terraform``` ```Yandex-Cloud``` ```Kubernetes```

### **Как запустить проект в локальной среде:**

Перейдите в директорию `practix/infra/local/`:

```shell
cd infra/local/
```

Создайте файл `.env`:

```dotenv
# SMTP
SMTP_SERVER=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=

```

Ознакомиться с проектом в локальной среде можно по следующим ссылкам:

| Адрес | Описание |
| :------ | :------ |
| [/admin](http://127.0.0.1:8000/admin) | _Панель управления фильмами_ |
| [/movies](http://127.0.0.1:3000/movies/api/docs) | _Документация API поиска фильмов_ |
| [/auth](http://127.0.0.1:5000/auth/api/docs) | _Документация API авторизации пользователей_ |
| [/ugc](http://127.0.0.1:8080/ugc/api/docs) | _Документация API пользовательского контента_  |
| [/notifications/admin](http://127.0.0.1:8001/notifications/admin/) | _Панель управления уведомлениями_ |
| [/notifications/api](http://127.0.0.1:6000/notifications/api/docs) | _Документация API уведомлений_ |
| [/frontend](http://127.0.0.1:3001/) | _Пользовательский интерфейс_ |

### **Как запустить проект в производственной среде:**

Перейдите в директорию `practix/infra/`:

```shell
cd infra/
```

Создайте файл `.env`:

```dotenv
# SECRET KEYS
SECRET_KEY=
JWT_SECRET_KEY=

# AUTH DB
AUTH_DB_USER=
AUTH_DB_PASSWORD=
AUTH_DB_NAME=

# MOVIES DB
MOVIES_DB_USER=
MOVIES_DB_PASSWORD=
MOVIES_DB_NAME=

# NOTIFICATIONS DB
NOTIFICATIONS_DB_USER=
NOTIFICATIONS_DB_PASSWORD=
NOTIFICATIONS_DB_NAME=

# RABBITMQ
RABBITMQ_DEFAULT_USER=
RABBITMQ_DEFAULT_PASS=

# MOVIES ADMIN PANEL SUPERUSER
MOVIES_DJANGO_SUPERUSER_USERNAME=
MOVIES_DJANGO_SUPERUSER_EMAIL=
MOVIES_DJANGO_SUPERUSER_PASSWORD=

# NOTIFICATIONS ADMIN PANEL SUPERUSER
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_PASSWORD=

# NOTIFICATIONS SMTP
SMTP_SERVER=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=

```

Ознакомиться с проектом в производственной среде можно по следующим ссылкам:

| Адрес | Описание |
| :------ | :------ |
| [/admin](http://127.0.0.1/admin) | _Панель управления фильмами_ |
| [/movies](http://127.0.0.1/movies/api/docs) | _Документация API поиска фильмов_ |
| [/auth](http://127.0.0.1/auth/api/docs) | _Документация API авторизации пользователей_ |
| [/ugc](http://127.0.0.1/ugc/api/docs) | _Документация API пользовательского контента_  |
| [/notifications](http://127.0.0.1/notifications/admin/) | _Панель управления уведомлениями_ |
