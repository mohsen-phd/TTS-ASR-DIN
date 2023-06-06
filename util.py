"""Utility module for the main script."""
import yaml
from loguru import logger

from asr.asr import ASR, ARLibrispeech
from asr.recorder import Recorder
from audio_processing.noise import Noise, WhiteNoise
from hearing_test.test_logic import DigitInNoise, HearingTest
from stimuli_generator.questions import DigitQuestions, Questions
from tts.tts import TTS, GenerateSound
from tts.utils import play_sound


def read_conf() -> dict:
    """Read the configuration file.

    Returns:
        dict: Return the configuration file as a dictionary.
    """
    with open("config.yaml", "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            logger.error(f"Error while reading the configuration file: {exc}")
    return {}


def initialize() -> tuple[HearingTest, Questions, ASR, Recorder, TTS, Noise]:
    """Initialize the hearing test and other modules.

    Returns:
        tuple: Return the hearing test, question generator, asr,
                recorder, sound and noise generator.
    """
    conf = read_conf()
    hearing_test = DigitInNoise(
        correct_threshold=conf["test"]["correct_threshold"],
        incorrect_threshold=conf["test"]["incorrect_threshold"],
        step_size=conf["test"]["step_size"],
        reversal_limit=conf["test"]["reversal_limit"],
    )

    stimuli_generator = DigitQuestions()

    asr = ARLibrispeech()

    recorder = Recorder(
        store=True,
        chunk=1024,
        rms_threshold=10,
        timeout_length=3,
        save_dir=r"records",
    )

    noise = WhiteNoise()

    sound_generator = GenerateSound(device="cpu")

    return hearing_test, stimuli_generator, asr, recorder, sound_generator, noise


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


def listen(asr: ASR, recorder: Recorder) -> str:
    """Listen to patient response, and transcribe it.

    Args:
        asr (ASR): asr object to transcribe the audio.
        recorder (Recorder): object to listen to the patient, and store the audio.

    Returns:
        str: transcribed text.
    """
    file_src = recorder.listen()
    transcribe = asr.transcribe(file_src)
    logger.debug(transcribe)
    return transcribe
