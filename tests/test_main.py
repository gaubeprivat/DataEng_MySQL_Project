"""
Modul: test_main
Author: Benjamin Gaube
Date: 2023-07-24

Info:
        Just a short showcase to demonstrate awareness of testdriven development.
        There will be no full test-coverage for this project.

        For usage please hardcode the path were ur zip-file is located.
"""

import unittest
import os
import tempfile

from src.main import unzip_data, unzip_it, FILENAME

directory = r'C:\Dateien Benjamin\playground\Python\data\projekt02'  # TODO: r'C:\Users\User\Downloads'
path = os.path.join(directory, FILENAME + '.zip')


class TestModule(unittest.TestCase):

    def test_unpacking_outer(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            unzip_it(path, temp_dir)
            content = os.listdir(os.path.join(temp_dir, FILENAME))
            self.assertIn('Data.zip', content)
            self.assertIn('StudentGrades.txt', content)

    def test_unpacking_inner(self):
        def test_it(path_to):
            content = os.listdir(os.path.join(path_to, 'Data'))
            self.assertIn('S1', content)
            self.assertIn('S5', content)
            self.assertIn('S10', content)

            content = os.listdir(os.path.join(path_to, r'Data\S3'))
            self.assertIn('Final', content)
            self.assertIn('Midterm 2', content)

            content = os.listdir(os.path.join(path_to, r'Data\S3\Midterm 1'))
            self.assertIn('IBI.csv', content)

        unzip_data(path, test_it)


if __name__ == '__main__':
    unittest.main()
