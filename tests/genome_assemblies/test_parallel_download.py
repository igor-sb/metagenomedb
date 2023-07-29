import os
import pytest
import tempfile

from src.genome_assemblies.parallel_download import ParallelDownloader


@pytest.fixture(name='parallel_download_test_urls')
def fixture_parallel_download_test_urls():
    return (
        'ftp://ftp.ncbi.nlm.nih.gov/robots.txt',
        'ftp://ftp.ncbi.nlm.nih.gov/favicon.ico',
        'ftp://ftp.ncbi.nlm.nih.gov/fufuter.html',
        'ftp://ftp.ncbi.nlm.nih.gov/README.ftp',
    )


def test_parallel_download(parallel_download_test_urls):
    with tempfile.TemporaryDirectory() as tmp_dir:
        queue = [
            (url, os.path.join(tmp_dir, os.path.basename(url)))
            for url in parallel_download_test_urls
        ]
        parallel_dl = ParallelDownloader(queue, n_parallel=2)
        parallel_dl.run()
        assert parallel_dl.n_processed_urls == parallel_dl.n_total_urls
