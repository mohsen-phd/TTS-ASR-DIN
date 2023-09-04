"""Get respond form command line."""
from get_response.base import CaptureResponse


class CLI(CaptureResponse):
    """Interface for the ASR system."""

    def get(self) -> str:
        """Get response from command line.

        Returns:
            str: File transcription.
        """
        return input("Enter your response: ")
