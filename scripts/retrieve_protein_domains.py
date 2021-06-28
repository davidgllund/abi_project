#!/usr/bin/env python
#----------------------------------------------------------------------------
# ABOUT THE SCRIPT:
# This script can be used to obtain a list of Pfam IDs and corresponding
# Ensembl protein IDs from the Human Genes (GRCh38.p13) dataset from BioMart.
#----------------------------------------------------------------------------

import pandas
from pybiomart import Dataset

# Define which dataset should be queried.
dataset = Dataset(name='hsapiens_gene_ensembl',
                  host='http://www.ensembl.org')

# Obtain data frame containing the relevant data.
df = dataset.query(attributes=['pfam','ensembl_peptide_id'], only_unique=False)

# Convert the data frame to a list and print it.
results = df.to_csv(index=False, sep='\t')
print(results)
