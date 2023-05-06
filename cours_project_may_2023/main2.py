import json


def print_last_5_operations():
    with open('operations.json') as f:
        data = json.load(f)

    # Отфильтровать и отсортировать операции по дате в обратном порядке
    executed_operations = sorted(filter(lambda op: op['state'] == 'EXECUTED', data), key=lambda op: op['date'],
                                 reverse=True)

    # Вывести список из 5 последних операций в заданном формате
    for op in executed_operations[:5]:
        date = op['date']
        description = op['description']
        from_acc = op['from'] or 'Карта'
        to_acc = op['to']
        amount, currency = op['operationAmount'].split()
        masked_from_acc = ' '.join([from_acc[:4], 'XX**', '****', from_acc[-4:]])
        masked_to_acc = '**' + to_acc[-4:]
        print(f'{date} {description}\n{masked_from_acc} -> Счет {masked_to_acc}\n{amount} {currency}\n')

#'''***************************************************'''

# импортируем функцию из файла с реализацией
#from operations import print_last_operations

# вызываем функцию для вывода 5 последних выполненных операций
print_last_5_operations(5)
