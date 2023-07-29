import os
import tempfile
from src.genome_assemblies.download import (
    download_assembly_summaries,
    create_download_queues,
)


def test_download_assembly_summaries():
    with tempfile.TemporaryDirectory() as temp_dir:
        for filename in download_assembly_summaries(temp_dir, timestamp=False):
            assert os.path.exists(filename) is True


def test_create_download_queues(
    mock_preprocessed_assembly_summary_file,
    snapshot,
):
    snapshot.snapshot_dir = 'tests/fixtures'
    snapshot.assert_match(
        create_download_queues(mock_preprocessed_assembly_summary_file),
        'test_assembly_summary_preprocessed_queues.txt',
    )
