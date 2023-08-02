import pandas as pd

from metagenomedb.genome_assemblies.io import load_raw_assembly_summary_table


def test_load_raw_assembly_summary_table(mock_assembly_summary_file):
    df = load_raw_assembly_summary_table(mock_assembly_summary_file)
    assert isinstance(df, pd.DataFrame)
