"""Class to generate and process the noise signal."""

from abc import ABC, abstractmethod

import numpy as np

from audio_processing.util import rms_amplitude


class Noise(ABC):
    """Abstract class for noise generation."""

    @abstractmethod
    def generate_noise(self, signal: np.ndarray, desired_snr_db: float) -> np.ndarray:
        """Interface for generating noise.

        Args:
            signal (np.ndarray): numpy array containing the signal.
            desired_snr_db (float): desired SNR of the noise relative
                                            to the signal in dB.

        Returns:
            np.ndarray: numpy array containing the noise signal.
        """
        ...


class WhiteNoise(Noise):
    """A class for generating random gaussian noise with specific db."""

    def generate_noise(self, signal: np.ndarray, desired_snr_db: float) -> np.ndarray:
        """Generate a random gaussian noise signal with a specific SNR.

        Args:
            signal (np.ndarray): numpy array containing the signal.
            desired_snr_db (float): desired SNR of the noise relative
                                            to the signal in dB.

        Returns:
            np.ndarray: numpy array containing the noise signal.
        """
        signal_amplitude = rms_amplitude(signal=signal)

        # Calculate the amplitude of the noise required to achieve the desired SNR in dB
        desired_snr = np.sqrt(10 ** (desired_snr_db / 20))
        noise_amplitude = signal_amplitude / desired_snr

        # Generate the noise signal with the calculated amplitude
        noise = np.random.normal(scale=noise_amplitude, size=len(signal))

        return noise
