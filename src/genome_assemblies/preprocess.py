import os
import re

import pandas as pd

from src.genome_assemblies.io import assembly_summary_config


def select_best_strain_assemblies(assemblies_df: pd.DataFrame) -> pd.DataFrame:
    assemblies_df = (
        assemblies_df
        .pipe(remove_infraspecific_name_metadata)
        .pipe(add_strain_name_column)
        .pipe(add_features_sequence_url_columns)
    )
    for column in ('assembly_level', 'refseq_category'):
        assemblies_df[column] = pd.Categorical(
            assemblies_df[column],
            categories=assembly_summary_config()[column],
            ordered=True,
        )
    column_order = assemblies_df.columns
    return (
        assemblies_df
        .sort_values(
            by=['assembly_level', 'refseq_category', 'seq_rel_date'],
            ascending=[True, True, False],            
        )
        .groupby('strain_name')
        .first()
        .reset_index()
        .reindex(columns=column_order)
    )


def remove_infraspecific_name_metadata(df: pd.DataFrame) -> pd.DataFrame:
    df.infraspecific_name = df.infraspecific_name.apply(
        lambda row: (
            str(row)
            .replace('strain=', '')
            .replace('nan', '')
            .replace('substr. ', '')
        ),
    )
    return df


def add_features_sequence_url_columns(df: pd.DataFrame) -> pd.DataFrame:
    df['url_features'] = df.ftp_path.apply(
        lambda path: os.path.join(
            path,
            os.path.basename(path) + '_feature_table.txt.gz',
        ),
    )
    df['url_sequence'] = df.ftp_path.apply(
        lambda path: os.path.join(
            path,
            os.path.basename(path) + '_genomic.fna.gz',
        ),
    )
    return df


def make_strain_name_from_organism_name(organism_name: str) -> str:
    strain_name = re.sub(
        r"(substr\. |str\. |subsp\. |'|\[|\])", '', str(organism_name),
    )
    return re.sub(r'\b(\w+)( \1\b)+', r'\1', strain_name)


def is_infraspecific_in_strain_name(
    strain_name: str,
    infraspecific_name: str,
) -> bool:
    if infraspecific_name == 'na':
        return True
    if infraspecific_name in strain_name:
        return True
    if infraspecific_name.replace(' ', '') in strain_name:
        return True
    return '(' in strain_name


def add_strain_name_column(df: pd.DataFrame) -> pd.DataFrame:
    df['strain_name'] = df['organism_name'].apply(
        make_strain_name_from_organism_name,
    )
    rows_with_detailed_labels = df.apply(
        lambda row: is_infraspecific_in_strain_name(
            row.strain_name,
            row.infraspecific_name,
        ),
        axis=1,
    )
    df.loc[~rows_with_detailed_labels, 'strain_name'] = (
        df[~rows_with_detailed_labels]['strain_name']
        + ' '
        + df[~rows_with_detailed_labels]['infraspecific_name']
    )
    return df
