import json
from datetime import datetime

def load_data():
    '''
    Загрузить данные из файла "operations.json"
    '''
    with open('operations.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def filtered_data(data, filter_from=False):
    '''
    Отфильтровать только выполненные операции
    '''
    data = [x for x in data if "state" in x and x["state"] == "EXECUTED"]
    if filter_from:
        data = [x for x in data if "from" in x]
    return data

def last_operations(data, count_last_operations):
    '''
    Отфильтровать операции по дате в обратном порядке
    '''
    data = sorted(data, key=lambda x: x["date"], reverse=True)
    data = data[:count_last_operations]
    return data

def format_operation(data):
    '''
    Обработать информацию из словарей и вывести на экран 5 последних операций
    '''
    # Создает пустой список
    formatted_data = []
    for info in data:

        # Преобразует строку даты из формата "YYYY-MM-DDTHH:mm:ss" в формат "DD.MM.YYYY"
        date = datetime.strptime(info["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        description = info["description"]

        # Маскирует номер счета в формате **XXXX
        recipient = f"{info['to'].split()[0]} **{info['to'][-4:]}"
        operations_amount = f"{info['operationAmount']['amount']} {info['operationAmount']['currency']['name']}"
        if "from" in info:
            sender = info["from"].split()
            from_bill = sender.pop(-1)

        # Маскирует номер карты в формате XXXX XX** **** XXXX
            from_bill = f"{from_bill[:4]} {from_bill[4:6]}** **** {from_bill[-4:]}"
            from_info = " ".join(sender)
        else:
            from_info, from_bill = "", ""

        # Возвращает в main список из 5 последних операций в нужном формате
        formatted_data.append(f"""\
{date} {description} 
{from_info} {from_bill} -> {recipient}
{operations_amount}
""")
    return formatted_data
