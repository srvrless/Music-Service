#  IN DEVELOPING...
## Nevless - Сервис предназначен для быстрого нахождения любомого трека.

### Реализована платная подписка по средствам API юкассы. 

### Stack Backend:
* **FastAPI**
* **Redis**
* **Celery**
* **Postgresql**
* **SQLAlchemy**
* **Asyncpg**
* **RabbitMQ**

### Stack Frontend:
* **HTML**
* **Vue.js**
* **Javascript**
* **Comming** **soon...**

#### Для поднятия сервиса в докере для локальной разработки :

`make up`

**Для накатывания миграций, запустить в терминале команды:**

`alembic init migrations`

`alembic revision --autogenerate -m "comment" - делается при любых изменениях моделей`

`alembic upgrade heads`
