import pytest
import json
from datetime import datetime
from main import load_data, filtered_data, last_operations, format_operation

with open('operations.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def test_load_data():
    data = load_data()
    assert isinstance(data, list)
    assert all(isinstance(d, dict) for d in data)
    assert all(set(d.keys()) == {'id', 'state', 'date', 'operationAmount', 'description', 'from', 'to'} for d in data)

def test_filtered_data():
    data = [{'date': '2023-05-10', 'amount': 100, 'type': 'debit'},
            {'date': '2023-05-11', 'amount': 200, 'type': 'credit'},
            {'date': '2023-05-12', 'amount': 300, 'type': 'debit'}]
    filtered = filtered_data(data, filter_from=True)
    assert len(filtered) == 1
    assert filtered[0]['date'] == '2023-05-10'
    assert filtered[0]['amount'] == 100
    assert filtered[0]['type'] == 'debit'

def test_last_operations():
    data = [{'date': '2023-05-10', 'amount': 100, 'type': 'debit'},
            {'date': '2023-05-11', 'amount': 200, 'type': 'credit'},
            {'date': '2023-05-12', 'amount': 300, 'type': 'debit'},
            {'date': '2023-05-13', 'amount': 400, 'type': 'credit'},
            {'date': '2023-05-14', 'amount': 500, 'type': 'debit'},
            {'date': '2023-05-15', 'amount': 600, 'type': 'credit'}]
    last = last_operations(data, 3)
    assert len(last) == 3
    assert last[0]['date'] == '2023-05-15'
    assert last[0]['amount'] == 600
    assert last[0]['type'] == 'credit'
    assert last[1]['date'] == '2023-05-14'
    assert last[1]['amount'] == 500
    assert last[1]['type'] == 'debit'
    assert last[2]['date'] == '2023-05-13'
    assert last[2]['amount'] == 400
    assert last[2]['type'] == 'credit'

@pytest.fixture
def test_data():
    return [{'date': '2023-05-10T08:05:00Z', 'amount': 100, 'type': 'debit'},
            {'date': '2023-05-11T12:30:00Z', 'amount': 200, 'type': 'credit'},
            {'date': '2023-05-12T16:15:00Z', 'amount': 300, 'type': 'debit'}]

def test_format_operation(test_data):
    data = format_operation(test_data)
    assert len(data) == 3
    assert data[0]['date'] == '2023-05-10 08:05:00'
    assert data[1]['date'] == '2023-05-11 12:30:00'
    assert data[2]['date'] == '2023-05-12 16:15:00'