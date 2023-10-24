import numpy as np
import sounddevice as sd


def create_sin_wave():
    samplerate = 44100
    fs_l = 1000
    fs_r = 1200
    t = np.linspace(0.0, 10.0, samplerate * 10)
    amplitude = 0.2  # total rms -> -10db
    data_l = amplitude * np.sin(2.0 * np.pi * fs_l * t)
    data_r = amplitude * np.sin(2.0 * np.pi * fs_r * t)
    wave = np.vstack((data_l, data_r)).T
    # write("example.wav", samplerate, data.astype(np.int16))
    return wave


def create_white_noise(sec):
    mean = 0
    std = 1
    num_samples = 44100
    samples_l = np.random.normal(mean, std, size=num_samples * sec) * 0.1
    # samples_l = np.pad(samples_l, (500), "constant", constant_values=(0))
    samples_r = np.random.normal(mean, std, size=num_samples * sec) * 0.1
    # samples_r = np.pad(samples_r, (500), "constant", constant_values=(0))
    return np.vstack((samples_l, samples_r)).T


samplerate = 44100
noise = create_white_noise(10)
# noise = create_sin_wave()
sd.play(noise, samplerate)
sd.wait()
