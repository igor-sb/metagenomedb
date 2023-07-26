"""Download genome assembly summaries."""

import os
import fire
import logging
from email.message import Message
from urllib.request import urlretrieve
from datetime import datetime

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def download_kingdom_assembly_summary(
    kingdom: str,
    output_filename: str
) -> tuple[str, Message]:
    base_url = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/'
    full_url = f'{base_url}/{kingdom}/assembly_summary.txt'

    output_path = os.path.dirname(output_filename)
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    return urlretrieve(full_url, output_filename)  # noqa: S310


def download_assembly_summaries(
    output_path: str,
    kingdoms: str='archaea,bacteria',
    timestamp: bool=True,
) -> list[str]:
    filenames = []
    suffix = '_' + datetime.now().strftime('%Y-%m-%d') if timestamp else ''
    for kingdom in kingdoms.split(','):
        LOG.info(f' downloading genome assembly summary for kingdom: {kingdom}')
        output_filename = os.path.join(
            output_path,
            f'{kingdom}_assembly_summary{suffix}.txt',
        )
        file, _ = download_kingdom_assembly_summary(kingdom, output_filename)
        filenames.append(file)
    return filenames


if __name__ == '__main__':
    fire.Fire(download_assembly_summaries)
