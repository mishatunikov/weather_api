# 🌤️ Weather API

Тестовое задание для позиции Backend-разработчика.  
REST API, предоставляющее **реальную** текущую погоду и прогноз на ближайшие 10 дней.  
Позволяет также **переопределить** прогноз вручную.

## 📡 Источник данных

Данные о погоде получаются из публичного сервиса **[Open-Meteo API](https://open-meteo.com/)**  
Для геокодирования городов используется **[Nominatim (OpenStreetMap)](https://nominatim.openstreetmap.org/)** через библиотеку **[geopy](https://geopy.readthedocs.io/)**.

## 🚀 Технологии

- Python 3.9+
- Django 4.2
- Django REST Framework
- SQLite
- Open-Meteo API
- Geopy

## Запуск
1. Скопируйте репозиторий:
```
https://github.com/mishatunikov/weather_api.git
```

2. Cоздайте и активируйте виртуальное окружение:

Если у вас Linux/macOS
```
python3 -m venv env
source env/bin/activate
```
Если у вас Windows
```
python -m venv env
source env/scripts/activate
```

3. Установить зависимости из файла requirements.txt:
```
pip install -r requirements/requirements.txt
```

4. Создайте файл .env и наполните его необходимыми переменными окружения (строго следуйте примеру .env_example).

5. Выполните миграции.
```
python manage.py migrate
```

6. Для управления созданными прогнозами через админку создайте суперпользователя.
```
python manage.py createsuperuser
```

7. Запустите проект.
```
python manage.py runserver
```

## Эндпоинты
### GET /api/weather/current/
Обязательный параметр запроса city.
Пример запроса: /api/weather/current?city=London

    Ответ:
        ```
        {
          "temperature": 22.1,
          "local_time": "16:45"
        }
        ```

### GET /api/weather/forecast/
Обязательные параметры запроса: city и date(dd.mm.yyyy)
Пример запроса: /api/weather/forecast?city=Paris&date=10.06.2025

Ответ:

    ```
    {
      "min_temperature": 11.1,
      "max_temperature": 24.5
    }
    ```

### POST /api/weather/forecast/

Пример тела запроса:
    
    ```
    {
      "city": "Berlin",
      "date": "11.06.2025",
      "min_temperature": 10.0,
      "max_temperature": 18.5
    }
    ```

Ответ:
- 201 Created — если создано
- 200 OK — если обновлено

## Особенности

- Прогнозы, заданные вручную, имеют приоритет над внешними данными (для /api/weather/forecast/).
