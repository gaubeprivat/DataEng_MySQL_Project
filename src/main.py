"""




""" # TODO


import os
import zipfile
import tempfile
import datetime as dt
import timeit
from typing import Generator

import mysql.connector

from src.student import Student
from src.sql_database import create_schema, connect_to_localhost

directory = r'C:\tests'
schema = 'application_project_gaube'
FILENAME = r'a-wearable-exam-stress-dataset-for-predicting-cognitive-performance-in-real-world-settings-1.0.0'


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def unzip_it(zip_path: str, extract_to: str) -> None:

    """
    Extracts the contents of a zip file to a specified location.

    This function takes a path to a zip file and a target directory as input
    and extracts all contents of the zip file to the target directory.

    :param zip_path: str, The path to the zip file to be extracted.
    :param extract_to: str, The directory to which the contents of
        the zip file should be extracted.
    :return: None
    """

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def unzip_data(main_zip_path: str, func: callable = None) -> None:
    """
    Extracts data to a temporary directory and optionally applies a function
    to it.

    The function takes the path to the zip file and a function to apply on the
    data (if provided). Firstly, it unzips the main zip file to a temporary
    directory, then looks for and unzips an inner zip file named 'Data.zip'
    contained within it. If a function is provided, it is applied to the
    temporary directory.

    :param main_zip_path: str, The path to the main zip file to be extracted.
    :param func: callable, An optional function to apply to the data after extraction.
        It should take one argument: the path to the directory where the data
        was extracted. Default is None, meaning no function will be applied.
    :return: None
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            unzip_it(main_zip_path, temp_dir)
            print('Successfully unpacked outer zip-File')

            inner_zip_path = os.path.join(temp_dir, FILENAME, 'Data.zip')
            unzip_it(inner_zip_path, temp_dir)
            print('Successfully unpacked inner zip-File')

            if func is not None:
                func(os.path.join(temp_dir))

        except FileNotFoundError:
            raise  # TODO: delet
            print(f'invalid path given: {main_zip_path}. Code has not executed.')


def generator_length(temp_dir: str) -> int:
    return len(os.listdir(os.path.join(temp_dir, 'Data')))


def student_factory(temp_dir: str) -> Generator[Student, None, None]:
    """
    Creates a generator yielding Student objects.

    This function generates Student objects, each containing relevant information,
    by traversing through the student data located in the specified temporary directory.

    :param temp_dir: str, The path to the temporary directory containing the data.
    :yield: Student, Yields Student objects.
    """

    students_list = os.listdir(os.path.join(temp_dir, 'Data'))
    students_grades = Student.extract_grades(os.path.join(temp_dir, FILENAME, 'StudentGrades.txt'))
    term_keys = [key for key in students_grades]

    for student_id in students_list:
        # reorganize grades of the student as list [mid1, mid2, final]
        grades = [
            students_grades[term_keys[0]][student_id],
            students_grades[term_keys[1]][student_id],
            students_grades[term_keys[2]][student_id]
        ]

        yield Student(os.path.join(temp_dir, 'Data'), student_id, tuple(grades))


def write_into_db():
    pass  # maybe a function to store information into db


def process_data(temp_dir):
    """

    .........calculate hrv for each student and store the values along with grades into db

    """

    #TODO
    expected_iterations = generator_length(temp_dir)
    start_dt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_t = timeit.default_timer()
    error_count = 0

    gen = student_factory(temp_dir)

    for i, stud in enumerate(gen):

        clear()
        print(f'Calculation of {expected_iterations} datasets started: {start_dt}')
        print(f'Actually in the {i + 1} run. Processing data of student: {stud.student_id}')
        print(f'Calculation to {round(i / expected_iterations * 100, 2)}% completed.')
        time_per_ds = 'unknown' if i < 2 else (timeit.default_timer() - start_t) / i
        if i >= 2:
            print(f'predicted tim: {round((time_per_ds * (expected_iterations - i)) / 3600, 2)}h')
        print(f'{error_count} errors occurred')
        
        # open database connection with context manager
        with connect_to_localhost(schema) as db:
            cursor = db.cursor()

            try:
                # if the student doesn't exist: write it into db
                cursor.execute('INSERT INTO dataset (student) VALUES (%s)', (stud.student_id,))
                cursor.execute('SELECT LAST_INSERT_ID()')
                last_id = cursor.fetchone()[0]
            except mysql.connector.IntegrityError as e:
                # if the student already in db: delete old entry, write..
                if 'Duplicate entry' in str(e):
                    print(f'Duplicate entry {stud.student_id} for key student detected. Deleting...')
                    cursor.execute(f"DELETE FROM dataset WHERE student = '{stud.student_id}'")
                    db.commit()
                    cursor.execute('INSERT INTO dataset (student) VALUES (%s, %s)', (stud.student_id,))

                    cursor.execute('SELECT LAST_INSERT_ID()')
                    last_id = cursor.fetchone()[0]
                else:
                    raise
                    # TODO: maybe outer try - except statment --> write log and continue with next student

            # TODO write exam table

            # TODO write parameter table

            # TODO use setter for ibi obj
            # TODO create inter_beat_interval table
            # TODO calculate sdnn, mean_nn

            # TODO create master_data table

            # TODO use static funtion-generator to yield moving window in for-loop
                # TODO calculate sdnn and mean_nn
                # TODO write window_values table

            db.commit()  # NOTE: LAST LINE OF CODE


if __name__ == '__main__':

    # directory = input()
    path = os.path.join(directory, FILENAME+'.zip')

    create_schema(schema)
    unzip_data(path, process_data)


