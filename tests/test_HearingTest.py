# flake8: noqa
import pytest

from hearing_test.test_logic import DigitInNoise


class Test_DigitInNoise:
    def setup(self):
        self.obj = DigitInNoise(1, 2, [1, 2], 3)

    def test_srt(self):
        self.obj._important_snr = [1, 2]
        assert self.obj.srt == 1.5
