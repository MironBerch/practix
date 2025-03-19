## **ETL**

### **Описание**

Данный микросервис является ETL-скриптом на Python для синхронизации данных из БД PostgreSQL в поисковый движок Elasticsearch и MongoDB. Данные содержат информацию о фильмах и связанных с ними людях, а так же о пользователях.

### **Технологии**

```Python``` ```PostgreSQL``` ```Elasticsearch``` ```Redis``` ```MongoDB``` ```Docker```

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
# movies db
MOVIES_DB_NAME=
MOVIES_DB_USER=
MOVIES_DB_PASSWORD=

# auth db
AUTH_DB_NAME=
AUTH_DB_USER=
AUTH_DB_PASSWORD=

```

Запустите проект:

```shell
docker-compose build
docker-compose up
```
