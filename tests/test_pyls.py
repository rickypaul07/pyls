import os
import pytest
from pyls.pyls import read_json, list_directory, format_long_listing, human_readable_size

# Path to the test JSON file
TEST_JSON_PATH = os.path.join(os.path.dirname(__file__), 'test_structure.json')


@pytest.fixture
def sample_structure():
    return read_json(TEST_JSON_PATH)


def test_read_json():
    structure = read_json(TEST_JSON_PATH)
    assert isinstance(structure, dict)


def test_list_directory(sample_structure, capsys):
    list_directory(sample_structure['contents'], show_hidden=False, long_format=False, reverse=False,
                   sort_by_time=False, filter_option=None, human_readable=False)
    captured = capsys.readouterr()
    assert captured.out.strip() == 'LICENSE README.md ast go.mod lexer main.go parser token'


def test_format_long_listing():
    item = {
        "name": "LICENSE",
        "size": 1071,
        "time_modified": 1699941437,
        "permissions": "-rw-r--r--"
    }
    formatted_output = format_long_listing(item, human_readable=False)
    assert formatted_output.strip() == '-rw-r--r-- 1071 Nov 14 11:27 LICENSE'


def test_human_readable_size():
    assert human_readable_size(2048) == '2.0K'
    assert human_readable_size(3072) == '3.0K'
    assert human_readable_size(1572864) == '1.5M'
    assert human_readable_size(1073741824) == '1.0G'
    assert human_readable_size(1099511627776) == '1.0T'

