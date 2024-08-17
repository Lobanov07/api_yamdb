# Проект YaMD

## Оглавление:
- [Стек технологий.](#Стек-технологий)
- [Краткое описание проекта.](#Краткое-описание-проекта)
- [Как запустить проект.](#Установка-и-запуск)
- [Примеры запросов к API.](#Примеры-запросов-к-API)
- [Команда разработки.](#Команда-разработки)
  
## Стек технологий
- Python 3.9
- Django
- DRF
- JWT токены

## Краткое описание проекта:
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Установка и запуск:
1.Клонировать репозиторий и перейти к проекту:
```
git clone https://github.com/shulikin/api_yatube.git && cd api_yatube
```
```
cd yatube_api
```
2.В корневой директории проекта создайте виртуальное окружение, используя команду:
- Если у вас windows
```
python -m venv venv
```
  или
```
py -3 -m venv venv
```
- Если у вас Linux/macOS
```
python3 -m venv venv.
```
3.Активируйте виртуальное окружение командой:
- Если у вас windows
```
source venv/Scripts/activate
```
- Если у вас Linux/macOS
```
source venv/bin/activate
```
4.Обновите менеджер пакетов:
```
python -m pip install --upgrade pip
```
5.Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
6.Выполнить миграции:
```
python manage.py migrate
```
7.Запустить проект:
```
python manage.py runserver
```
Ваш проект запустился на `http://127.0.0.1:8000/`

С помощью команды *pytest* вы можете запустить тесты и проверить работу модулей

8. Можно создать пользователя после запуска проекта:
```
http://127.0.0.1:8000/v1/auth/signup/
```
отправить POST-запрос:

    {
        "username": "XXXXX",
        "email": "XXXXX"
    }

9. В проекте в папке `sent_emails` появится сгенерированное письмо с кодом подтвержения. Скопируйте этот код, он потребуется для получения токена к зарегистрированной учетной записи

##  Аутентификация

Выполните POST-запрос *localhost:8000/v1/auth/token/* передав поля username и confirmation_code(см. пункт 9 и 10).

API вернет JWT-токен в формате:

    {
        "token": "ХХХХХXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    }
    
token - наш токен, который необходимо передать в заголовке Authorization: Bearer <токен> при отправке запросов

Теперь пользователь считается авторизованным и может полноценно использовать текущий проект по отзывам произведений.

## Примеры запросов к API

### Регистрация пользователей и выдача токенов

Регистрация нового пользователя

Получить код подтверждения на переданный email.
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.
```
POST http://127.0.0.1:8000/api/v1/auth/signup/
```
Пример запроса:
```
{
"email": "string",
"username": "string"
}
```
Пример ответа:
```
{
"email": "string",
"username": "string"
}
```
Получение JWT-токена

Получение JWT-токена в обмен на username и confirmation code.
Права доступа: Доступно без токена.
```
POST http://127.0.0.1:8000/api/v1/auth/token/
```
Пример запроса:
```
{
"username": "string",
"confirmation_code": "string"
}
```
Пример ответа:
```
{
  "token": "string"
}
```
### Категории

Получение списка всех категорий

Получить список всех категорий
Права доступа: Доступно без токена
```
GET http://127.0.0.1:8000/api/v1/categories/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
Добавление новой категории

Создать категорию.
Права доступа: Администратор.
Поле slug каждой категории должно быть уникальным.
```
POST http://127.0.0.1:8000/api/v1/categories/
```
Пример запроса:
```
{
  "name": "string",
  "slug": "string"
}
```
Пример ответа:
```
{
  "name": "string",
  "slug": "string"
}
```
Удаление категории

Удалить категорию.
Права доступа: Администратор.
```
DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/
```

### Жанры
Получение списка всех жанров

Получить список всех жанров.
Права доступа: Доступно без токена
```
GET http://127.0.0.1:8000/api/v1/genres/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
Добавление жанра

Добавить жанр.
Права доступа: Администратор.
Поле slug каждого жанра должно быть уникальным.
```
POST http://127.0.0.1:8000/api/v1/genres/
```
Пример запроса:
```
{
  "name": "string",
  "slug": "string"
}
```
Удаление жанра

Удалить жанр.
Права доступа: Администратор.
```
DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/
```

### Произведения (Titles)
Получение списка всех произведений

Получить список всех объектов.
Права доступа: Доступно без токена
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
Добавление произведения

Добавить новое произведение.
Права доступа: Администратор.
Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).
При добавлении нового произведения требуется указать уже существующие категорию и жанр.
```
POST http://127.0.0.1:8000/api/v1/titles/
```
Пример запроса:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Получение информации о произведении

Информация о произведении
Права доступа: Доступно без токена
```
GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
Пример ответа:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Частичное обновление информации о произведении

Обновить информацию о произведении
Права доступа: Администратор
```
PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
Пример запроса:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Удаление произведения

Удалить произведение.
Права доступа: Администратор.
```
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

### Отзывы (Reviews)
Получение списка всех отзывов

Получить список всех отзывов.
Права доступа: Доступно без токена.
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
Добавление нового отзыва

Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.
Права доступа: Аутентифицированные пользователи.
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
Пример запроса:
```
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Полуение отзыва по id

Получить отзыв по id для указанного произведения.
Права доступа: Доступно без токена.
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Частичное обновление отзыва по id

Частично обновить отзыв по id.
Права доступа: Автор отзыва, модератор или администратор.
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
Пример запроса:
```
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Удаление отзыва по id

Удалить отзыв по id
Права доступа: Автор отзыва, модератор или администратор.
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

### Комментарии к отзывам (Comments)
Получение списка всех комментариев к отзыву

Получить список всех комментариев к отзыву по id
Права доступа: Доступно без токена.
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
Добавление комментария к отзыву

Добавить новый комментарий для отзыва.
Права доступа: Аутентифицированные пользователи.
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Пример запроса:
```
{
  "text": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Получение комментария к отзыву

Получить комментарий для отзыва по id.
Права доступа: Доступно без токена.
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Частичное обновление комментария к отзыву

Частично обновить комментарий к отзыву по id.
Права доступа: Автор комментария, модератор или администратор.
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
Пример запроса:
```
{
  "text": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Удаление комментария к отзыву

Удалить комментарий к отзыву по id.
Права доступа: Автор комментария, модератор или администратор.
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

### Пользователи (Users)
Получение списка всех пользователей

Получить список всех пользователей.
Права доступа: Администратор
```
GET http://127.0.0.1:8000/api/v1/users/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```
Добавление пользователя

Добавить нового пользователя.
Права доступа: Администратор
Поля email и username должны быть уникальными
```
POST http://127.0.0.1:8000/api/v1/users/
```
Пример запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Получение пользователя по username

Получить пользователя по username.
Права доступа: Администратор
```
GET http://127.0.0.1:8000/api/v1/users/{username}/
```
Пример запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Изменение данных пользователя по username

Изменить данные пользователя по username.
Права доступа: Администратор.
Поля email и username должны быть уникальными.
```
PATCH http://127.0.0.1:8000/api/v1/users/{username}/
```
Пример запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Удаление пользователя по username

Удалить пользователя по username.
Права доступа: Администратор.
```
DELETE http://127.0.0.1:8000/api/v1/users/{username}/
```
Получение данных своей учетной записи

Получить данные своей учетной записи
Права доступа: Любой авторизованный пользователь
```
GET http://127.0.0.1:8000/api/v1/users/me/
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Изменение данных своей учетной записи

Изменить данные своей учетной записи
Права доступа: Любой авторизованный пользователь
Поля email и username должны быть уникальными.
```
PATCH http://127.0.0.1:8000/api/v1/users/me/
```
Пример запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

## Команда разработки
* ### **Nelen Denis**
  * github: [tosno](https://github.com/tosno)
* ### **Shulikin Aleksey**
  * github: [shulikin](https://github.com/shulikin)
* ### **Lobanov Konstantin**
  * github: [Lobanov07](https://github.com/Lobanov07)
