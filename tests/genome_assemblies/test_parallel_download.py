import pytest
from unittest.mock import patch

from src.genome_assemblies.parallel_download import ParallelDownloader

def mock_download(url):
    # Simulate the behavior of the download function
    return f"Mock content for {url}"


def test_parallel_download():
    # Sample list of URLs to test with
    urls = ["http://example.com/file1.txt", "http://example.com/file2.txt", "http://example.com/file3.txt"]


    # Mock the download function
    with patch("parallel_downloader.download", side_effect=mock_download):
        # Call the function to be tested
        result = parallel_download(urls)

    # Assert the results against the expected mock content
    assert result == ["Mock content for http://example.com/file1.txt",
                      "Mock content for http://example.com/file2.txt",
                      "Mock content for http://example.com/file3.txt"]
