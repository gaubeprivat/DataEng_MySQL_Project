"""
Modul: sql_database
Author: Benjamin Gaube
Date: 2023-10-09
"""  # TODO

# check if there is already a schema/database
# if yes - ask if it realy shall be overwritten "tip y/n"
# y -> overwrite / n -> raise Error and catch it in main to finish without processing

from time import sleep

import mysql.connector
from mysql.connector.connection import MySQLConnection


def connect_to_localhost(database: str = None) -> MySQLConnection:
    """
    Establish a connection to a MySQL database on localhost.

    This function attempts to establish a connection to a MySQL
    database running on localhost using the 'root' user and no password.
    If the initial connection attempt fails, the function will try to
    reconnect up to 5 times, waiting 60 seconds between each attempt.

    :param database: The name of the database to connect to. Default is None.
    :type database: C{str}
    :return: The database connection object.
    :rtype: L{MySQLConnection}
    :raise mysql.connector.Error: If unable to establish connection after 5 retries.
    """

    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database=database
        )
    # if the connection to db isn't possible wait 60 seconds and try again.. try 5 times
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

    return db


def create_schema(schema_name: str):
    db = connect_to_localhost()

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
        value_id INT,
        value FLOAT,
        timestamp INT,
        FOREIGN KEY (student_id) REFERENCES dataset(id) ON DELETE CASCADE,
        FOREIGN KEY (term_id) REFERENCES exam(id),
        FOREIGN KEY (parameter_id) REFERENCES hrv(id)
    )
    ''')

    db.commit()


if __name__ == '__main__':
    create_schema('application_project_gaube')
