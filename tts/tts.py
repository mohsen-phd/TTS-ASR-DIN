"""Convert text to speech."""
import numpy as np
from speechbrain.pretrained import HIFIGAN, Tacotron2


class GenerateSound:
    """Class for generating waveform from string."""

    def __init__(self, device: str = "cpu") -> None:
        """Initialize the class and load  tacotron2 and hifi_gan.

        Args:
            device (str): device to run the operations on
                (cpu,cuda,mps). Defaults to "cpu".
        """
        self.tacotron2 = Tacotron2.from_hparams(
            source="speechbrain/tts-tacotron2-ljspeech",
            savedir="models/tmpdir_tts",
            run_opts={"device": device},
        )
        self.hifi_gan = HIFIGAN.from_hparams(
            source="speechbrain/tts-hifigan-ljspeech",
            savedir="models/tmpdir_vocoder",
            run_opts={"device": device},
        )

    def get_sound(self, text: str) -> np.ndarray:
        """Get an input text and generate the corresponding wave form.

        Args:
            text (str): input string

        Returns:
            np.ndarray: waveform in shape of (1,length_of_wave)
        """
        mel_output, mel_length, alignment = self.tacotron2.encode_text(text)

        # Running Vocoder (spectrogram-to-waveform)
        waveforms = self.hifi_gan.decode_batch(mel_output)
        return waveforms.to("cpu").squeeze(1).numpy()
