"""Utility functions for audio processing."""
import numpy as np


def calculate_snr_db(signal: np.ndarray, noise: np.ndarray) -> float:
    """Calculate the SNR in dB of a signal relative to a noise.

    Args:
        signal (np.ndarray): numpy array containing the signal.
        noise (np.ndarray): numpy array containing the noise.

    Returns:
        float: float containing the SNR in dB of the signal relative to the noise.
    """
    # Calculate the power of the signal
    signal_power = np.sum(signal**2) / len(signal)

    # Calculate the power of the noise
    noise_power = np.sum(noise**2) / len(noise)

    # Calculate the SNR in dB
    snr_db = 10 * np.log10(signal_power / noise_power)

    return snr_db
