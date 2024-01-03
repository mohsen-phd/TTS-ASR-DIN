"""A module to manage and organize the test procedure."""
import os
from abc import ABC, abstractmethod
from pathlib import Path

from colorama import Fore
from loguru import logger
from pydub import AudioSegment

from audio_processing.noise import Babble, WhiteNoise
from get_response.asr import ASR, SimpleASR, SpeechBrainASR
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
            save_dir=configs["test"]["record_save_dir"],
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
        print(Fore.GREEN + "Enter the number you heard")
        logger.debug("Enter the number you heard")

        listed_response = [
            self.digit_convertor[i]
            for i in self.response_capturer.get()
            if i in self.digit_convertor
        ]
        logger.debug(listed_response)
        return listed_response


class ASRTestManager(TestManager):
    """Test manager for ASR test."""

    def __init__(self, configs: dict) -> None:
        """Initialize the ASR test manager.

        Args:
            configs (dict): Loaded configuration.
        """
        super().__init__(configs)
        self._prepend = AudioSegment.from_wav(configs["test"]["Prepend_wav_file"])
        self._prepend_len = configs["test"]["prepend_str_len"]

    def _capture_method(self) -> CaptureResponse:
        return self.get_asr()

    def get_asr(self) -> ASR:
        """Get the proper asr engine based on config file.

        Raises:
            NotImplementedError: If the asr type is not implemented.

        Returns:
            ASR: The asr engine.
        """
        if self.conf["ml"]["asr_type"] == "SpeechBrain":
            return SpeechBrainASR(
                source=self.conf["ml"]["asr_source"],
                save_dir=self.conf["ml"]["asr_save_dir"],
            )
        elif self.conf["ml"]["asr_type"] == "SimpleASR":
            return SimpleASR()
        raise NotImplementedError

    def _post_process(self, responses: list[str]) -> list[str]:
        """Post process the transcribe and remove common mistakes.

        Args:
            responses (list[str]): List of words in the participant's response.

        Returns:
            list[str]: List of words in the participant's response after changing the common mistakes.
        """
        common_mistakes = {
            "ate": "eight",
            "for": "four",
            "too": "two",
            "through": "three",
            "to": "two",
            "tree": "three",
            "sixth": "six",
            "seventy": "seven",
            "fifth": "five",
            "fourth": "four",
            "fly": "five",
        }
        clean_response = [
            common_mistakes[x] if x in common_mistakes else x for x in responses
        ]
        return clean_response

    def get_response(self) -> list[str]:
        """Get the response from the participant.

        Returns:
            list[str]: List of words in the participant's response.
        """
        logger.debug("Repeat the number you heard")

        print(Fore.GREEN + "Repeat the number you heard")

        file_src = self.recorder.listen()

        transcribe = self.response_capturer.get(src=file_src).lower()
        logger.debug(transcribe)
        results = self._post_process(transcribe.split(" "))
        logger.debug(results)
        try:
            os.remove(file_src.split("/")[-1])
        except FileNotFoundError:
            logger.debug("file not found")
        return results
