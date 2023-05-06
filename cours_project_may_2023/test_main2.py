import json
from datetime import datetime
from typing import List

from operations import get_last_operations


def test_get_last_operations():
    # Создаем тестовые данные
    test_data = [
        {
            "id": 1,
            "date": "2022-01-01T00:00:00",
            "state": "EXECUTED",
            "operationAmount": {"amount": 100.0, "currency": "RUB"},
            "description": "Перевод",
            "from": "1111222233334444",
            "to": "12345678",
        },
        {
            "id": 2,
            "date": "2022-01-02T00:00:00",
            "state": "EXECUTED",
            "operationAmount": {"amount": 200.0, "currency": "RUB"},
            "description": "Перевод",
            "from": "5555666677778888",
            "to": "87654321",
        },
        {
            "id": 3,
            "date": "2022-01-03T00:00:00",
            "state": "EXECUTED",
            "operationAmount": {"amount": 300.0, "currency": "RUB"},
            "description": "Перевод",
            "from": "1111222233334444",
            "to": "56781234",
        },
        {
            "id": 4,
            "date": "2022-01-04T00:00:00",
            "state": "EXECUTED",
            "operationAmount": {"amount": 400.0, "currency": "RUB"},
            "description": "Перевод",
            "from": "1111222233334444",
            "to": "87654321",
        },
        {
            "id": 5,
            "date": "2022-01-05T00:00:00",
            "state": "EXECUTED",
            "operationAmount": {"amount": 500.0, "currency": "RUB"},
            "description": "Перевод",
            "from": "5555666677778888",
            "to": "56781234",
        },
        {
            "id": 6,
            "date": "2022-01-06T00:00:00",
            "state": "CANCELED",
            "operationAmount": {"amount": 600.0, "currency": "RUB"},
            "description": "Перевод",
            "from": "1111222233334444",
            "to": "56781234",
        },
    ]
    # Преобразуем дату из строки в объект datetime
    for data in test_data:
        data["date"] = datetime.fromisoformat(data["date"])

    # Создаем тестовый файл
    with open("test_operations.json", "w") as f:
        json.dump(test_data, f)

    # Вызываем функцию, которую тестируем
    last_operations = get_last_operations("test_operations.json", 5)

    # Проверяем результаты
    assert len(last_operations) == 5

    for i, op in enumerate(last_operations):
        assert op["date"] == test_data[-i-1]["date"].strftime("%d.%m.%Y")
        assert op["description"] == test_data[-i-1]["description"]
        assert op["from"]
