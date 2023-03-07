"""Module to extract information from patient response."""

from abc import ABC, abstractmethod


class AbstractExtractor(ABC):
    @abstractmethod
    def extract(self, answer: str) -> dict[str]:
        """Get the response as text, and return usable information as dict.

        Args:
            answer (str): patient response

        Returns:
            dict[str]: _description_
        """


class YesNoAnswer(AbstractExtractor):
    def extract(self, answer: str) -> dict[str]:
        if "yes" in answer.lower():
            return {"agree": True}
        elif "no" in answer.lower():
            return {"agree": False}
