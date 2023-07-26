import re

import pandas as pd


def load_raw_assembly_summary_table(filename: str) -> pd.DataFrame:
    columns = {
        '#assembly_accession': str,
        'refseq_category': str,
        'taxid': str,
        'organism_name': str,
        'infraspecific_name': str,
        'assembly_level': str,
        'seq_rel_date': str,
        'ftp_path': str,
    }
    return pd.read_csv(
        filename,
        delimiter='\t',
        skiprows=1,
        usecols=list(columns.keys()),
        dtype=columns,
    )


def remove_infraspecific_name_metadata(infraspecific_name: str) -> str:
    return (
        str(infraspecific_name)
        .replace('strain=', '')
        .replace('nan', '')
        .replace('substr. ', '')
    )


def make_strain_name_from_organism_name(organism_name: str) -> str:
    strain_name = (
        str(organism_name)
        .replace('substr. ', '')
        .replace('str. ', '')
        .replace('subsp. ', '')
        .replace("'", '')
    )
    strain_name = (
        re.sub(r'\b(\w+)( \1\b)+', r'\1', strain_name)
        .replace('[', '')
        .replace(']', '')
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
        row['strain_name'],
        row['infraspecific_name'],
    )
    if infraspecific_in_strain:
        return row['strain_name']
    return row['strain_name'] + ' ' + row['infraspecific_name']
