"""
Modul: student
Author: Benjamin Gaube
Date: 2023-10-07

Modul provides the student-object from the zip-file
"""  # TODO


import os
import re
from typing import Dict  # List, Tuple, Any, Callable

from src.event_series import InterBeatInterval


class Student:
    """
    
    """
    # TODO docstring

    def __init__(self, temp_path, student_id, grades):
        self.path = os.path.join(temp_path, student_id)
        self.student_id = student_id
        self.grades = grades
        self._ibi = None

    @property
    def ibi(self):
        return self._ibi

    @ibi.setter
    def ibi(self, temp_dir):

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
