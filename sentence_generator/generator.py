"""This is a module for generating question string."""
import enum


class QTypes(enum.Enum):
    """Store different type of catagories for questions."""

    name_object = 0
    opposite = 1
    synonym = 2
    same_category = 4
    statement = 5


class Generator:
    """This is a class responsible for generating the questions."""

    def __init__(self) -> None:
        """Initialize the method and create the list of sentences."""
        self.question_list: dict = {
            1: {
                "question": "Could you tell me the names of three different animals?",
                "type": QTypes.name_object,
            },
            2: {
                "question": """Could you provide me with the names of the
                                                    three capital cities?""",
                "type": QTypes.name_object,
            },
            3: {"question": "Please name three sports", "type": QTypes.name_object},
            4: {"question": "What is the opposite of good?", "type": QTypes.opposite},
            5: {
                "question": "Can you name three opposites  for the word clean?",
                "type": QTypes.opposite,
            },
            6: {
                "question": "What are some words with the same meaning as bright?",
                "type": QTypes.synonym,
            },
            7: {
                "question": "Is this statement true?  London is a city.",
                "type": QTypes.statement,
            },
            8: {
                "question": "Does reject  and decline have the same meaning?",
                "type": QTypes.synonym,
            },
            9: {
                "question": "are reindeer and camels both animals?",
                "type": QTypes.same_category,
            },
        }

    def next_item(
        self,
    ) -> str:
        """Iterate over list of questions and return one question at a time.

        Yields:
            str: one question from the list
        """
        for _, question in self.question_list.items():
            yield question
