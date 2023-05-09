"""Class to generate and process the noise signal."""

import numpy as np


class Noise:
    """A class for generating random gussian noise with specific db."""

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
        signal_power = np.sum(signal**2) / len(signal)

        # Calculate the power of the noise required to achieve the desired SNR in dB
        desired_snr = 10 ** (desired_snr_db / 10)
        noise_power = signal_power / desired_snr

        # Generate the noise signal with the calculated power
        noise = np.random.normal(scale=np.sqrt(noise_power), size=len(signal))

        return noise
