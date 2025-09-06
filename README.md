# DDS Project

## Описание проекта
ДДС (движение денежных средств) — это процесс учета, управления и анализа
поступлений и списаний денежных средств компании или частного лица. В рамках
данного проекта создано веб-приложение, в котором пользователь имеет 
возможность вести учет всех денежных операций компании.

## Стек
* **Django:** Веб-фреймворк для разработки серверной части.
* **Django REST Framework:** Библиотека для создания RESTful API.
* **SQLite:** Система управления базами данных.
* **Python:** Язык программирования, на котором написан проект.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Dinara2801/dds.git
```

```
cd dds
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в модуль  и выполнить миграции:

```
cd backend
```

```
python3 manage.py migrate
```

Заполнить базу данных:

```
python manage.py import_data
```

Запустить проект:

```
python3 manage.py runserver
```
## Примеры запросов и ответов

### Пример запроса на создание статуса операции
```json
POST /api/statuses/
Content-Type: application/json

{
    "name": "Бизнес"
}
```

Ответ:

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Бизнес"
        }
    ]
}
```

### Пример запроса на создание типа операции
```json
POST /api/types/
Content-Type: application/json

{
    "name": "Списание"
}
```

Ответ:

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Списание"
        }
    ]
}
```

### Пример запроса на создание категории
```json
POST /api/types/1/categories/
Content-Type: application/json

{
    "name": "Инфраструктура"
}
```

Ответ:

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Инфраструктура"
        }
    ]
}
```

### Пример запроса на создание подкатегории
```json
POST /api/types/1/categories/1/subcategories/
Content-Type: application/json

{
    "name": "Proxy"
}
```

Ответ:

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Proxy"
        }
    ]
}
```

### Пример запроса на создание записи ДДС

```json
POST api/cashflows/
Content-Type: application/json

{
    "type": "Списание",
    "category": "Инфраструктура",
    "subcategory": "Proxy",
    "status": "Бизнес",
    "created_at": "2025-09-06",
    "amount": 1000,
    "comment": ""
}
```

Ответ:

```json
{
    "id": 1,
    "type": "Списание",
    "category": "Инфраструктура",
    "subcategory": "Proxy",
    "status": "Бизнес",
    "created_at": "2025-09-06",
    "amount": 1000,
    "comment": ""
}
```
