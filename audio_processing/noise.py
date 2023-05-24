"""Class to generate and process the noise signal."""

import numpy as np

from audio_processing.util import rms_power


class Noise:
    """A class for generating random gaussian noise with specific db."""

    @staticmethod
    def generate_noise(signal: np.ndarray, desired_snr_db: float) -> np.ndarray:
        """Generate a random gaussian noise signal with a specific SNR.

        Args:
            signal (np.ndarray): numpy array containing the signal.
            desired_snr_db (float): desired SNR of the noise relative
                                            to the signal in dB.

        Returns:
            np.ndarray: numpy array containing the noise signal.
        """
        signal_power = rms_power(signal=signal)

        # Calculate the power of the noise required to achieve the desired SNR in dB
        desired_snr = np.sqrt(10 ** (desired_snr_db / 20))
        noise_power = signal_power / desired_snr

        # Generate the noise signal with the calculated power
        noise = np.random.normal(scale=noise_power, size=len(signal))

        return noise
