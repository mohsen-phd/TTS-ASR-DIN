"""Main entry point of the program."""

from tts.tts import GenerateSound
from tts.utils import play_sound

if __name__ == "__main__":
    g = GenerateSound(device="cpu")
    wave = g.get_sound(
        "Could you provide me with the names of the three capital cities?"
    )
    play_sound(wave=wave.squeeze(0), fs=22050)
