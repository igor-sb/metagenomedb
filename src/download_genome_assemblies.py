"""Download genome assembly summaries from NCBI FTP."""

import logging
import fire

from src.genome_assemblies.download import download_assembly_summaries

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    fire.Fire(download_assembly_summaries)
