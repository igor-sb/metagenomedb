from typing import Any

import pandas as pd
import yaml


def assembly_summary_config(
    filename: str = 'config/genome_assembly.yaml',
) -> dict[str, Any]:
    with open(filename) as yaml_config:
        config = yaml.safe_load(yaml_config)
    return config


def load_raw_assembly_summary_table(filename: str) -> pd.DataFrame:
    config = assembly_summary_config()
    return pd.read_csv(
        filename,
        delimiter='\t',
        skiprows=1,
        usecols=list(config['columns'].keys()),
        dtype=config['columns'],
    )


def write_filtered_assembly_summary_table(
    df: pd.DataFrame,
    filename: str,
) -> None:
    df.to_csv(filename, sep='\t', index=False)
