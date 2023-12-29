"""Parse the digit dataset and create a json file for training."""
import glob
import json
import os
from pathlib import Path

import torchaudio
from loguru import logger

dev_clean_root = (
    "/Users/user/Documents/Projects/PhD/Wordnet-Hearing-Test/train/digit_asr/recordings"
)
wav_files = glob.glob(os.path.join(dev_clean_root, "*.wav"), recursive=True)
logger.debug("tot wav audio files {}".format(len(wav_files)))

records = {}
vocab = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}
for wav_file in wav_files:
    utt_id = Path(wav_file).stem
    records[utt_id] = {
        "file_path": wav_file,
        "words": vocab[int(utt_id.split("_")[0])],
        "spkID": utt_id.split("_")[1],
        "length": torchaudio.info(wav_file).num_frames,
    }


with open("train/digit_asr/data.json", "w") as f:
    json.dump(records, f, indent=4)
