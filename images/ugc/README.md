## **UGC**

### **Описание**

Микросервис представляет собой интерфейс для работы с пользовательским контентом (UGC).

### **Технологии**

```Python``` ```FastAPI``` ```MongoDB``` ```NGINX``` ```Docker``` ```Docker Compose```

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
# SECRET KEYS
JWT_SECRET_KEY=

```

Запустите проект:

```shell
docker-compose build
docker-compose up
```
