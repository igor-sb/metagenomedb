import pytest
import os
import pandas as pd

from src.genome_assemblies.preprocess import load_raw_assembly_summary_table

fixture_path = '{base_path}/tests/fixtures'.format(
    base_path=os.path.abspath('.'),
)


@pytest.fixture(name='mock_assembly_summary_file')
def fixture_mock_assembly_summary_file():
    return '{fixture_path}/test_assembly_summary.txt'.format(
        fixture_path=fixture_path,
    )


def test_load_raw_assembly_summary_table(mock_assembly_summary_file):
    df = load_raw_assembly_summary_table(mock_assembly_summary_file)
    assert isinstance(df, pd.DataFrame)
