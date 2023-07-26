import os
import tempfile
from src.genome_assemblies.download import download_assembly_summaries

def test_download_assembly_summaries():
    with tempfile.TemporaryDirectory() as temp_dir:
        for filename in download_assembly_summaries(temp_dir, timestamp=False):
            assert os.path.exists(filename) is True


