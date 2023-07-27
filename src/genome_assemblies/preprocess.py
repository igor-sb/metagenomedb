import os
import re

import pandas as pd

from src.genome_assemblies.io import assembly_summary_config


def select_best_strain_assemblies(assemblies_df: pd.DataFrame) -> pd.DataFrame:
    assemblies_df = (
        assemblies_df
        .pipe(remove_infraspecific_name_metadata)
        .pipe(create_strain_names)
        .pipe(construct_download_urls)
    )
    for column in ('assembly_level', 'refseq_category'):
        assemblies_df[column] = pd.Categorical(
            assemblies_df[column],
            categories=assembly_summary_config()[column],
            ordered=True,
        )
    return (
        assemblies_df
        .sort_values(
            by=['assembly_level', 'refseq_category', 'seq_rel_date'],
            ascending=[False, False, False],
        )
        .groupby('strain_name')
        .first()
        .reset_index(drop=True)
    )


def remove_infraspecific_name_metadata(df: pd.DataFrame) -> pd.DataFrame:
    df.infraspecific_name = df.infraspecific_name.apply(
        lambda row: (
            str(row.infraspecific_name)
            .replace('strain=', '')
            .replace('nan', '')
            .replace('substr. ', '')
        ),
    )
    return df


def create_strain_names(df: pd.DataFrame) -> pd.DataFrame:
    df.strain_name = df.organism_name.apply(
        make_strain_name_from_organism_name,
    )
    df.strain_name = df.apply(
        add_detailed_strain_designation,
        axis=1,
    )
    return df


def construct_download_urls(df: pd.DataFrame) -> pd.DataFrame:
    df.url_features = df.ftp_path.apply(
        lambda path: os.path.join(
            path,
            os.path.basename(path) + '_feature_table.txt.gz',
        ),
    )
    df.url_sequence = df.ftp_path.apply(
        lambda path: os.path.join(
            path,
            os.path.basename(path) + '_genomic.fna.gz',
        ),
    )
    return df


def make_strain_name_from_organism_name(organism_name: str) -> str:
    strain_name = re.sub(
        r"substr\. |str\. |subsp\. |\'|\[|\]", '', str(organism_name),
    )
    return re.sub(r'\b(\w+)( \1\b)+', r'\1', strain_name)


def is_infraspecific_in_strain_name(
    strain_name: str,
    infraspecific_name: str,
) -> bool:
    if infraspecific_name in strain_name:
        return True
    if infraspecific_name.replace(' ', '') in strain_name:
        return True
    return '(' in strain_name


def add_detailed_strain_designation(row: pd.Series) -> pd.Series:
    infraspecific_in_strain = is_infraspecific_in_strain_name(
        row.strain_name,
        row.infraspecific_name,
    )
    if not infraspecific_in_strain:
        row.strain_name = row.strain_name + ' ' + row.infraspecific_name
    return row.strain_name
