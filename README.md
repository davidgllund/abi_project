# Course project: Are well-connected proteins more multi-faceted than others?

This repository contains files used for the Applied bioinformatics course project. 

## Contents of repository

### **Makefile**

Main file used to produce the results.


### **config.mk**

Cofiguration file required to run the makefile.

### **abi_project_env.yml**

**yml**-file that can be used to easily create a conda environment containing all dependencies.

### **scripts**

Directory containing auxiliary python scripts used during the analysis.

- **retrieve_protein_domains.py**
- **network_analysis.py**

## Dependencies

To run, you need to have the following packages installed:

Python >= 3.8.10
- numpy >= 1.19.1
- pandas >= 1.1.3
- networkx >= 2.5.1
- matplotlib >= 3.4.2
- seaborn >= 0.11.0
- pybiomart >= 0.2.0

Alternatively, if you have conda installed you can use the provided file **abi_project_env.yml** to create an appropriate environment using

```bash
conda env create -f abi_project_env.yml
```
