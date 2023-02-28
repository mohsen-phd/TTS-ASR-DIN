"""Main entry point of the program."""

from sentence_generator.generator import Generator
from tts.tts import GenerateSound
from tts.utils import play_sound

if __name__ == "__main__":
    text_generator = Generator()
    for sentence in text_generator.next_item():
        g = GenerateSound(device="cpu")
        wave = g.get_sound(sentence)
        play_sound(wave=wave.squeeze(0), fs=22050)
