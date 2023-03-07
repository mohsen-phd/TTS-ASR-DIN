"""This is a module for generating question string."""


from sentence_generator.questions import (
    NameObjectQuestions,
    OppositeQuestions,
    Questions,
    SameCategoryQuestions,
    StatementQuestions,
    SynonymQuestions,
)


class Generator:
    """This is a class responsible for generating the questions."""

    def __init__(self) -> None:
        """Initialize the method and create the list of Questions."""
        self.question_list = [
            NameObjectQuestions(
                "Could you tell me the names of three different animals?", ["animal"]
            ),
            NameObjectQuestions(
                "Could you provide me with the names of the three capital cities?",
                ["cities"],
            ),
            NameObjectQuestions("Please name three sports", ["sport"]),
            OppositeQuestions("What is the opposite of good?", ["good"]),
            OppositeQuestions(
                "Can you name three opposites  for the word clean?", ["clean"]
            ),
            SynonymQuestions(
                "What are some words with the same meaning as bright?", ["bright"]
            ),
            StatementQuestions(
                "Is this statement true?  London is a city.", ["london"], "city"
            ),
            SynonymQuestions(
                "Does reject  and decline have the same meaning?",
                ["reject", "decline"],
                self_check=True,
            ),
            SameCategoryQuestions(
                "are reindeer and camels both animals?",
                ["reindeer", "camels"],
                "animals",
            ),
        ]

    def next_item(
        self,
    ) -> Questions:
        """Iterate over list of questions and return one question at a time.

        Yields:
            questions: one question from the list
        """
        for question in self.question_list:
            yield question
