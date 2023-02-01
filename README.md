# Проект Foodgram, «Продуктовый помощник»


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


[//]: # 
  [Python]: <https://www.python.org>
  [Django REST framework]: <https://www.django-rest-framework.org>
  [Django]: <https://www.djangoproject.com>
  [SimpleJWT]: <https://django-rest-framework-simplejwt.readthedocs.io/en/latest/>
  [PostgreSQL]: <https://www.postgresql.org/>