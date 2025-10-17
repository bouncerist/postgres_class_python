import psycopg2
from config import database_config
import logging
class ConnectDB:
    #Соединимся (инициализируем) к БД
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname=database_config.get("dbname"),
                user=database_config.get("user"),
                password=database_config.get("password"),
                host=database_config.get("host"),
                port=database_config.get("port")
            )
            self.cursor = self.connection.cursor()
            logging.info("Успешное подключение к базе данных")
        except psycopg2.OperationalError as e:
            logging.error(f"Ошибка подключения к базе данных: {e}")
            raise
        except Exception as e:
            logging.error(f"Ошибка подключения к базе данных: {e}")
            raise

    #Чтобы не повторять один и тот же код несколько раз (откат транзакции)
    def rollback_transactions(self):
        self.connection.rollback()
        logging.info("Откат транзакции")

    # Функция для выполнения запроса по типу: Select, Insert Into, возможны и другие запросы
    # принимает 2 аргумента: request (Insert Into или Select, возможны и другие запросы)
    # params: Этот аргумент принимается в случае команды Insert Into, где нужно передать названия столбцов и значение к ним
    def query(self, request, params):
        try:
            if params is None:
                self.cursor.execute(request)
            else:
                self.cursor.execute(request, params)
            self.connection.commit()
        except Exception as e:
            logging.error(f"Ошибка выполнения запроса: {request}: {e}")
            self.rollback_transactions()
            raise

    # Получения всех строк для запроса Select
    # В моём случае для ФИО клиента с максимальной суммой покупки
    # использую fetchall, так как клиентов с одинаковой максимальной суммой может быть несколько
    def all_lines(self):
        try:
            return self.cursor.fetchall()
        except psycopg2.InterfaceError as e:
            logging.error(f"Ошибка при получении всех строк: {e}")
            self.rollback_transactions()
            raise
        except psycopg2.OperationalError as e:
            logging.error(f"Ошибка при получении всех строк: {e}")
            self.rollback_transactions()
            raise
        except Exception as e:
            logging.error(f"Ошибка при получении всех строк: {e}")
            self.rollback_transactions()
            raise

    # Получение одной строки в случае выполнения запросы Select
    # В коде не используется, но пригодится в будущем
    def one_line(self):
        try:
            return self.cursor.fetchone()
        except psycopg2.InterfaceError as e:
            logging.error(f"Ошибка при получении строки: {e}")
            self.rollback_transactions()
            raise
        except psycopg2.OperationalError as e:
            logging.error(f"Ошибка при получении строки: {e}")
            self.rollback_transactions()
            raise
        except Exception as e:
            logging.error(f"Ошибка при получении строки: {e}")
            self.rollback_transactions()
            raise

    # Возвращает сообщение при выполнении кода запроса
    def status(self):
        return self.cursor.statusmessage

    # Закрываем соединение с БД
    def close(self):
        try:
            self.connection.close()
            self.cursor.close()
            logging.info("Соединение с БД закрыт!")
        except psycopg2.OperationalError as e:
            logging.error(f"Ошибка при закрытии соединения с БД: {e}")
            raise
        except Exception as e:
            logging.error(f"Ошибка при закрытии соединения с БД: {e}")
            raise