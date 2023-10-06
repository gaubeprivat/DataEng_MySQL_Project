"""




"""

# TODO local imports

import os
import zipfile
import tempfile


def generator_length():
    pass


def student_factory(path):
    # TODO yield student-object
    pass


def write_database():
    pass  # maybe a function to store information into db


def calculate_hrv(temp_dir):
    # give status message --> call generator_length()
    # for-loop over student_factory()

    # connect to database
    # use Student-information to calculate hrv
    pass


def _unzip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def unzip_data(main_zip_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        _unzip(main_zip_path, temp_dir)

        inner_zip_path = os.path.join(temp_dir, 'Data.zip')
        _unzip(inner_zip_path, temp_dir)
        # TODO Function call mit func(temp_dir)  (func = calculate_hrv())


if __name__ == '__main__':

    path = r'C:\Datein Benjamin\playground\Python\data\projekt02\a-wearable-exam-stress-dataset-for-predicting-cognitive-performance-in-real-world-settings-1.0.0.zip'
    # path = input()# TODO input path

    try:
        unzip_data(path)
    except FileNotFoundError:
        print(f'invalid path given: {path}')

    # TODO call creat_schema.py
    # TODO call write_database
