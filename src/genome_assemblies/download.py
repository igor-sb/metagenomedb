import os
from datetime import datetime
from email.message import Message
from urllib.request import urlretrieve


def download_kingdom_assembly_summary(
    kingdom: str,
    output_filename: str,
) -> tuple[str, Message]:
    base_url = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/'
    full_url = f'{base_url}/{kingdom}/assembly_summary.txt'
    return urlretrieve(full_url, output_filename)  # noqa: S310


def download_assembly_summaries(
    output_path: str,
    kingdoms: str = 'archaea,bacteria',
    timestamp: bool = True,
) -> list[str]:
    filenames = []
    suffix = '_' + datetime.now().strftime('%Y-%m-%d') if timestamp else ''
    for kingdom in kingdoms.split(','):
        output_filename = os.path.join(
            output_path,
            f'{kingdom}_assembly_summary{suffix}.txt',
        )
        download_kingdom_assembly_summary(kingdom, output_filename)
        filenames.append(output_filename)
    return filenames
