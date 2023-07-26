import re
import types

import pandas as pd

# See: https://tinyurl.com/DictConstant
ASSEMBLY_LEVELS = ('Complete Genome', 'Chromosome', 'Scaffold', 'Contig')
REFSEQ_LEVELS = ('reference genome', 'representative genome', 'na')
RAW_ASSEMBLY_SUMMARY_COLUMNS = types.MappingProxyType({
    '#assembly_accession': str,
    'refseq_category': str,
    'taxid': str,
    'organism_name': str,
    'infraspecific_name': str,
    'assembly_level': str,
    'seq_rel_date': str,
    'ftp_path': str,
})


def select_best_strain_assemblies(assemblies_df: pd.DataFrame) -> pd.DataFrame:
    assemblies_df.infraspecific_name = assemblies_df.infraspecific_name.apply(
        remove_infraspecific_name_metadata,
    )
    assemblies_df.strain_name = assemblies_df.organism_name.apply(
        make_strain_name_from_organism_name,
    )
    assemblies_df.assembly_level = pd.Categorical(
        assemblies_df.assembly_level,
        categories=ASSEMBLY_LEVELS,
        ordered=True,
    )
    assemblies_df.refseq_category = pd.Categorical(
        assemblies_df.refseq_category,
        categories=REFSEQ_LEVELS,
        ordered=True,
    )
    assemblies_df.strain_name = assemblies_df.apply(
        add_detailed_strain_designation,
        axis=1,
    )
    assemblies_df = assemblies_df.sort_values(
        by=['assembly_level', 'refseq_category', 'seq_rel_date'],
        ascending=[False, False, False],
    )
    return (
        assemblies_df
        .groupby('strain_name')
        .first()
        .reset_index(drop=True)
    )


def load_raw_assembly_summary_table(filename: str) -> pd.DataFrame:
    return pd.read_csv(
        filename,
        delimiter='\t',
        skiprows=1,
        usecols=list(RAW_ASSEMBLY_SUMMARY_COLUMNS.keys()),
        dtype=RAW_ASSEMBLY_SUMMARY_COLUMNS,
    )


def write_filtered_assembly_summary_table(
    df: pd.DataFrame,
    filename: str,
) -> None:
    df.to_csv(filename, sep='\t', index=False)


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
        row.strain_name,
        row.infraspecific_name,
    )
    if not infraspecific_in_strain:
        row.strain_name = row.strain_name + ' ' + row.infraspecific_name
    return row.strain_name
