"""Utility module for the main script."""

import yaml
from loguru import logger
from yaml import YAMLError

from audio_processing.noise import Noise
from tts.tts import TTS
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
