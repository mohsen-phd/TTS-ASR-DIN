"""This is a module for generating question string."""


from collections.abc import Iterator

from sentence_generator.questions import DigitQuestions, Questions


class Generator:
    """This is a class responsible for generating the questions."""

    def __init__(self) -> None:
        """Initialize the method and create the list of Questions."""
        self.question_list = [
            DigitQuestions("number " + i, [str(i)])
            for i in [
                "one",
                "two",
                "three",
                "Four",
                "Five",
                "six",
                "seven",
                "eight",
                "nine",
            ]
        ]

    def next_item(
        self,
    ) -> Iterator[Questions]:
        """Iterate over list of questions and return one question at a time.

        Yields:
            questions: one question from the list
        """
        for question in self.question_list:
            yield question
