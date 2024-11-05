# practix

### **Описание**

[PRACTIX](https://github.com/MironBerch/practix) — это микросервисы для онлайн-кинотеатра:
- [Панель администратора](https://github.com/MironBerch/practix/tree/main/images/admin-panel) на фреймворке Django
- [Загрузка данных](https://github.com/MironBerch/practix/tree/main/images/admin-panel/scripts/load_db) в базу данных PostgreSQL
- [ETL](https://github.com/MironBerch/practix/tree/main/images/etl) для переноса данных из PostgreSQL в Elasticsearch
- [Асинхронный API](https://github.com/MironBerch/practix/tree/main/images/async-api) на фреймворке FastAPI
- [Авторизация пользователей](https://github.com/MironBerch/practix/tree/main/images/auth) на фреймворке Flask
- [Пользовательский контент](https://github.com/MironBerch/practix/tree/main/images/ugc) c помощью NoSQL базы данных MongoDB

### **Технологии**

```Python``` ```FastAPI``` ```Django``` ```Flask``` ```PostgreSQL``` ```Elasticsearch``` ```Redis``` ```MongoDB``` ```SQLite``` ```Docker``` ```Docker Compose```

### **Как запустить проект:**

В локальной среде:
```shell
cd infra/local/
docker compose build
docker compose up
```

В производственной среде:
```shell
cd infra/
docker compose build
docker compose up
```
