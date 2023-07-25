"""Download genome assembly summaries."""

import os
import fire
import logging
import urllib.request
from datetime import datetime

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def download_kingdom_assembly_summary(kingdom, output_filename):
    base_url = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/'
    full_url = f'{base_url}/{kingdom}/assembly_summary.txt'

    output_path = os.path.dirname(output_filename)
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    urllib.request.urlretrieve(full_url, output_filename)  # noqa: S310


def download_assembly_summaries(
    output_path,
    kingdoms='archaea,bacteria',
    timestamp=True,
):
    suffix = '_' + datetime.now().strftime('%Y-%m-%d') if timestamp else ''
    for kingdom in kingdoms.split(','):
        LOG.info(' downloading genome assembly summary for kingdom: {kingdom}')
        output_filename = os.path.join(
            output_path,
            f'{kingdom}_assembly_summary{suffix}.txt',
        )
        download_kingdom_assembly_summary(kingdom, output_filename)


if __name__ == '__main__':
    fire.Fire(download_assembly_summaries)
