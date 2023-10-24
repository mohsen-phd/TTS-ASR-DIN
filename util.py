"""Utility module for the main script."""

import numpy as np
import yaml
from loguru import logger
from yaml import YAMLError

from audio_processing.noise import Noise
from vocalizer.utils import play_sound
from vocalizer.vocalizer import Vocalizer


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


def play_stimuli(sound_generator: Vocalizer, snr_db: int, stimuli: str, noise: Noise):
    """Play the stimuli to the patient.

    Args:
        sound_generator (Vocalizer): object to generate sound using a TTS.
        snr_db (int): signal to noise ratio in db.
        stimuli (str): The stimuli to play.
        noise (Noise): object to generate noise.
    """
    sound_wave = sound_generator.get_sound(stimuli)
    sound_wave = np.pad(sound_wave, (500, 500), "constant", constant_values=(0, 0))
    noise_signal = noise.generate_noise(sound_wave, snr_db)
    noisy_wave = sound_wave + noise_signal
    play_sound(wave=noisy_wave, fs=22050)
