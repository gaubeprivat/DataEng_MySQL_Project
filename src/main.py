"""




""" # TODO

# TODO local imports

import os
import zipfile
import tempfile


FILENAME = r'a-wearable-exam-stress-dataset-for-predicting-cognitive-performance-in-real-world-settings-1.0.0'


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


def unzip_it(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def unzip_data(main_zip_path, func=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            unzip_it(main_zip_path, temp_dir)
            print('Successfully unpacked outer zip-File')

            inner_zip_path = os.path.join(temp_dir, FILENAME, 'Data.zip')
            unzip_it(inner_zip_path, temp_dir)
            print('Successfully unpacked inner zip-File')

            if func is not None:
                func(temp_dir)

        except FileNotFoundError:
            print(f'invalid path given: {path}')


        # TODO Function call mit func(temp_dir)  (func = calculate_hrv())


def testf(temp_dir):
    import pandas as pd
    pd.read_csv(os.path.join(temp_dir, r'Data\S1\Final\IBI.csv'), encoding='utf-8-sig')
    print('hallo i habs gelese')


if __name__ == '__main__':

    path = os.path.join(r'C:\Dateien Benjamin\playground\Python\data\projekt02', FILENAME+'.zip')
    # path = input()# TODO input path

    # TODO call creat_schema.py
    unzip_data(path)


