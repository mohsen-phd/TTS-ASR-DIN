"""Module for storing question and their validation method."""
import random
from abc import ABC, abstractmethod


class Questions(ABC):
    """Abstract class for questions. Each type of question must use this api."""

    def __init__(self) -> None:
        """Initialize the questions object by storing the text of the question."""
        self.question = ""
        self.main_words = []

    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        """Based on question type, check if the answer is correct or not.

        Args:
            answer (str): answer to the question given by the patient.

        Returns:
            bool: Is a match or not.
        """
        pass

    @abstractmethod
    def get_stimuli(self) -> str:
        """Generate a sample stimuli.

        Returns:
            str: stimuli for the question.
        """
        pass


class DigitQuestions(Questions):
    """Class for modeling digit-in-noise test questions."""

    def __init__(self) -> None:
        """Initialize the questions object by storing the text of the question."""
        self.vocab_list = [
            "One",
            "Two",
            "Three",
            "Four",
            "Five",
            "Six",
            "Seven",
            "Eight",
            "Nine",
        ]
        super().__init__()

    def get_stimuli(self) -> str:
        """Generate a sample stimuli.

          Generate a sample stimuli consist of three words
          by randomly selecting from the list of vocab.

        Returns:
            str: stimuli for the question.
        """
        self.main_words = random.sample(self.vocab_list, 3)
        self.question = "The number is " + " ".join(self.main_words)
        return self.question

    def check_answer(self, answer: str) -> bool:
        """Check the given number is the same as the one  presented to the patient.

        Args:
            answer (str): The patient's response.

        Returns:
            bool: Is a match or not.
        """
        answer = answer.lower()
        correct_count = 0
        for word in self.main_words:
            if word.lower() in answer:
                correct_count += 1
                answer = answer.replace(word.lower(), "")

        if correct_count >= 2:
            return True
        else:
            return False
