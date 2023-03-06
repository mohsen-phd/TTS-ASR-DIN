"""Main entry point of the program."""
from loguru import logger

from asr.asr import ASR
from asr.recorder import Recorder
from sentence_generator.generator import Generator
from tts.tts import GenerateSound
from tts.utils import play_sound

if __name__ == "__main__":
    text_generator = Generator()
    ASR = ASR()
    recorder = Recorder(
        store=True,
        chunk=1024,
        rms_threshold=10,
        timeout_length=3,
        save_dir=r"records",
    )
    for sentence in text_generator.next_item():
        g = GenerateSound(device="cpu")
        wave = g.get_sound(sentence)
        play_sound(wave=wave.squeeze(0), fs=22050)
        file_src = recorder.listen()
        transcribe = ASR.transcribe(file_src)
        logger.debug(transcribe)
