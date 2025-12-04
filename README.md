# TCP сервер

## Описание
Сервер на Python, который принимает HTTP-запросы и выводит в консоль

## Запуск
```



```
git clone https://github.com/Pewter71/tasks-for-pumping.git
cd tasks-for-pumping

uv sync
source .venv/bin/activate
python -m src.main
```

После запуска открыть в браузере:
```
http://127.0.0.1:8080/
```

## Запуск тестового POST запроса
```
python -m src.test_request
```