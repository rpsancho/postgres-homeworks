"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import os.path
import csv

DATABASE = 'north'
USER = 'postgres'
PASSWORD = '1'

DATA_DIR = os.path.abspath('./north_data')
CUSTOMERS_DATA = os.path.join(DATA_DIR, 'customers_data.csv')
EMPLOYEES_DATA = os.path.join(DATA_DIR, 'employees_data.csv')
ORDERS_DATA = os.path.join(DATA_DIR, 'orders_data.csv')


def write_csv_to_table(file_path: str, table_name: str, cursor):
    with open(file_path, 'r', newline='', encoding='UTF-8') as csvfile:
        csvreader = csv.reader(csvfile)

        # get and skip header
        header = next(csvreader)

        col_list = ', '.join(header)
        placeholders = ', '.join('%s' for _ in header)

        for row in csvreader:
            cursor.execute(f"INSERT INTO {table_name} ({col_list}) VALUES ({placeholders});", row)


def main():
    with psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD) as conn:
        with conn.cursor() as cur:
            write_csv_to_table(CUSTOMERS_DATA, 'customers', cur)
            write_csv_to_table(EMPLOYEES_DATA, 'employees', cur)
            write_csv_to_table(ORDERS_DATA, 'orders', cur)
        conn.commit()


if __name__ == "__main__":
    main()
