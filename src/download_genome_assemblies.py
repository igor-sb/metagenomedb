import logging
from src.genome_assemblies.download import download_assembly_summaries

import fire  # type: ignore

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

if __name__ == '__main__':
	fire.Fire(download_assembly_summaries)
