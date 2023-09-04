"""Base class for the response capturing system."""
from abc import ABC, abstractmethod


class CaptureResponse(ABC):
    """Interface for the ASR system."""

    @abstractmethod
    def get(self, *args, **kwargs) -> str:
        """Get a wav file address and return the transcription of it.

        Returns:
            str: transcribe of the file.
        """
        ...
