"""Main entry point of the program."""
from loguru import logger

from asr.asr import ASR
from asr.recorder import Recorder
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

    for question in text_generator.next_item():
        wave = sound_generator.get_sound(question.question)
        play_sound(wave=wave.squeeze(0), fs=22050)
        file_src = recorder.listen()
        transcribe = asr.transcribe(file_src)
        logger.debug(transcribe)
        matched = question.check_answer(transcribe)
        print(matched)


if __name__ == "__main__":
    main()
