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
