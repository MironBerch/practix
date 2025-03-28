## **Async API**

### **Описание**

Микросервис представляет собой асинхронный API для полнотекстового поиска фильмов.

### **Технологии**

```Python``` ```FastAPI``` ```Redis``` ```Elasticsearch``` ```NGINX``` ```Docker``` ```Docker Compose```

### **Как запустить проект:**

В локальной среде:

```shell
cd infra/local/
docker-compose build
docker-compose up
```

В производственной среде:

```shell
cd infra/
docker-compose build
docker-compose up
```

### **Как использовать проект:**

В локальной среде:

```
http://127.0.0.1:8000/movies/api/docs
```

В производственной среде:

```
http://127.0.0.1/movies/api/docs
```
