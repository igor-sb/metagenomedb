"""Functions for downloading assembly."""

import os
from datetime import datetime
from email.message import Message
from urllib.request import urlretrieve


def create_assembly_summary_url(kingdom: str) -> str:
    return '{base_url}/{kingdom}/assembly_summary.txt'.format(
        base_url='ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/',
        kingdom=kingdom,
    )


def download_kingdom_assembly_summary(
    kingdom: str,
    output_filename: str,
) -> tuple[str, Message]:
    url = create_assembly_summary_url(kingdom)
    return urlretrieve(url, output_filename)  # noqa: S310


def create_output_filename(output_path: str, timestamp: bool = True) -> str:
    pass


def download_assembly_summaries(
    output_path: str,
    kingdoms: str = 'archaea,bacteria',
    timestamp: bool = True,
) -> list[str]:
    filenames = []
    if timestamp:
        suffix = '_{current_date}'.format(
            current_date=datetime.now().strftime('%Y-%m-%d'),
        )
    else:
        suffix = ''
    for kingdom in kingdoms.split(','):
        output_filename = '{kingdom}_assembly_summary{suffix}.txt'.format(
            kingdom=kingdom,
            suffix=suffix,
        )
        output_filename_with_path = os.path.join(output_path, output_filename)
        download_kingdom_assembly_summary(kingdom, output_filename_with_path)
        filenames.append(output_filename_with_path)
    return filenames
