import pandas as pd
from pandas.testing import assert_frame_equal
from src.genome_assemblies.io import (
    load_raw_assembly_summary_table,
    preprocessed_assembly_summary_columns,
)
from src.genome_assemblies.preprocess_summary import select_best_strain_assemblies


def test_select_best_strain_assemblies(
    mock_assembly_summary_file,
    mock_preprocessed_assembly_summary_file,
):
    df = load_raw_assembly_summary_table(mock_assembly_summary_file)
    preprocessed_cols = preprocessed_assembly_summary_columns()
    expected_df = pd.read_csv(
        mock_preprocessed_assembly_summary_file,
        delimiter='\t',
        usecols=list(preprocessed_cols.keys()),
        dtype=preprocessed_cols,
    )
    actual_df = select_best_strain_assemblies(df)
    for column in ('assembly_level', 'refseq_category'):
        actual_df[column] = actual_df[column].astype(str)
    assert_frame_equal(left=actual_df, right=expected_df)
