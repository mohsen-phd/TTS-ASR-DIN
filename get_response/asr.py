"""Run ASR and convert audio to text."""
import os
from abc import abstractmethod

from loguru import logger
from speechbrain.pretrained import EncoderDecoderASR

from get_response.base import CaptureResponse


class ASR(CaptureResponse):
    """Interface for the ASR system."""

    def __init__(self) -> None:
        """Initialize the class."""
        self.file_path = ""

    @abstractmethod
    def _transcribe(self) -> str:
        """Get a wav file address and return the transcription of it.

        Returns:
            str: transcribe of the file.
        """
        ...

    @abstractmethod
    def get(self) -> str:
        """Transcribe the input file.

        Returns:
            str: File transcription.
        """
        ...


class ARLibrispeech(ASR):
    """Use Attention and RNNLM trained on LibriSpeech to convert audio to text.

    url: https://huggingface.co/speechbrain/asr-crdnn-rnnlm-librispeech
    """

    def __init__(self) -> None:
        """Initialize the class by loading HugginFace models."""
        self.asr_model = EncoderDecoderASR.from_hparams(
            source="speechbrain/asr-crdnn-rnnlm-librispeech",
            savedir="models/asr/asr-crdnn-rnnlm-librispeech",
        )
        self.file_path = ""

    def _transcribe(self) -> str:
        """Get a wav file address and return the transcription of it.

        Returns:
            str: transcribe of the file.
        """
        result = self.asr_model.transcribe_file(self.file_path)
        basename = os.path.basename(self.file_path)
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            logger.warning(f"{basename} not found.")
        return result

    def get(self) -> str:
        """Transcribe the input file.

        Returns:
            str: File transcription.
        """
        return self._transcribe()
