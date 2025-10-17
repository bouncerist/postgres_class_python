import logging
from database_manager import DatabaseManager
from config import csv_paths
import csv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_logs.log'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    data = DatabaseManager()

    # Заполнение таблиц из data_for_tables/clients.csv
    with open(csv_paths.get("clients"), mode='r') as file:
        next(file)
        clients_data = csv.reader(file)
        for line in clients_data:
            data.insert_info_clients(line[0], line[1], line[2], line[3])

    # Заполнение таблиц из data_for_tables/cards.csv
    with open(csv_paths.get("cards"), mode='r') as file:
        next(file)
        cards_data = csv.reader(file)
        for line in cards_data:
            data.insert_client_cards(line[0], line[1], line[2], line[3], line[4], line[5], line[6])

    # Заполнение таблиц из data_for_tables/transactions.csv
    with open(csv_paths.get("transactions"), mode='r') as file:
        next(file)
        transactions_data = csv.reader(file)
        for line in transactions_data:
            data.insert_card_transaction(line[0], line[1], line[2], line[3], line[4], line[5])

    # ФИО клиента с максимальной суммой покупки
    result = data.select()
    print(f'ФИО: {result[0]} \nМакс. сумма покупки: {result[1]}')