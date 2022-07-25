# Master_Thesis: Software-based energy efficiency analysis: benchmarks and assessment methods
 
This repository contains all the data and experiments related to master thesis. 

This repository can be divided into three parts (folders): SLR, Experiments and Thesis manuscript 

The SLR folder contains all the steps and results obtained during the systematic literature review such as papers obtained from the queries, papers criteria analysis, data extraction and catalog of benchmarks. 

Composition of SLR folder: 
- Data extraction final papers: Contains the data obtained from final set of papers analysis (By individual papers and by a global overview). 
- Papers criteria satisfaction: Composed of several steps where for each step, an analysis by crietria is done on papers obtained from the queries. In total there are 4 steps.  
- Catalog of benchmarks.csv: Allows to see benchmarks wich are useful for assess energy consumption based their usage. All the benchmarks are used for assessing concurrency. 

The experiments folder contains all the scripts and data of the experiments. In total there are 8 experiments where 4 are for on type of computer and 4 for another type. 

Composition of Experiments folder: 
- Linux_PF0222 (PC1): Contains 4 experiments only for this computer. It is older computer. 
- MESSY (PC2): Contains also 4 experiments for this computer. It is a newer computer.

Remark: Each experiment is composed of a replication package of Vacation2 benchmark and the energy results obtained after running the Vacation2 benchmark. 
- processing.py: It is a python script that is used for generating the results for all experiments as graphs and tables. The results are stored in Visualization folder. 

Thesis manuscript contains the pdf of the thesis. 
