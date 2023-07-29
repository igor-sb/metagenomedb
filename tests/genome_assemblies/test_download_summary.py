import os
import tempfile

from metagenomedb.genome_assemblies.download_summary import (
    download_assembly_summaries,
)


def test_download_assembly_summaries():
    with tempfile.TemporaryDirectory() as temp_dir:
        downloaded_files = download_assembly_summaries(
            temp_dir,
            kingdoms='archaea',
        )
        for filename in downloaded_files:
            assert os.path.exists(filename) is True
