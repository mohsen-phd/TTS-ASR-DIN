"""Run ASR and convert audio to text."""
from abc import ABC, abstractmethod
import os

from loguru import logger
from speechbrain.pretrained import EncoderDecoderASR


class ASR(ABC):
    """Interface for the ASR system."""

    @abstractmethod
    def transcribe(self, src: str) -> str:
        """Get a wav file address and return the transcription of it.

        Args:
            src (str): Address of the audio file.

        Returns:
            str: transcribe of the file.
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

    def transcribe(self, src: str) -> str:
        """Get a wav file address and return the transcription of it.

        Args:
            src (str): Address of the audio file.

        Returns:
            str: transcribe of the file.
        """
        result = self.asr_model.transcribe_file(src)
        basename = os.path.basename(src)
        try:
            os.remove(src)
        except FileNotFoundError:
            logger.warning(f"{basename} not found.")
        return result
