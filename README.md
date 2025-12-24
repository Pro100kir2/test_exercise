# README.md

## Стандарт документации
Решение придерживается **Google Python Style Guide** для docstrings[](https://google.github.io/styleguide/pyguide.html). 
Это обеспечивает ясные, краткие и единообразные описания функций и классов.

## Используемые библиотеки (MIT или эквивалент)
- FastAPI (MIT) — https://github.com/tiangolo/fastapi
- pydantic (MIT) — https://github.com/pydantic/pydantic
- uvicorn (BSD) — https://github.com/encode/uvicorn
- requests (Apache 2.0) — https://github.com/psf/requests

## Структура предполагаемого okved.json
Файл должен быть списком объектов вида:
```json
[
  {"phone_end": "1234567", "code": "62.01", "name": "Разработка компьютерного ПО"},
  {"phone_end": "987654", "code": "47.11", "name": "Торговля розничная в неспециализированных магазинах"}
]
```

## Для запуска необходимо отправить запрос формата :
```curl -X 'POST' \
  'http://127.0.0.1:8000/find-okved' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "phone": "79121234567"
}
```# test_exercise
