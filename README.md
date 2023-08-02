[![CI](https://github.com/igor-sb/metagenomedb/actions/workflows/ci.yml/badge.svg)](https://github.com/igor-sb/metagenomedb/actions)
[![codecov](https://codecov.io/gh/igor-sb/metagenomedb/branch/main/graph/badge.svg?token=WRQ8X3SDVA)](https://codecov.io/gh/igor-sb/metagenomedb)

# Metagenome 16S Database

Code for downloading, preprocessing, and organizing microbial 16S sequences
based on full genome assemblies from NCBI Genome and NCBI RefSeq databases.

## Installation

For reproducible analysis, first install [poetry](https://python-poetry.org/docs/#installation) package manager. Then run:

```sh
make install
make shell
```

## Download microbial genome assembly summary tables

```py
mkdir data
python src/download_genome_assemblies.py data/
```

This will create two files with the current date in the format YYYY-MM-DD:

- data/archaea_assembly_summary_YYYY-MM-DD.txt
- data/bacteria_assembly_summary_YYYY-MM-DD.txt

## Preprocess genome assembly summary tables

The two tables with genome assembly summaries are pre-processed, by cleaning up
microbial strain names, since multiple genome assemblies can be listed for the
exact same strain.

For each unique microbial strain, a single assembly is picked by selecting:

- the highest assembly level ('Complete Genome' > 'Chromosome' > 'Scaffold' > 'Contig')
- the highest RefSeq level ('reference genome' > 'representative genome' > 'na') 
- the most recent date ('seq_rel_date')

If there are still multiple assemblies following these criteria, we just pick the
first one from the list.

```py
python src/preprocess_genome_assemblies.py \
    archaea_assembly_summary_YYYY-MM-DD.txt \
    archaea_assembly_summary_YYYY-MM-DD_filtered.txt

python src/preprocess_genome_assemblies.py \
    bacteria_assembly_summary_YYYY-MM-DD.txt \
    bacteria_assembly_summary_YYYY-MM-DD_filtered.txt

```

This will create two additional files:

- data/archaea_assembly_summary_YYYY-MM-DD_filtered.txt
- data/bacteria_assembly_summary_YYYY-MM-DD_filtered.txt
