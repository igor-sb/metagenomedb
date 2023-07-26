import pandas as pd
import re


def load_raw_assembly_summary_table(filename):
	columns = {
		'#assembly_accession': str,
		'refseq_category': str,
		'taxid': str,
		'organism_name': str,
		'infraspecific_name': str,
		'assembly_level': str,
		'seq_rel_date': str,
		'ftp_path': str
	}
	return pd.read_csv(
		filename,
		delimiter='\t',
		skiprows=1,
		usecols=list(columns.keys()), 
		dtype=columns
	)


def remove_infraspecific_name_metadata(infraspecific_name):
	return (
		str(infraspecific_name)
		.replace('strain=', '')
		.replace('nan', '')
		.replace('substr. ', '')
	)


def make_strain_name_from_organism_name(organism_name):
	strain_name = (
		str(organism_name)
		.replace('substr. ', '')
		.replace('str. ', '')
		.replace('subsp. ', '')
		.replace('\'', '')
	)
	strain_name = (
		re.sub(r'\b(\w+)( \1\b)+', r'\1', strain_name)
		.replace('[', '')
		.replace(']', '')
	)
	return re.sub(r'\b(\w+)( \1\b)+', r'\1', strain_name)


def is_infraspecific_not_in_strain_name(strain_name, infraspecific_name):
	return (
		infraspecific_name not in strain_name and \
			infraspecific_name.replace(' ', '') not in strain_name and \
			'(' not in strain_name
	)


def add_detailed_strain_designation(row):
	if is_infraspecific_not_in_strain_name(
		row['strain_name'],
		row['infraspecific_name'],
	):
		return row['strain_name'] + ' ' + row['infraspecific_name']
	else:
		return row['strain_name']	