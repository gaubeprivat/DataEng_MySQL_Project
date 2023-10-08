"""




""" # TODO

import os
import zipfile
import tempfile
from typing import Generator

from src.student import Student

FILENAME = r'a-wearable-exam-stress-dataset-for-predicting-cognitive-performance-in-real-world-settings-1.0.0'


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
            raise  # TODO: entfernen
            print(f'invalid path given: {main_zip_path}')


def generator_length(temp_dir: str) -> int:
    return len(os.listdir(os.path.join(temp_dir, 'Data')))


def student_factory(temp_dir: str) -> Generator[Student, None, None]:
    """
    Creates a generator yielding Student objects.

    This function generates Student objects, each containing relevant information,
    by traversing through the student data located in the specified temporary directory.

    :param temp_dir: str, The path to the temporary directory containing the data.
    :yield: Student, Yields Student objects.
    :example:
        >>> student_gen = student_factory('path/to/temp_dir')
        >>> next(student_gen)
        <Student object at 0x...>
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



def write_into_db():
    pass  # maybe a function to store information into db


def calculate_hrv(temp_dir):
    # give status message --> call generator_length()
    # call Student.get_grades() to get a dictionary of all grades
    # the grades have to passed to the student object.. how? further function?

   for stud in student_factory(temp_dir):
        pass
        # connect to database

        # use Student-information to calculate hrv
        # use write_into_db() to store the new calculated parameters into db





if __name__ == '__main__':

    path = os.path.join(r'C:\Dateien Benjamin\playground\Python\data\projekt02', FILENAME+'.zip')
    # path = input()# TODO input path

    # TODO call create_schema.py
    unzip_data(path, calculate_hrv)


