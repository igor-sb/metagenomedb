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


def create_kingdom_output_filename(
    kingdom: str,
    output_path: str,
    timestamp: bool,
) -> str:
    if timestamp:
        suffix = '_{current_date}'.format(
            current_date=datetime.now().strftime('%Y-%m-%d'),
        )
    else:
        suffix = ''
    output_base_filename = '{kingdom}_assembly_summary{suffix}.txt'.format(
        kingdom=kingdom,
        suffix=suffix,
    )
    return os.path.join(output_path, output_base_filename)


def download_assembly_summaries(
    output_path: str,
    kingdoms: tuple = ('archaea', 'bacteria'),
    timestamp: bool = True,
) -> list[str]:
    filenames = []
    for kingdom in kingdoms:
        output_filename_with_path = create_kingdom_output_filename(
            output_path,
            kingdom,
            timestamp,
        )
        download_kingdom_assembly_summary(kingdom, output_filename_with_path)
        filenames.append(output_filename_with_path)
    return filenames
