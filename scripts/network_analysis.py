#!/usr/bin/env python
#----------------------------------------------------------------------------
# ABOUT THE SCRIPT:
# This script is used to analyze the connection between highly connected
# proteins and number of corresponding protein domains. This is done by 
# creating an interaction network from a list of protein links, separating
# the proteins based on their degree in the network, and for each group 
# calculating how many protein domains correspond to each protein. This is 
# then visualized as a boxplot which is written to a png-file.
#
# ARGUMENTS:
# 1. List of protein links [input].
# 2. List of Pfam IDs and corresponding Ensembl protein IDs [input].
# 3. Name of output png-file [output].
#----------------------------------------------------------------------------

import sys
import numpy as np
import pandas as pd
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
from time import sleep

# Function that, given a network, separates nodes with degree higher or lower than 100.
def divide_nodes(network):
    nodes = list(network.nodes)
    degrees = [d for n, d in network.degree]

    over_100 = []
    under_100 = []

    p = 0

    for i in range(len(nodes)):
        
        if 100*i/(len(nodes)-1) > p:
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*p, p))
            sys.stdout.flush()
            sleep(0.25)
            p += 1

        if degrees[i] > 100:
            over_100.append(nodes[i])
        else:
            under_100.append(nodes[i])

    return over_100, under_100

# Function that, given a list of protein names and a data frame containing names of proteins and corresponding protein domans, calculates how many domains correspond to each protein and returns this as a list.
def get_number_of_domains(nodes, domains):
    number_of_domains = []

    p = 0

    for i in range(len(nodes)):

        if 100*i/(len(nodes)-1) > p:
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*p, p))
            sys.stdout.flush()
            sleep(0.25)
            p += 1

        number_of_domains.append(sum(domains['Protein stable ID'] == nodes[i]))

    return number_of_domains

# Function that, given a data frome containing integers, returns a list containing the logarithms of the integers.
def log_transform_domains(domains):
    log_transformed = []

    for number in domains:
        if number != 0:
            log_transformed.append(np.log(number))
        else:
            log_transformed.append(np.nan)

    return log_transformed

# Read file containg links that will be used to create a network.
network_data_frame = pd.read_csv(sys.argv[1], sep = ' ', header = None)

# Create network.
network = nx.from_pandas_edgelist(network_data_frame, source = 0, target = 1)

# Separate nodes in the netwok with a degree higher or lower than 100.
print("Separating proteins based on node degree.")
over_100, under_100 = divide_nodes(network)

# Read file containing information about protein domains.
domain_info = pd.read_csv(sys.argv[2], sep='\t')

# Filter away rows where the protein domain ID is missing.
domain_filtered = domain_info[pd.notna(domain_info['Pfam ID'])]

# Calculate number of protein domains corresponding to each protein in the two groups
print("\nCalculating domains for proteins with degree > 100.")
domains_over_100 = get_number_of_domains(over_100, domain_filtered)

print("\nCalculating domains for proteins with degree =< 100.")
domains_under_100 = get_number_of_domains(under_100, domain_filtered)

print("\nFinished calculations, generating boxplot.\n")

# Create data frame to use for plotting. Also include the logarithm of the number of domains.
combined_domains = pd.Series(domains_over_100+domains_under_100, dtype='object')
log_domains = pd.Series(log_transform_domains(combined_domains), dtype='object')
group_labels = pd.Series(np.repeat(['> 100', '=< 100'], [len(domains_over_100), len(domains_under_100)]), dtype='category')

df = pd.DataFrame({'Number of protein domains': combined_domains, 'log(Number of protein domains)': log_domains, 'Node degree': group_labels})

# Filter away rows representing proteins that did not have any known protein domains.
df_filtered = df[df['Number of protein domains'] != 0]

# Create boxplot
sns.set_style('whitegrid')
sns.set_context('talk')
sns_plot = sns.catplot(data=df_filtered, y='log(Number of protein domains)', x='Node degree', kind='box')
sns_plot.savefig(sys.argv[3], dpi=1200)
