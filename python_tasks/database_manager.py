from datetime import datetime
from connect_to_database import ConnectDB
import logging

class DatabaseManager:
    def __init__(self):
        self.cursor = ConnectDB()

        # Для выполнения запросов
    def select(self):
        request = """with rank_client_amount as (
                        select cl.full_name, sum(amount) amount_purchase,
                        dense_rank() over (order by sum(amount) desc) rnk
                        from clients cl
                        join cards c on cl.id = c.client_id 
                        join transactions t on c.id = t.card_id
                        where t.transaction_type = 'Покупка'
                        group by full_name
                        )
                        select full_name, amount_purchase 
                        from rank_client_amount
                        where rnk = 1"""
        self.cursor.query(request, None)
        logging.info("Запрос выполнен успешно!")
        return self.cursor.one_line()


    #Чтобы не заходить всё время в БД и смотреть какой максимальный ID
    def get_id_client(self):
        request = """SELECT id FROM clients
                         ORDER BY id DESC
                         LIMIT 1"""
        self.cursor.query(request, None)
        return self.cursor.one_line()

    #Чтобы не заходить всё время в БД и смотреть какой максимальный ID
    def get_id_card(self):
        request = """SELECT id FROM cards
                         ORDER BY id DESC
                         LIMIT 1"""
        self.cursor.query(request, None)
        return self.cursor.one_line()

    # Вставка данных для таблицы clients
    def insert_info_clients(self, id, full_name, email, phone):
        request = """INSERT INTO clients (id, full_name, email, phone, registration_date) VALUES
        (%s, %s, %s, %s, %s)"""
        self.cursor.query(request, (id, full_name, email, phone, datetime.now().replace(microsecond=0)))
        return self.cursor.status()

    # Вставка данных для таблицы cards
    def insert_client_cards(self, id, client_id, card_number, card_type, issue_date, expiry_date, status):
        request = """INSERT INTO cards (id, client_id, card_number, card_type, issue_date, expiry_date, status) VALUES
        (%s, %s, %s, %s, %s,  %s, %s)"""
        self.cursor.query(request, (id, client_id, card_number, card_type, issue_date, expiry_date, status))
        return self.cursor.status()

    # Вставка данных для таблицы transactions
    def insert_card_transaction(self, id, card_id, transaction_date, amount, transaction_type, description):
        request = """INSERT INTO transactions 
        (id, card_id, transaction_date, amount, transaction_type, description) 
        VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.query(request, (id, card_id, transaction_date, amount, transaction_type, description))
        return self.cursor.status()

    # Автоматически закрывает соединение при ошибке или успешном выполнении кода
    def __del__(self):
        self.cursor.close()