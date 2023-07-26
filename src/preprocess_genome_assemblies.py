"""Preprocess raw assembly summary table.

Clean up microbial strain names and select only the best microbial strain
genome assemblies (best assembly level, refseq category and most recent date).
"""

import fire

from src.genome_assemblies.preprocess import (
    load_raw_assembly_summary_table,
    select_best_strain_assemblies,
    write_filtered_assembly_summary_table,
)


def main(input_assembly_summary: str, output_assembly_summary) -> None:
    df = load_raw_assembly_summary_table(input_assembly_summary)
    filtered_df = select_best_strain_assemblies(df)
    write_filtered_assembly_summary_table(filtered_df, output_assembly_summary)


if __name__ == '__main__':
    fire.Fire(main)
