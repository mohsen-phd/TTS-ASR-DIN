"""Train a Speechbrain asr."""
import speechbrain as sb
from speechbrain.dataio.dataset import DynamicItemDataset
from speechbrain.dataio.encoder import CategoricalEncoder
import torch


@sb.utils.data_pipeline.takes("file_path")
@sb.utils.data_pipeline.provides("signal")
def audio_pipeline(file_path):
    sig = sb.dataio.dataio.read_audio(file_path)
    return sig


@sb.utils.data_pipeline.takes("spkID")
@sb.utils.data_pipeline.provides("spkid_encoded")
def spk_id_encoding(spkid):
    return torch.LongTensor([spk_id_encoder.encode_label(spkid)])


@sb.utils.data_pipeline.takes("words")
@sb.utils.data_pipeline.provides("words_encoded")
def word_encoding(words):
    return torch.LongTensor([word_encoder.encode_label(words)])


dataset = DynamicItemDataset.from_json("train/digit_asr/data.json")
spk_id_encoder = CategoricalEncoder()
spk_id_encoder.update_from_didataset(dataset, "spkID")

word_encoder = CategoricalEncoder()
word_encoder.update_from_didataset(dataset, "words")

sb.dataio.dataset.add_dynamic_item([dataset], spk_id_encoding)
sb.dataio.dataset.add_dynamic_item([dataset], audio_pipeline)
sb.dataio.dataset.add_dynamic_item([dataset], word_encoding)


dataset.set_output_keys(
    ["words", "words_encoded", "signal"],
)

sorted_data = dataset.filtered_sorted(sort_key="length")
