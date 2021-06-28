## About this file:
## ----------------
## This makefile performs the following tasks:
## 1. Downloads the Homo sapiens part of STRING
## 2. Creates an interaction network by selecting the edges with a "combined score" larger or equal to 500, a number which indicates significance.
## 3. Partition the proteins in two groups, the ones with a node degree larger than 100 and one smaller or equal to 100.
## 4. Download the number of known protein-domains per Ensembl id from BioMart.
## 5. Make a boxplot, comparing the number of domains of proteins with node degrees >100 to the ones with node degrees <=100.
## 
## Auxillary scripts:
## ------------------
## To run, the following python scripts need to be located in the "scripts" subdirectory:
## - retrieve_protein_domains.py
## - network_analysis.py
##
## Dependencies:
## -------------
## To run, you need the following packages installed:
## 
## Python >= 3.8.10
## - numpy >= 1.19.1
## - pandas >= 1.1.3
## - networkx >= 2.5.1
## - matplotlib >= 3.4.2
## - seaborn >= 0.11.0
## - pybiomart >= 0.2.0
## 
## Rules:
## ------

include config.mk

LINKS=protein_links.txt
SIGN=significant_proteins.txt
DOMAINS=proteins_w_domains.txt
PNG=protein_domains_vs_string_degree.png

.PHONY : all
all : $(PNG)

## protein_links.txt			: Download protein links from STRINGDB.
$(LINKS) :
	curl https://stringdb-static.org/download/protein.links.v11.0/9606.protein.links.v11.0.txt.gz -o $@.gz
	gunzip $@.gz

## proteins_w_domains.txt			: Retrieve protein domains from BioMart.
$(DOMAINS) : $(BIOMRT_SRC) 
	 $(BIOMRT_EXE) > $@

## significant_proteins.txt		: Extract significant (combined score > 500) protein links.
$(SIGN) : $(LINKS)
	awk -F ' ' '{{ if ( int($$3) >= 500 ) print $$1, $$2 }}' $< | awk '{{ gsub("9606.", ""); print }}'  > $@

## protein_domains_vs_string_degree.png	: Perform analysis and display results in png format.
$(PNG) : $(NETWRK_SRC) $(SIGN) $(DOMAINS)
	$(NETWRK_EXE) $(SIGN) $(DOMAINS) $@

## clean					: Remove auto-generated files.
.PHONY : clean
clean :
	rm $(LINKS) $(SIGN) $(DOMAINS) $(PNG)

.PHONY : variables
variables :
	@echo LINKS: $(LINKS)
	@echo SIGN: $(SIGN)
	@echo DOMAINS: $(DOMAINS)
	@echo PNG: $(PNG)

.PHONY : help
help : Makefile
	@grep ^'##' $< | sed 's/\## //g'
