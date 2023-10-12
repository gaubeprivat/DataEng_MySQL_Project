"""
Main Module of Package application_project
-------------------------------------------

This module serves as the main integration and orchestration point for processing
student data and physiological signals during various exams, given by:

a-wearable-exam-stress-dataset-for-predicting-cognitive-performance-in-real-world-settings-1.0.0.zip

It utilizes functionalities defined in complementary modules within the package to
extract data, calculate Heart Rate Variability (HRV) parameters for all students and
all exams, and store them alongside student information in a SQL database, which was
developed for this purpose.


Main Functions:
- `unzip_data()`: Extracts data of the zip-file into temporary directory
- `student_factory()`: Generator providing student-objects
- `calculate_hrv()`: simple hrv-calculations (mean_nni and sdnn)
- `process_data()`: Use the in this package provided functionality to process the data
                    and store them into the database

Usage:
    The used Data is free access and available on `https://www.physionet.org/content/wearable-exam-stress/1.0.0/`.
    The path to the downloaded zip-file hase to be hardcoded in the variable `directory`
    or alternatively the zip-file has to be in the directory `C:\tests`.

    A local MySQl server has to run. For this purpose I used XAMPP (https://www.apachefriends.org/de/index.html)
    with the default Settings (localhost Port `3306`, no password and user `root`).
    The necessary schema will automatically be created while running this code.

Contained Modules:
- `student.py`: Provides a student-object with all necessary information.
- `event_series.py`: Provides a further object which is used as attribute of Student
- `sql_database.py`: Provides the schema of the developed database and a contextmanager
                     for the connection to localhost.

:Author: Benjamin Gaube
:Date: 2023-10-12
"""


import os
import zipfile
import tempfile
import datetime as dt
import timeit
from typing import Generator, Tuple

import mysql.connector
import numpy as np

from src.student import Student
from src.sql_database import create_schema, connect_to_localhost
from src.event_series import InterBeatInterval

directory = r'C:\tests'  # TODO Enter the path to the downloaded zip-File here.
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
            unzip_it(inner_zip_path, os.path.join(temp_dir, FILENAME))
            print('Successfully unpacked inner zip-File')

            if func is not None:
                func(os.path.join(temp_dir, FILENAME))

        except FileNotFoundError:
            print(f'invalid path given: {main_zip_path}. Code has not executed.')
            raise


def generator_length(temp_dir: str) -> int:
    """
    Get the length of the generator object provided by student_factory().

    :param temp_dir: str, The path to the temporary directory containing the data.
    :return: int, Length of the generator.
    """
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
    students_grades = Student.extract_grades(os.path.join(temp_dir, 'StudentGrades.txt'))
    term_keys = [key for key in students_grades]

    for student_id in students_list:
        # reorganize grades of the student as list [mid1, mid2, final]
        grades = [
            students_grades[term_keys[0]][student_id],
            students_grades[term_keys[1]][student_id],
            students_grades[term_keys[2]][student_id]
        ]

        yield Student(os.path.join(temp_dir, 'Data'), student_id, tuple(grades))


def calculate_hrv(hrv_array: np.array) -> Tuple[float, float]:
    """
    Calculate the simple HRV parameters: nni_mean and SDNN.

    More complex time-domain parameters like RMSSD and SDANN do not make sense with
    this data because several inter-beat intervals are missing. Thus, there are
    numerous interruptions in the event series, making it not persistent.
    Consequently, it does not make sense to apply a Fourier transformation to
    calculate frequency-based parameters (e.g., High Frequency - Low Frequency Ratio).
    Furthermore, evaluating persistence with Detrended Fluctuation Analysis or other
    nonlinear methods will not lead to consistent data.

    :param hrv_array: np.array, Array containing inter beat intervals.
    :yield: tuple(float, float), Returning the mean nni and the SDNN.
    """

    return np.mean(hrv_array).round(2), np.std(hrv_array, ddof=0).round(2)


def process_data(temp_dir: str):
    """
    Process student and HRV data from a ZIP file and store structured Data into an SQL database.

    :param temp_dir: str, The path to the temporary directory containing the data.
    """

    # TODO
    expected_iterations = generator_length(temp_dir)
    start_dt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_t = timeit.default_timer()
    error_count = 0
    terms = ['mid1', 'mid2', 'final']

    gen = student_factory(temp_dir)

    for i, stud in enumerate(gen):

        clear()
        print(f'Calculation of {expected_iterations} datasets started: {start_dt}')
        print(f'Actually in the {i + 1} run. Processing data of student: {stud.student_id}')
        print(f'Calculation to {round(i / expected_iterations * 100, 2)}% completed.')
        time_per_ds = 'unknown' if i < 2 else (timeit.default_timer() - start_t) / i
        if i >= 2:
            print(f'estimated time remaining: {round((time_per_ds * (expected_iterations - i)) / 60, 2)} min')
        print(f'{error_count} errors occurred')
        
        # open database connection with context manager
        with connect_to_localhost(schema) as db:
            cursor = db.cursor()

            try:
                # add student to db
                try:
                    # if the student doesn't exist: write student
                    cursor.execute('INSERT INTO dataset (student) VALUES (%s)', (stud.student_id,))
                    cursor.execute('SELECT LAST_INSERT_ID()')
                    last_id = cursor.fetchone()[0]
                except mysql.connector.IntegrityError as e:
                    # if the student already in db: rewrite student
                    if 'Duplicate entry' in str(e):
                        print(f'Duplicate entry {stud.student_id} for key student detected. Deleting...')
                        cursor.execute(f"DELETE FROM dataset WHERE student = '{stud.student_id}'")
                        db.commit()
                        print(f'Successfully deleted {stud.student_id}. Rewriting...')
                        cursor.execute('INSERT INTO dataset (student) VALUES (%s)', (stud.student_id,))

                        cursor.execute('SELECT LAST_INSERT_ID()')
                        last_id = cursor.fetchone()[0]
                    else:
                        raise
            except Exception as e:
                with open(os.path.join(directory, 'error_log.txt'), 'a') as file:
                    error_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    file.write(f'Error in {stud.student_id} at {error_time}:\n {e}')
                    file.write('\n\n')
                continue

            # set ibi object for student
            stud.ibi = stud.path

            # process data and store it into db
            for j, term in enumerate(terms, start=1):
                ibi_df = getattr(stud.ibi, term)

                # fill table inter_beat_interval
                for value_id, row in ibi_df.iterrows():
                    cursor.execute(
                        'INSERT INTO inter_beat_interval (student_id, term_id, ibi_value_id, ibi_value, timestamp) '
                        'VALUES (%s, %s, %s, %s, %s)', (last_id, j, value_id + 1, int(row[1]), int(row[0]))
                    )
                db.commit()

                # process data
                duration = round((ibi_df.time.iloc[-1] - ibi_df.time.iloc[0]) / 3600, 2)  # recording duration in hours
                ibi_array = np.array(ibi_df.interval)
                nni_mean, sdnn = calculate_hrv(ibi_array)
                insert_into_master = (last_id, j, stud.grades[j - 1], float(nni_mean),
                                      float(sdnn), len(ibi_array), float(duration))

                # fill table master_data
                cursor.execute('INSERT INTO master_data (student_id, term_id, grade, nni_mean, sdnn, '
                               'number_of_ibi, duration_in_h) VALUES (%s, %s, %s, %s, %s, %s, %s)', insert_into_master)
                db.commit()

                window_generator = InterBeatInterval.moving_5min_window(ibi_df, term)

                for k, window_dic in enumerate(window_generator, start=1):
                    ibi_num = len(window_dic['intervals'])
                    if ibi_num < 3:
                        continue
                    hrv_parameters = calculate_hrv(window_dic['intervals'])

                    for par_id, value in enumerate(hrv_parameters, start=1):
                        # fill table window_values
                        cursor.execute('INSERT INTO window_values (student_id, term_id, window_id, timestamp, '
                                       'parameter_id, hrv_value, number_of_ibi) VALUES ( %s, %s, %s, %s, %s, %s, %s)',
                                       (last_id, j, k, int(window_dic['time']), par_id, float(value), ibi_num))

                db.commit()
            db.commit()


if __name__ == '__main__':

    # directory = input()
    path = os.path.join(directory, FILENAME+'.zip')

    create_schema(schema)
    unzip_data(path, process_data)
