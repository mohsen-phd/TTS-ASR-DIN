"""Main entry point of the program."""
from loguru import logger

from asr.asr import ASR
from asr.recorder import Recorder
from audio_processing.noise import Noise
from sentence_generator.generator import Generator
from tts.tts import GenerateSound
from tts.utils import play_sound


def main():
    """Code entry point."""
    text_generator = Generator()
    asr = ASR()
    recorder = Recorder(
        store=True,
        chunk=1024,
        rms_threshold=10,
        timeout_length=3,
        save_dir=r"records",
    )
    sound_generator = GenerateSound(device="cpu")
    snr_db = 5
    for question in text_generator.next_item():
        sound_wave = sound_generator.get_sound(question.question).squeeze(0)
        noise = Noise.generate_noise(sound_wave, snr_db)
        noisy_wave = sound_wave + noise
        play_sound(wave=noisy_wave, fs=22050)
        file_src = recorder.listen()
        transcribe = asr.transcribe(file_src)
        logger.debug(transcribe)
        matched = question.check_answer(transcribe)
        logger.debug(f"Matched: {matched}")


if __name__ == "__main__":
    main()
