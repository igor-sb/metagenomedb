import os
import pytest

fixture_path = '{base_path}/tests/fixtures'.format(
    base_path=os.path.abspath('.'),
)


@pytest.fixture()
def mock_assembly_summary_file():
    return '{fixture_path}/test_assembly_summary.txt'.format(
        fixture_path=fixture_path,
    )


@pytest.fixture()
def mock_preprocessed_assembly_summary_file():
    return '{fixture_path}/test_assembly_summary_preprocessed.txt'.format(
        fixture_path=fixture_path,
    )
