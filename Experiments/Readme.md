# Experiments

This folder contains all the experimental data as well as the script for running the experiment (Vacation2) and generating the results. 

In two folders Linux-PF0222 (PC1) and MESSY (PC2) can be found experiments and their results.
In each folder, there are 4 experiments and each experiment has a replcation package of Vacation2 benchmark. 
The difference between each experiment is in the Vacation2 parameter (t), which corresponds to the number of reservations. 

- Experiment1: Contains the default parameters of the Vacation2 benchmark and where t is equal to 1000. 
- Experiment2: t = 10 
- Experiment3: t = 50 
- Experiment4: t = 100 

For running an experiment, the following has to be done: 

1. Open terminal 
2. In terminal, access the src folder of energy-efficiency of one experiment. (i.e: https://github.com/olexstet/Master_Thesis_SO/tree/main/Experiments/Linux-PF0222/Experiment1/energy-efficiency/src) 
3. Run Vacation2-energy-consumption-RAPL.bash as: bash Vacation2-energy-consumption-RAPL.bash
4. Waiting until the end of the execution (it may take hours to execute everything for one experiment). Results during the runtime are written in output folder:https://github.com/olexstet/Master_Thesis_SO/tree/main/Experiments/Linux-PF0222/Experiment1/energy-efficiency/output 
5. Perform the same steps (2-4) on other experiments 
6. Access Experiments folder (https://github.com/olexstet/Master_Thesis_SO/tree/main/Experiments) for running processing.py file for generating graphs and tables in Visualization folder.
6'. If you want to generate graphs and tables for single experiment, then in processing.py modify the pc_paths and experiment_paths ( comment or remove unuseful ones).
7. Processing.py script will take some minutes to generate the results which can be found here as exemple: https://github.com/olexstet/Master_Thesis_SO/tree/main/Experiments/Linux-PF0222/Experiment1/Visualization. 

Remarks: As experiments take a lot of time to execute, the decision was taken to execute them one by one and not creating a script that allow to run everything at once. 

