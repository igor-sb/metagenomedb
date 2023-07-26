import os
import pandas as pd
import pytest

from src.genome_assemblies.preprocess import (
    load_raw_assembly_summary_table,
)

fixture_path = '{base_path}/tests/fixtures'.format(
    base_path=os.path.abspath('.'),
)

@pytest.fixture()
def testing_assembly_summary_filename():
    return '{fixture_path}/test_assembly_summary.txt'.format(
        fixture_path=fixture_path,
    )


def reference_preprocessed_assembly_summary():
    return pd.read_csv(
        '{fixture_path}/test_assemby_summary_preprocessed.txt',
    )


def test_load_raw_assembly_summary_table(testing_assembly_summary_filename):
    return load_raw_assembly_summary_table(testing_assembly_summary_filename)


def test_write_filtered_assembly_summary_table():
    pass


def test_remove_infraspecific_name_metadata():
    pass
