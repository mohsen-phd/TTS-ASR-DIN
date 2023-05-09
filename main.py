"""Main entry point of the program."""
from loguru import logger

from asr.asr import ASR
from asr.recorder import Recorder
from audio_processing.noise import Noise
from hearing_test.test_logic import DigitInNoise
from sentence_generator.generator import QuestionGenerator
from tts.tts import GenerateSound
from tts.utils import play_sound


def main():
    """Code entry point."""
    hearing_test = DigitInNoise(2, 1, [5, 3, 1])
    question_generator = QuestionGenerator()
    asr = ASR()
    recorder = Recorder(
        store=False,
        chunk=1024,
        rms_threshold=10,
        timeout_length=3,
        save_dir=r"records",
    )
    sound_generator = GenerateSound(device="cpu")

    snr_db = 5
    correct_count = incorrect_count = 0
    for idx, question in enumerate(question_generator.next_item()):
        sound_wave = sound_generator.get_sound(question.question).squeeze(0)
        noise = Noise.generate_noise(sound_wave, snr_db)
        noisy_wave = sound_wave + noise
        play_sound(wave=noisy_wave, fs=22050)
        file_src = recorder.listen()
        transcribe = asr.transcribe(file_src)
        logger.debug(transcribe)
        matched = question.check_answer(transcribe)
        logger.debug(f"Matched: {matched}")
        snr_db = hearing_test.get_next_snr(correct_count, incorrect_count, idx)


if __name__ == "__main__":
    main()
