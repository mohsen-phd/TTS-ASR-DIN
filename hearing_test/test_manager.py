"""A module to manage and organize the test procedure."""
from abc import ABC, abstractmethod
from pathlib import Path

from loguru import logger

from audio_processing.noise import Babble, WhiteNoise
from get_response.asr import ASR, ARLibrispeech, SimpleASR
from get_response.base import CaptureResponse
from get_response.cli import CLI
from get_response.recorder import Recorder
from hearing_test.test_logic import DigitInNoise
from stimuli_generator.questions import DigitQuestions
from vocalizer.vocalizer import TTS, Recorded, Vocalizer


class TestManager(ABC):
    """A class to create the hearing test based on config file."""

    def __init__(self, configs: dict) -> None:
        """Initialize the hearing test and other modules.

        Args:
            configs (dict): Path to the configuration file.
        """
        self.conf = configs
        self.hearing_test = DigitInNoise(
            correct_threshold=self.conf["test"]["correct_threshold"],
            incorrect_threshold=self.conf["test"]["incorrect_threshold"],
            step_size=self.conf["test"]["step_size"],
            reversal_limit=self.conf["test"]["reversal_limit"],
            minimum_threshold=self.conf["test"]["minimum_threshold"],
        )

        self.stimuli_generator = DigitQuestions()

        self.response_capturer = self._capture_method()

        self.recorder = Recorder(
            store=True,
            chunk=1024,
            rms_threshold=10,
            timeout_length=3,
            save_dir=r"records",
        )

        self.noise = self._get_noise()

        self.sound_generator = self._get_sound_generator()

        self.start_snr = self.conf["test"]["start_snr"]

    def _get_sound_generator(self) -> Vocalizer:
        if self.conf["stimuli_vocalizer"]["name"] == "recorded":
            return Recorded(Path(self.conf["stimuli_vocalizer"]["src"]))
        elif self.conf["stimuli_vocalizer"]["name"] == "tts":
            return TTS(device="cpu")
        else:
            raise NotImplementedError

    def _get_noise(self):
        """Get the proper noise generator based on config file.

        Raises:
            NotImplementedError: If the noise type is not implemented.

        Returns:
            Noise: The noise generator.
        """
        if self.conf["test"]["noise"]["type"] == "white":
            return WhiteNoise()
        elif self.conf["test"]["noise"]["type"] == "babble":
            return Babble(noise_src=self.conf["test"]["noise"]["src"])
        raise NotImplementedError

    @abstractmethod
    def get_response(self) -> list[str]:
        """Get the response from the participant.

        Returns:
            list[str]: List of words in the participant's response.
        """
        ...

    @abstractmethod
    def _capture_method(self) -> CaptureResponse:
        """Select the way the participant will give it's response.

        Returns:
            CaptureResponse: Object responsible for capturing response.
        """
        ...


class CliTestManager(TestManager):
    """Test manager for command line test."""

    def __init__(self, configs: dict) -> None:
        """Initialize the command line test manager.

        Args:
            configs (dict): Loaded configuration.
        """
        super().__init__(configs)
        self.digit_convertor = {
            "0": "zero",
            "1": "one",
            "2": "two",
            "3": "three",
            "4": "four",
            "5": "five",
            "6": "six",
            "7": "seven",
            "8": "eight",
            "9": "nine",
        }

    def _capture_method(self) -> CaptureResponse:
        """Return the object that get response from terminal.

        Returns:
            CaptureResponse: Object responsible for capturing response.
        """
        return CLI()

    def get_response(self) -> list[str]:
        """Get the response from the participant.

        Returns:
            list[str]: List of words in the participant's response.
        """
        listed_response = [
            self.digit_convertor[i]
            for i in self.response_capturer.get()
            if i in self.digit_convertor
        ]
        return listed_response


class ASRTestManager(TestManager):
    """Test manager for ASR test."""

    def _capture_method(self) -> CaptureResponse:
        return self.get_asr()

    def get_asr(self) -> ASR:
        """Get the proper asr engine based on config file.

        Raises:
            NotImplementedError: If the asr type is not implemented.

        Returns:
            ASR: The asr engine.
        """
        if self.conf["ml"]["asr_type"] == "ARLibrispeech":
            return ARLibrispeech()
        elif self.conf["ml"]["asr_type"] == "SimpleASR":
            return SimpleASR()
        raise NotImplementedError

    def get_response(self) -> list[str]:
        """Get the response from the participant.

        Returns:
            list[str]: List of words in the participant's response.
        """
        file_src = self.recorder.listen()
        transcribe = self.response_capturer.get(src=file_src)
        logger.debug(transcribe)
        return transcribe.split(" ")
