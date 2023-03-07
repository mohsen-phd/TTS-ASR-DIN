"""Module for storing question and their validation method."""
from abc import ABC, abstractmethod


class Questions(ABC):
    """Abstract class for questions. Each type of question must use this api."""

    def __init__(
        self, question: str, main_words: list[str], category: str = None
    ) -> None:
        """Initialize the questions object by storing the text of the question.

        Args:
            question (str): question to store.
            main_words (list[str]): words of interest in the sentence that should
                be used to infer answer from WordNet.
            category (str): Word category to check against WordNet.
        """
        self.question = question
        self.answer: str = None
        self.main_words = main_words
        self.category = category

    @abstractmethod
    def check_answer(self, answer: str):
        """Based on question type, check if the answer is correct or not.

        Args:
            answer (str): answer to the question givern by the patient.
        """
        pass


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
        category: str = None,
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
        super().__init__(question, main_words, category)
        self.self_check = self_check

    def check_answer(
        self,
        answer: str,
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
