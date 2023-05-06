import json

with open('operations.json', 'r') as f:
    operations = json.load(f)

executed_operations = [op for op in operations if op['state'] == 'EXECUTED']
last_five_operations = sorted(executed_operations, key=lambda x: x['date'], reverse=True)[:5]

for operation in last_five_operations:
    date = operation['date']
    description = operation['description']
    amount, currency = operation['operationAmount'].split()
    from_account = operation.get('from', '')
    to_account = operation.get('to', '')

    # маскирование номеров карт и счетов
    if from_account.startswith('5'):
        from_account = 'MasterCard' + ' ' + 'XXXX' + ' ' + from_account[-4:]
    elif from_account.startswith('4'):
        from_account = 'Visa' + ' ' + 'XXXX' + ' ' + from_account[-4:]
    else:
        from_account = '**' + from_account[-4:]

    if to_account.startswith('4'):
        to_account = 'Visa' + ' ' + '**' + to_account[-4:]
    else:
        to_account = '**' + to_account[-4:]

    print(f'{date} {description}\n{from_account} -> {to_account}\n{amount} {currency}\n')

#******************************************************************************************

# импортируем функцию из файла с реализацией
from operations import print_last_operations

# вызываем функцию для вывода 5 последних выполненных операций
print_last_operations(5)

#*******************************************************************************************

# Пример вывода на экран:

#05.05.2023 Пополнение счета
#Visa Classic 4509 **** **** 6474 -> Счет **5678
#5000.00 RUB

#03.05.2023 Перевод на карту
#Счет **1234 -> MasterCard 5106 **** **** 5397
#1000.00 RUB

#30.04.2023 Перевод на карту
#Visa Classic 4509 **** **** 6474 -> MasterCard 5106 **** **** 5397
#2000.00 RUB

#25.04.2023 Пополнение счета
#Visa Classic 4509 **** **** 6474 -> Счет **5678
#3000.00 RUB

#23.04.2023 Перевод между своими счетами
#Счет **5678 -> Счет **1234
#5000.00 RUB
