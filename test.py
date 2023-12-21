from get_response.asr import SimpleASR
import numpy as np

s = SimpleASR()
w = s.get(
    "/Users/user/Documents/Projects/PhD/Wordnet-Hearing-Test/train/digit_asr/data/my_test/44khz/my_voice_test_5-6-10.wav"
)
print(w)
