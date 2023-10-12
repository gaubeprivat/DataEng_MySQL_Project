"""
Student Module
-------------------------------------------

This module provides the Student object which stores the Student ID, the temporary
path, information about the grades per term and on event_series object which provides
further information about the HRV and some functionality.

The static methode provides functionality to get the grades from a specific txt-file.

:Modul: student
:Author: Benjamin Gaube
:Date: 2023-10-12
"""


import os
import re
from typing import Dict

from src.event_series import InterBeatInterval


class Student:
    """
    Represents a student and manages associated data and functionality.

    The Student class provides functionality to handle a student's data which
    includes student identification, grades, and physiological data (IBI). Methods
    for extracting grade information and handling IBI data are included.

    :ivar path: str, Absolute path to the student's data directory.
    :ivar student_id: str, A unique identifier for the student.
    :ivar grades: dict, Nested dictionary containing the student's grade information.
    :ivar _ibi: InterBeatInterval or None, An object that stores and manages the student's IBI data.
    """

    def __init__(self, temp_path, student_id, grades):
        self.path = os.path.join(temp_path, student_id)
        self.student_id = student_id
        self.grades = grades
        self._ibi = None

    @property
    def ibi(self) -> InterBeatInterval:
        """
        Accessor for the '_ibi' attribute to safely access the IBI object.

        :return: InterBeatInterval, The IBI object associated with the student.
        """
        return self._ibi

    @ibi.setter
    def ibi(self, temp_dir):
        """
        Setter for the '_ibi' attribute to initialize the IBI object.

        :param temp_dir: str, Directory containing the IBI data.
        :raise FileNotFoundError: If required IBI data folders are not found.
        """

        check_content = ['Final', 'Midterm 1', 'Midterm 2']

        for entry in check_content:
            if entry not in os.listdir(temp_dir):
                raise FileNotFoundError(f'Missing {entry} folder in {temp_dir}')

        # initialize object
        self._ibi = InterBeatInterval(temp_dir)

    @staticmethod
    def extract_grades(file_path: str) -> Dict[str, Dict[str, int]]:
        """
        Extracts grade information from a text file and organizes it in a nested dictionary.

        :param file_path: str, path to the text file containing the grade information.
        :return: Dict[str, Dict[str, int]], a nested dictionary containing the organized grade information.
        """

        EXAM_KEY_TRANSLATION = {
            'MIDTERM 1': 'mid1',
            'MIDTERM 2': 'mid2',
            'FINAL (OUT OF 200)': 'final'
        }

        with open(file_path, 'r') as file:
            lines = file.readlines()

        grades = {}
        current_exam = None

        for line in lines:
            # Checks if "GRADES -" is contained in the current line.
            if "GRADES -" in line:
                # Uses a regex to extract the name of the exam from the line and store it in current_exam.
                exam_name_extracted = re.search(r'GRADES - (.+)', line).group(1)
                # Translates the extracted exam name to the desired key format and sets it as current_exam.
                current_exam = EXAM_KEY_TRANSLATION.get(exam_name_extracted, exam_name_extracted)
                # Adds a new empty dictionary to grades with the key of the currently processed exam.
                grades[current_exam] = {}
            # Checks if "–" is in the current line, indicating it's a line with a student ID and a score.
            elif "–" in line:
                # Uses another regex to extract the student ID and score from the line.
                student_id, score = re.search(r'(S\d+) – (\d+)', line).groups()

                # Remove leading zeros from the student ID, e.g., "S01" becomes "S1"
                student_id = "S" + str(
                    int(student_id[1:]))  # Convert numbers to int to remove leading zero and then back to str

                # Adds the score to the grades dictionary, indexed by the current exam and student ID.
                grades[current_exam][student_id] = int(score)

        return grades
