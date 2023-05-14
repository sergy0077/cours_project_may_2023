from functions import load_data, filtered_data, last_operations, format_operation

# Последовательно вызываем функции из файла functions
data = load_data()
data = filtered_data(data, filter_from=True)
data = last_operations(data, count_last_operations=5)
data = format_operation(data)
# Запускаем цикл вывода 5 последних операций в нужном формате
print(f'\nВывод пяти последних транзакций:\n')
for info in data:
    print(info)