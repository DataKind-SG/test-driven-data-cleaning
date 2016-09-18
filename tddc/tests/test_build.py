import os
import subprocess
import pytest

from tddc import build


@pytest.fixture()
def build_class(fixtures_dir, input_filename, tmpdir):
    return build.Scripts(
        summaries_root_dir=fixtures_dir,
        input_file=input_filename,
        scripts_root_dir=tmpdir.strpath,
        output_dir='')


def is_same_file(file_a, file_b):
    diff_return = subprocess.call(['diff', file_a, file_b])
    return diff_return == 0


def test_write_cleaning_script(build_class, fixtures_dir):
    cleaning_file = build_class.write_cleaning_script()
    cleaning_base = os.path.splitext(os.path.basename(cleaning_file))[0]
    fixture_clean = os.path.join(fixtures_dir, cleaning_base)
    assert is_same_file(cleaning_file, fixture_clean)


def test_write_test_cleaning_script(build_class, fixtures_dir):
    test_cleaning_file = build_class.write_test_cleaning_script()
    test_cleaning_base = os.path.splitext(
        os.path.basename(test_cleaning_file))[0]
    fixture_test_clean = os.path.join(
        fixtures_dir, test_cleaning_base)
    assert is_same_file(test_cleaning_file, fixture_test_clean)
