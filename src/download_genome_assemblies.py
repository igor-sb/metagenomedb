"""Download genome assembly summaries from NCBI FTP server."""

import logging

import fire

from src.genome_assemblies.download import download_assembly_summaries

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    LOG.info('downloading assembly summaries')
    fire.Fire(download_assembly_summaries)
