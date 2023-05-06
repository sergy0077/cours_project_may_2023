import json

from datetime import datetime


def format_operation_date(date_str):
    # Функция преобразует строку даты из формата "YYYY-MM-DDTHH:mm:ss" в формат "DD.MM.YYYY"
    date = datetime.fromisoformat(date_str)
    return date.strftime('%d.%m.%Y')


def mask_card_number(card_number):
    # Функция заменяет номер карты на маску, оставляя первые 6 и последние 4 цифры
    return f"{card_number[:6]} {'*'*4} {card_number[-4:]}"


def mask_account_number(account_number):
    # Функция заменяет номер счета на маску, оставляя только последние 4 цифры
    return f"**{account_number[-4:]}"


def print_last_operations(file_path):
    with open(file_path) as f:
        operations = json.load(f)

    # Отфильтровываем только выполненные операции и сортируем по дате
    executed_operations = sorted(filter(lambda op: op['status'] == 'EXECUTED', operations), key=lambda op: op['created_at'])

    # Выбираем последние 5 операций
    last_operations = executed_operations[-5:]

    # Форматируем и выводим операции
    for op in last_operations:
        date_str = op['created_at']
        date = format_operation_date(date_str)

        description = op['description']

        from_account = op['from']['masked_number']
        from_account = mask_card_number(from_account) if op['from']['type'] == 'card' else mask_account_number(from_account)

        to_account = op['to']['masked_number']
        to_account = mask_account_number(to_account)

        amount = op['amount']
        currency = op['currency']['code']

        print(f"{date} {description}\n{from_account} -> Счет {to_account}\n{amount} {currency}\n")

print_last_operations('operations.json')

#28.01.2021 Списание наличных
#Visa Platinum 4276 **40 **21 -> Счет **9638
#20000.0 RUB

#12.02.2021 Пополнение счета
#Счет **7834 -> Visa Platinum 4276 **40 **21
#10000.0 RUB

#21.02.2021 Перевод на счет другому клиенту
#Visa Platinum 4276 **40 **21 -> Счет **3412
#5000.0 RUB

#10.03.2021 Перевод организации
#Visa Platinum 7000 79** **** 6361 -> Счет **9638
#82771.72 RUB

#25.03.2021 Перевод другому клиенту
#Visa Platinum 7000 79** **** 6361 -> Счет **3412
