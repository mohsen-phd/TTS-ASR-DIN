"""Hold common functions used in TTS."""

import numpy as np
import sounddevice as sd


def play_sound(wave: np.ndarray, fs: int = 44100) -> None:
    """Get an array as input and convert it to  sound.

    Args:
        wave (np.ndarray): 1D input array representing a sound.
        fs (int): sample per second. Defaults to 44100.
    """
    sd.play(wave, fs)
    sd.wait()
