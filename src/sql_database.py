"""
Modul: sql_database
Author: Benjamin Gaube
Date: 2023-10-09
"""  # TODO

# check if there is already a schema/database
# if yes - ask if it realy shall be overwritten "tip y/n"
# y -> overwrite / n -> raise Error and catch it in main to finish without processing

from time import sleep
from contextlib import contextmanager

import mysql.connector
from mysql.connector.connection import MySQLConnection

@contextmanager
def connect_to_localhost(database=None):
    """
    Establish and manage a connection to a MySQL database on localhost.

    :param database: str, Optional. The name of the database to connect to.
                     Default is None.
    :yield: MySQLConnection, The database connection object.
    :raise mysql.connector.Error: If unable to establish connection after 5 retries.
    """
    db = None
    try:
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database=database
            )
        except mysql.connector.Error:
            tries = 0
            while True:
                if tries > 5:
                    raise mysql.connector.Error('Could not connect to database')
                sleep(60)
                try:
                    db = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='',
                        database=database
                    )
                    break

                except mysql.connector.Error:
                    tries += 1

        yield db  # The connection is used here

    finally:
        if db is not None:
            db.close()


def create_schema(schema_name: str):
    """
    
    
    """ # TODO

    with connect_to_localhost() as db:

        cursor = db.cursor()

        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {schema_name}')
        cursor.execute(f'USE {schema_name}')

        cursor.execute('''
        CREATE TABLE dataset (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student VARCHAR(5) UNIQUE
        )
        ''')

        cursor.execute('''
        CREATE TABLE exam (
            id INT AUTO_INCREMENT PRIMARY KEY,
            term VARCHAR(10)
        )    
        ''')

        cursor.execute('''
        CREATE TABLE hrv (
            id INT AUTO_INCREMENT PRIMARY KEY,
            parameter VARCHAR(15)
        )
        ''')

        cursor.execute('''
        CREATE TABLE inter_beat_interval (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT, 
            term_id INT,
            ibi_value_id INT,
            ib_value FLOAT,
            timestamp INT,
            FOREIGN KEY (student_id) REFERENCES dataset(id) ON DELETE CASCADE,
            FOREIGN KEY (term_id) REFERENCES exam(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE master_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            term_id INT,
            grade INT,
            nni_mean FLOAT,
            sdnn FLOAT,
            number_of_ibi INT,
            FOREIGN KEY (student_id) REFERENCES dataset(id) ON DELETE CASCADE,
            FOREIGN KEY (term_id) REFERENCES exam(id)                    
        )
        ''')

        cursor.execute('''
        CREATE TABLE window_values (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            term_id INT,
            parameter_id INT,
            parameter VARCHAR(15),
            hrv_value_id INT,
            hrv_value FLOAT,
            timestamp INT,
            FOREIGN KEY (student_id) REFERENCES dataset(id) ON DELETE CASCADE,
            FOREIGN KEY (term_id) REFERENCES exam(id),
            FOREIGN KEY (parameter_id) REFERENCES hrv(id)
        )
        ''')

        db.commit()


if __name__ == '__main__':
    create_schema('application_project_gaube')  # hardcoded
