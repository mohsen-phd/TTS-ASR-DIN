# flake8: noqa
import pytest
from contextlib import nullcontext as does_not_raise
from util import read_conf


def test_read_conf_ok():
    conf = read_conf("tests/files/config.yaml")
    assert conf == {"Name": "test", "ID": [1, 2]}


def test_read_conf_no_file():
    with pytest.raises(FileNotFoundError):
        conf = read_conf("tests/files/config_no_file.yaml")
