"""Functions for downloading assembly."""

import os
from datetime import datetime
from email.message import Message
from urllib.request import urlretrieve

from src.genome_assemblies.io import load_preprocessed_assembly_summary_table


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
    kingdoms: str = 'archaea,bacteria',
    timestamp: bool = True,
) -> list[str]:
    filenames = []
    for kingdom in kingdoms.split(','):
        output_filename_with_path = create_kingdom_output_filename(
            output_path,
            kingdom,
            timestamp,
        )
        download_kingdom_assembly_summary(kingdom, output_filename_with_path)
        filenames.append(output_filename_with_path)
    return filenames


def construct_download_path_from_url(url: str, out_path: str) -> str:
    return os.path.join(out_path, os.path.basename(url))


def create_download_queues(
    assembly_summary_filename: str,
    features_path: str = 'data/features/',
    sequence_path: str = 'data/sequence/',
) -> dict[str, list]:
    df = load_preprocessed_assembly_summary_table(assembly_summary_filename)
    features_queue = [
        (url, construct_download_path_from_url(url, features_path))
        for url in df.url_features
    ]
    sequence_queue = [
        (url, construct_download_path_from_url(url, sequence_path))
        for url in df.url_sequence
    ]
    return {'features': features_queue, 'sequence': sequence_queue}
