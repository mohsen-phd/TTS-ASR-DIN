"""This is a module for generating question string."""


class Generator:
    """This is a class responsible for generating the questions."""

    def __init__(self) -> None:
        """Initilize the method and create the list of sentences."""
        self.question_list = [
            "Could you tell me the names of three different animals?",
            "Could you provide me with the names of the three capital cities?",
            "Please name three sports",
            "What is the opposite of good?",
            "Can you name three opposites  for the word clean?",
            "What are some words with the same meaning as bright?",
            "Is this statement true?  London is a city.",
            "Does reject  and decline have the same meaning?",
            "are reindeer and camels both animals?",
        ]

    def next_item(
        self,
    ) -> str:
        """Iterate over list of questions and return one question at a time.

        Yields:
            str: one question from the list
        """
        for question in self.question_list:
            yield question
