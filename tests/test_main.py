"""
Tests for Main Module
----------------------

Tests in this project primarily are a showcase to demonstrate awareness of testdriven development.
But they were also used along the development of the basic functionality, to work around
unpacking. I know, that 'data mocking' could be an opportunity, but for now this approach
should work. Because this should primarily a showcase, there is no full test-coverage for
this project.

Usage:
    For usage the directory were ur zip-file is located has to be given. Please hardcode the
    [main_zip_path] in class TestModul. The Test-Code is structured in a way that the
    zip-File (as it is downloaded from the given website) is permanently unpacked in the
    given path and could be used in these tests. There will no interaction with a database
    in the tests of test_event_series.py, test_student.py and test_main.py, so there is no
    need to run one.

Data download:
    https://www.physionet.org/content/wearable-exam-stress/1.0.0/

:Modul: test_main
:Author: Benjamin Gaube
:Date: 2023-10-12
"""

import os
import tempfile
import zipfile
import unittest

from src.main import unzip_data, unzip_it, generator_length, student_factory, FILENAME


class TestModul(unittest.TestCase):

    main_zip_path = r'C:\tests'  # TODO: enter the folder path to the zip-file here

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
