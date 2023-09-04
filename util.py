"""Utility module for the main script."""
import yaml
from loguru import logger
from yaml import YAMLError

from audio_processing.noise import Noise, WhiteNoise
from get_response.asr import ASR, ARLibrispeech
from get_response.base import CaptureResponse
from get_response.cli import CLI
from get_response.recorder import Recorder
from hearing_test.test_logic import DigitInNoise
from stimuli_generator.questions import DigitQuestions
from tts.tts import TTS, GenerateSound
from tts.utils import play_sound


def read_conf(src: str = "config.yaml") -> dict:
    """Read the configuration file.

    Args:
        src (str): Path to the configuration file. Defaults to "config.yaml".

    Returns:
        dict: Return the configuration file as a dictionary.

    Raises:
        YAMLError: If an error occurs while reading or parsing the configuration file.
    """
    with open(src, "r") as f:
        try:
            return yaml.safe_load(f)
        except YAMLError as exc:
            logger.error(f"Error while reading the configuration file: {exc}")
            raise exc


class TestManager:
    """A class to create the hearing test based on config file."""

    def __init__(self, config_file: str) -> None:
        """Initialize the hearing test and other modules.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.conf = read_conf(config_file)
        self.hearing_test = DigitInNoise(
            correct_threshold=self.conf["test"]["correct_threshold"],
            incorrect_threshold=self.conf["test"]["incorrect_threshold"],
            step_size=self.conf["test"]["step_size"],
            reversal_limit=self.conf["test"]["reversal_limit"],
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

        self.noise = WhiteNoise()

        self.sound_generator = GenerateSound(device="cpu")

        self.start_snr = self.conf["test"]["start_snr"]

    def _capture_method(self) -> CaptureResponse:
        if self.conf["response_capturing"] == "cli":
            return CLI()
        if self.conf["response_capturing"] == "asr":
            return self.get_asr()
        raise NotImplementedError

    def get_asr(self) -> ASR:
        """Get the proper asr engine based on config file.

        Raises:
            NotImplementedError: If the asr type is not implemented.

        Returns:
            ASR: The asr engine.
        """
        if self.conf["asr"]["type"] == "ARLibrispeech":
            return ARLibrispeech()
        raise NotImplementedError

    def get_response(self) -> str:
        """Get the response from the participant.

        Raises:
            NotImplementedError: The response capturing method is not implemented.

        Returns:
            str: Response from the participant.
        """
        if self.conf["response_capturing"] == "cli":
            return self.response_capturer.get()

        if self.conf["response_capturing"] == "asr":
            file_src = self.recorder.listen()
            transcribe = self.response_capturer.get(src=file_src)
            logger.debug(transcribe)
            return transcribe

        raise NotImplementedError


def play_stimuli(sound_generator: TTS, snr_db: int, stimuli: str, noise: Noise):
    """Play the stimuli to the patient.

    Args:
        sound_generator (TTS): object to generate sound using a TTS.
        snr_db (int): signal to noise ratio in db.
        stimuli (str): The stimuli to play.
        noise (Noise): object to generate noise.
    """
    sound_wave = sound_generator.get_sound(stimuli).squeeze(0)
    noise_signal = noise.generate_noise(sound_wave, snr_db)
    noisy_wave = sound_wave + noise_signal
    play_sound(wave=noisy_wave, fs=22050)
