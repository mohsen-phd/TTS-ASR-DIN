"""Main entry point of the program."""
from loguru import logger

from asr.asr import ASR
from asr.recorder import Recorder
from audio_processing.noise import Noise
from hearing_test.test_logic import DigitInNoise
from sentence_generator.generator import QuestionGenerator
from sentence_generator.questions import Questions
from tts.tts import GenerateSound
from tts.utils import play_sound


def initialize() -> (
    tuple[DigitInNoise, QuestionGenerator, ASR, Recorder, GenerateSound]
):
    """Initialize the hearing test and other modules.

    Returns:
        tuple: Return the hearing test, question generator, asr, recorder and sound
    """
    hearing_test = DigitInNoise(
        correct_threshold=2, incorrect__threshold=1, step_size=[5, 3, 1]
    )

    question_generator = QuestionGenerator()

    asr = ASR()

    recorder = Recorder(
        store=True,
        chunk=1024,
        rms_threshold=10,
        timeout_length=3,
        save_dir=r"records",
    )

    sound_generator = GenerateSound(device="cpu")

    return hearing_test, question_generator, asr, recorder, sound_generator


def play_stimuli(sound_generator: GenerateSound, snr_db: int, question: Questions):
    """Play the stimuli to the patient.

    Args:
        sound_generator (GenerateSound): object to generate sound using a TTS.
        snr_db (int): signal to noise ratio in db.
        question (Questions): The stimuli to play.
    """
    sound_wave = sound_generator.get_sound(question.question).squeeze(0)
    noise = Noise.generate_noise(sound_wave, snr_db)
    noisy_wave = sound_wave + noise
    play_sound(wave=noisy_wave, fs=22050)


def listen(asr: ASR, recorder: Recorder) -> str:
    """Listent to patient response, and transcribe it.

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


def main():
    """Code entry point."""
    hearing_test, question_generator, asr, recorder, sound_generator = initialize()

    snr_db = 5
    correct_count = incorrect_count = 0
    for idx, question in enumerate(question_generator.next_item()):
        play_stimuli(sound_generator, snr_db, question)

        transcribe = listen(asr, recorder)

        matched = question.check_answer(transcribe)
        logger.debug(f"Matched: {matched}")

        snr_db = hearing_test.get_next_snr(correct_count, incorrect_count, idx)


if __name__ == "__main__":
    main()
