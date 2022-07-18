# vacation2-benchmark-replication-package
This is a replication package that runs the vacation2[1][2] benchmark. 

## Assumptions/Pre-requisites
Desktop computer with at least 16 Gb Memory.
processor      Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz
disk           512GB ADATA SSD SX900
system         OptiPlex 9020 (05A4)

### Accuracy tip
Make sure to reduce the amount of processes active in the background as much as possible when running the experiment to increase the accuracy and reliability of the results.

### Software
20.04.2-Ubuntu
x86_64 GNU/Linux

Python 3.8.10

Leiningen 2.9.8 on Java 11.0.11 OpenJDK 64-Bit Server VM

#### Lein
You can run the program using [Leiningen](https://leiningen.org/). Follow the instructions at that website to install and setup leiningen.

To test if Leiningen is working, clone the repo and navigate to the /vacation2 directory inside the terminal using the command:<br />
`$ cd vacation2-benchmark-replication-package/vacation2`

Then run the command

`$ lein run -- -v original -w 1 -s 0 -t 1000 -r 50 -n 10 -p 5`

some output should pop up, when the execution is done, the last output should be the parameters used inside the experiment. Those Parameters are defined at the end of this README.md

**Note:** Those parameters were the ones chosen and run by the original authors.[2]<br />
**Important:** Make sure lein command is working, otherwise the script will not work.


## Recommended Setup

1. Clone this repo using the command in the terminal:<br /> `git clone --recursive https://minsky.uni.lu/gitlab/ac-devops/energy-efficiency`
2. Go inside the src folder inside the repo using the command:<br /> `cd vacation2-benchmark-replication-package/src/`
3. Make the bash scripts executable using the command:<br /> `sudo chmod +x <bash script name>` <br />
example: <br /> `sudo chmod +x automate-experiments-vacation2-logging.bash`


## Experiment execution

There are two bash scripts that run the experiment described in the research paper of Swalens, J., Koster, J. D., & Meuter, W. D. (2021)[2]:
1. automate-experiments-vacation2-logging.bash: maximal information logging, may be energy and time extensive. Meant for generation of charts later on.
2. automate-experiments-vacation2-RAW.bash: minimal information logging, meant to be used when measuring the power consumption during the run of the experiment using a device on the computer. <br />

Then, there is a third script that will extract time units from the execution of the experiment and plot the results to validate the replication of the original experiment. <br />

1. plotting-main.bash: script that cleans the previous data inside validation/execution-times and validation/graphs and reproduces them using the information
inside output/Logging. It then calls the python program <plotting-program.py> to generate the charts.<br />
**WARNING:** Running the first script will take a long time. On the machine used in this respository, it took around **FIVE AND A HALF** *hours*.
Running the first script will generate all the data needed to get the experiment results for the computer being used as well as allow for chart plotting later.
### Running the script
**IMPORTANT(1):** Running any bash script will require running them directly from the directory they are in. That means if a bash script is inside src/ then you need to go inside that folder (using, for example, cd src/ command) and THEN run the script. <br />

**IMPORTANT(2):** The script <automate-experiments-vaation2-logging.bash> **MUST BE RUN WITH ADMINISTRATOR PRIVILEGE (i.e use sudo command)**


1. Run the script using the command:<br /> `bash automate-experiments-vacation2-logging.bash`
	1. a whole run for an experiment is defined as running the following command 33 iterations:<br /> `-v original -w 1 -s 0 -t 1000 -r 50 -n 10 -p 5`
	for each iteration, the only variable changed during the run is the **-w**, which is the thread count. it has the following values throughout the run:
<br /> [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64]
	
	2. For every run, the variable **-v** is changed along side the variable **-s**.
	**-v** is the version of the bench mark. "original" is the original version with only primary workers (i.e **-w**).
	The other version of the bench mark is "txact", which has secondary workers (i.e **-s**).Only this version has secodary workers, in the "original" they default to 0.
	The original experiment by the researchers was done with the following versions: original, txact (s=1), txact (s=2), txact(s=8) and txact(s=64)
	Each run of those paramters was repeated **30** times. This means the command lein is being called: $33 (number of primary threads) \times 5 (number of different versions) \times 30 (number of repetitions) = **4950** $

## Data analysis

1. Run the plotting-main.bash throught the following command: <br /> `bash plotting-main.bash` (do not forget to make this script executable!).

When the script is done, there should be 2 new graphs generated from the files inside the execution-times/ folder.
[Graphs](https://minsky.uni.lu/gitlab/ac-devops/energy-efficiency/-/tree/main/validation/graphs)


## Paramteres defintion:

<br /> **-v** either orginal or txact.
<br /> **-w** the number of primary worker actors.
<br /> **-s** the number of secondary worker actors. (this is only available for txact version)
<br /> **-t** the numver of reservations.
<br /> **-n** number of queries per relation per reservation.
<br /> **-r** number of flights/rooms/cars.
<br /> **-p** work factor for password generation.
<br /> **-d** prnt debug information

# References
[1] github repo of the original [vacation2](https://github.com/jswalens/vacation2) benchmark <br />
[2] Swalens, J., Koster, J. D., & Meuter, W. D. (2021). Chocola: Composable Concurrency Language. ACM Transactions on Programming Languages and Systems (TOPLAS), 42(4), 1-56.
