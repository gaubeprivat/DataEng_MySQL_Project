"""
Modul: test_main
Author: Benjamin Gaube
Date: 2023-10-08

Info:
    These tests primarily are a showcase to demonstrate awareness of testdriven development.
    There will be no full test-coverage for this project.

    For usage please hardcode the [main_zip_path] in class TestModul with the directory were ur zip-file is located.
"""

import os
import tempfile
import zipfile
import unittest

from src.main import unzip_data, unzip_it, generator_length, student_factory, FILENAME


class TestModul(unittest.TestCase):

    main_zip_path = r'C:\tests'  # TODO: enter the folder path of the zip-file here

    def setUp(self):
        """ define the setUp outside the class, to use it in multiple test_moduls"""

        self.path = os.path.join(TestModul.main_zip_path, FILENAME + '.zip')

        # make sure, that the zipfile is unzipped in the test-folder
        if FILENAME not in os.listdir(TestModul.main_zip_path):
            zipfile.ZipFile(self.path).extractall(TestModul.main_zip_path)

        self.unpacked_directory = os.path.join(TestModul.main_zip_path, FILENAME)

        # make sure, that the inner zip_file is unzipped
        if 'Data' not in self.unpacked_directory:
            zipfile.ZipFile(os.path.join(self.unpacked_directory, 'Data.zip')).extractall(self.unpacked_directory)


class TestMainModul(TestModul):

    def test_unpacking_outer(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            unzip_it(self.path, temp_dir)
            content = os.listdir(os.path.join(temp_dir, FILENAME))
            self.assertIn('Data.zip', content)
            self.assertIn('StudentGrades.txt', content)

    def test_unpacking_inner(self):
        def testing(path_to: str):
            content = os.listdir(os.path.join(path_to, 'Data'))
            self.assertIn('S1', content)
            self.assertIn('S5', content)
            self.assertIn('S10', content)

            content = os.listdir(os.path.join(path_to, r'Data\S3'))
            self.assertIn('Final', content)
            self.assertIn('Midterm 2', content)

            content = os.listdir(os.path.join(path_to, r'Data\S3\Midterm 1'))
            self.assertIn('IBI.csv', content)

        unzip_data(self.path, testing)

    def test_generator_length(self):
        length = generator_length(self.unpacked_directory)
        self.assertEqual(length, 10)

    def test_student_factory(self):  # tests for class Student in test_student.py
        students_list = []
        students_list_validate = ['S1', 'S3', 'S5', 'S7', 'S10']
        for stud in student_factory(os.path.join(self.unpacked_directory)):  # self.unpacked_directory
            students_list.append(stud.student_id)

        for stud in students_list_validate:
            self.assertIn(stud, students_list)

        self.assertEqual(len(students_list), 10)


if __name__ == '__main__':
    unittest.main()
