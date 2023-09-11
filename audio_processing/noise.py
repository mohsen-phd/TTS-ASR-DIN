"""Class to generate and process the noise signal."""

from abc import ABC, abstractmethod

import numpy as np
from scipy.io import wavfile

from audio_processing.util import convert_to_specific_rms, rms_amplitude


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

    def _get_noise_amplitutre(self, signal: np.ndarray, desired_snr_db: float) -> float:
        """Measure the required amplitude of the noise to achieve the desired SNR.

        Get a signal and an SNR in dB and calculate the amplitude of the noise required
          to achieve the desired SNR.

        Args:
            signal (np.ndarray): numpy array containing the signal.
            desired_snr_db (float): desired SNR of the noise relative

        Returns:
            float: float containing the amplitude of the noise required to achieve
            the desired SNR in dB.
        """
        signal_amplitude = rms_amplitude(signal=signal)
        desired_snr = np.sqrt(10 ** (desired_snr_db / 20))
        noise_amplitude = signal_amplitude / desired_snr
        return noise_amplitude


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
        noise_amplitude = self._get_noise_amplitutre(signal, desired_snr_db)
        noise = np.random.normal(scale=noise_amplitude, size=len(signal))

        return noise


class Babble(Noise):
    """A class for generating babble noise from w wave file."""

    def __init__(self, noise_src: str) -> None:
        """Initialize the class and load the noise file.

        Args:
            noise_src (str): path of the wave file containing the noise.
        """
        self._sample_rate, self._noise = wavfile.read(noise_src)

    def generate_noise(self, signal: np.ndarray, desired_snr_db: float) -> np.ndarray:
        """Generate a babble noise signal.

        Return a babble noise from the loaded file and scale it to the desired SNR.
        a return a noise signal with the same length as the input signal.

        Args:
            signal (np.ndarray): numpy array containing the signal.
            desired_snr_db (float): desired SNR of the noise relative
                                            to the signal in dB.

        Returns:
            np.ndarray: numpy array containing the noise signal.
        """
        noise_amplitude = self._get_noise_amplitutre(signal, desired_snr_db)

        scaled_noise = convert_to_specific_rms(self._noise, noise_amplitude)

        return scaled_noise[: len(signal)]
