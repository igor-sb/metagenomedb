"""Preprocess raw assembly summary table.

Clean up microbial strain names and select only the best microbial strain
genome assemblies (best assembly level, refseq category and most recent date).
"""

import logging

import fire

from src.genome_assemblies.io import (
    load_raw_assembly_summary_table,
    write_filtered_assembly_summary_table,
)
from src.genome_assemblies.preprocess_summary import (
    select_best_strain_assemblies,
)

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def main(input_assembly_summary: str, output_assembly_summary) -> None:
    LOG.info('loading raw assembly summary table')
    df = load_raw_assembly_summary_table(input_assembly_summary)
    LOG.info('preprocessing and selecting best assemblies')
    filtered_df = select_best_strain_assemblies(df)
    LOG.info('writing preprocessed assembly summary table')
    write_filtered_assembly_summary_table(filtered_df, output_assembly_summary)


if __name__ == '__main__':
    fire.Fire(main)
