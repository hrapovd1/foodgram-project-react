# Проект Foodgram, «Продуктовый помощник»

[![Python application](https://github.com/hrapovd1/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/hrapovd1/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

**Документация по API приложения доступно по адресу [hrapovd.sytes.net](http://hrapovd.sytes.net/api/docs/redoc.html)**

### Описание
Cервис позволяет публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин
скачивать сводный список продуктов, необходимых для приготовления одного или
нескольких выбранных блюд.

### Техническое описание
К проекту по адресу <http://hrapovd.sytes.net/api/docs/redoc.html> подключена документация API.  
В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса  
указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

#### Фронтенд
Предоставлен командой курса.

#### Бекенд
- [Python] v3.7
- [Django] v2.2.28
- [Django REST framework] v3.13.1
- [SimpleJWT] v4.8.0
- [PostgreSQL] 13

### Пользовательские роли
- **Аноним** — может просматривать список рецептов и отдельные рецепты, фильтровать по тегам вывод.
- **Аутентифицированный пользователь** (`user`) — может просматривать всё, как и Аноним, а так же создавать новые рецепты, добавлять рецепты других пользователей в "Избранное" и "Список покупок" из которого потом можно скачать ингредиенты в виде файла.
- **Администратор** (`admin`) — полные права на управление всем контентом проекта. 
Так же доступен администраторская [страница](http://hrapovd.sytes.net/admin/) на которой можно добавить/удалить теги и инградиенты.
### Запуск проекта
#### Минимальные требования к инфраструктуре:

- Docker Engine 20.10.0+
- docker compose 1.29.2

#### Установка переменных среды.
Для корректного запуска необходимо создать файл .env с переменными:
```BASH
cd infra
touch .env
```
Затем необходимо заполнить его следующими переменными:
```BASH
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
Для запуска в продакшен среде необходимо создать отдельную базу для приложения, создать пользователя для этой базы и внести эти данные в .env файл.


#### Запуск
```BASH
cd infra
docker-compose up -d
``` 
- Настройка БД: 
```BASH
docker-compose exec app python3 manage.py migrate
```
- Собираем статические файлы для корректного отображения страниц: 
```BASH
docker-compose exec app python3 manage.py collectstatic --noinput
```
- Создаем супер пользователя: 
```BASH
docker-compose exec app python3 manage.py createsuperuser
```
- При желании импортируем тестовые данные, для демонстрации: 
```BASH
docker-compose exec app python3 manage.py loaddata static/data/dump.json
```
В результате создадуться пользователи:
  
    * test@local.net (пароль: 1234.Rewq)
    * test1@local.net (пароль: 1234.Rewq)
    * admin@local.net (пароль: 1234.Rewq) - администратор
и демонстрационные рецепты.
- Или только заполняем таблицу инградиентов, а остальное создаем самостоятельно:
```BASH
docker-compose exec web python3 manage.py importcsv
```
## Примеры запросов API

### Зарегистрировать пользователя

запрос:
```
curl --location --request POST 'http://localhost/api/users/' \
--header 'Content-Type: application/json' \
--data-raw '{
"email": "test2@local.net",
"username": "test2",
"first_name": "Тест2",
"last_name": "Ф",
"password": "1234.Rewq"
}'
```
ответ:
```
{"email":"test2@local.net","id":4,"username":"test2","first_name":"Тест2","last_name":"Ф","is_subscribed":false}
```
### Получить токен аутентификации

запрос:
```
curl --location --request POST 'http://localhost/api/auth/token/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
"email": "test2@local.net",
"password": "1234.Rewq"
}'
```

ответ:
```
{"auth_token":"2a487c65d11b17f27f5d40834af0dc78b991d7c2"}
```

### Получить список рецептов

запрос:
```
curl --location --request GET 'http://localhost/api/recipes/?tags=breekfast'
```

ответ:
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breekfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

### Создать рецепт 

запрос:
```
curl --location --request POST 'http://localhost/api/recipes/' \
--header 'Authorization: Token 2a487c65d11b17f27f5d40834af0dc78b991d7c2' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tags": [
        1
    ],
    "ingredients": [
        {
            "id": 1,
            "amount": 20
        },
        {
            "id": 1990,
            "amount": 40
        }
    ],
    "name": "Бутер",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "text": "Бутер из хлеба и варения.",
    "cooking_time": 2
}'
```
ответ:
```
{"id":21,"tags":[{"id":1,"name":"Завтрак","slug":"breekfast","color":"#b6e0e0"}],"author":{"email":"test2@local.net","id":4,"username":"test2","first_name":"Тест2","last_name":"Ф","is_subscribed":false},"ingredients":[{"id":1,"name":"абрикосовое варенье","measurement_unit":"г","amount":20},{"id":1990,"name":"хлеб","measurement_unit":"г","amount":40}],"is_favorited":false,"is_in_shopping_cart":false,"name":"Бутер","image":"/media/recipes/b10d5fae-e19c-43e6-8b0d-dbdc3a213895.png","text":"Бутер из хлеба и варения.","cooking_time":2}
```

[//]: # 
  [Python]: <https://www.python.org>
  [Django REST framework]: <https://www.django-rest-framework.org>
  [Django]: <https://www.djangoproject.com>
  [SimpleJWT]: <https://django-rest-framework-simplejwt.readthedocs.io/en/latest/>
  [PostgreSQL]: <https://www.postgresql.org/>