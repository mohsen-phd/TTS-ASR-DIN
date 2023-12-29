"""Get respond form command line."""
from get_response.base import CaptureResponse
from colorama import Fore


class CLI(CaptureResponse):
    """Interface for the ASR system."""

    def get(self) -> str:
        """Get response from command line.

        Returns:
            str: File transcription.
        """
        return input(Fore.GREEN + "Enter your response: ")
