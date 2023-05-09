"""Module for storing question and their validation method."""
from abc import ABC, abstractmethod


class Questions(ABC):
    """Abstract class for questions. Each type of question must use this api."""

    def __init__(self, question: str, main_words: list[str]) -> None:
        """Initialize the questions object by storing the text of the question.

        Args:
            question (str): question to store.
            main_words (list[str]): words of interest in the sentence that should
                be used to infer answer from WordNet.
        """
        self.question = question
        self.answer: str = ""
        self.main_words = main_words

    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        """Based on question type, check if the answer is correct or not.

        Args:
            answer (str): answer to the question givern by the patient.

        Returns:
            bool: Is a match or not.
        """
        pass


class DigitQuestions(Questions):
    """Class for modeling digit-in-noise test questions."""

    def check_answer(self, answer: str) -> bool:
        """Check the given number is the same as the one  presented to the patient.

        Args:
            answer (str): The patient's response.

        Returns:
            bool: Is a match or not.
        """
        if self.main_words[0].lower() in answer.lower():
            return True
        else:
            return False


class NameObjectQuestions(Questions):
    """Class to model this type of questions."""

    def check_answer(self, answer: str):
        """Check answer based on patient response and type of question.

        Args:
            answer (str): patient response
        """
        pass


class OppositeQuestions(Questions):
    """Class to model this type of questions."""

    def check_answer(self, answer: str):
        """Check answer based on patient response and type of question.

        Args:
            answer (str): patient response
        """
        pass


class SynonymQuestions(Questions):
    """Class to model this type of questions."""

    def __init__(
        self,
        question: str,
        main_words: list[str],
        category: str,
        self_check: bool = False,
    ) -> None:
        """Initialize the questions object by storing the text of the question.

        Args:
            question (str): question to store.
            main_words (list[str]): words of interest in the sentence that should
                be used to infer answer from WordNet.
            category (str): Word category to check against WordNet.
            self_check (bool): check if main_words are synonym,
                or the synonym is given by the patient.
        """
        super().__init__(question, main_words)
        self.self_check = self_check
        self.category = category

    def check_answer(
        self,
        answer: str,
        self_check: bool,
    ):
        """Check answer based on patient response and type of question.

        Args:
            answer (str): patient response
            self_check (bool): check if main_words are synonym,
                or the synonym is given by the patient.
        """
        pass


class SameCategoryQuestions(Questions):
    """Class to model this type of questions."""

    def check_answer(self, answer: str):
        """Check answer based on patient response and type of question.

        Args:
            answer (str): patient response
        """
        pass


class StatementQuestions(Questions):
    """Class to model this type of questions."""

    def check_answer(self, answer: str):
        """Check answer based on patient response and type of question.

        Args:
            answer (str): patient response
        """
        pass
