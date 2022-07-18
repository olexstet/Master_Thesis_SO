#!/bin/bash

# last modified: 15/12/2021

echo "Starting Automation Script (RAW version)..."


# this is the benchmark version with transacional actors
#lein run -- -vtxact -w 4 -s 8 -t 30 -n 300

# this is the original version of the benchmark
#
#lein run -- -v original -w 4 -s 8 -t 30 -n 300

# Paramteres defintion:
# -v either orginal or txact.
# -w the number of primary worker actors.
# -s the number of secondary worker actors. (this is only available for txact version)
# -t the numver of reservations.
# -n number of queries per relation per reservation.
# -r number of flights/rooms/cars.
# -p work factor for password generation.
# -d prnt debug information

#Version=txact
#primary_worker_actors=1
#secondary_worker_actors=20
#num_reservations=50
#num_queries=10

primary_worker_actors=1
secondary_worker_actors=1
num_reservations=1000
num_flights_cars=50
num_queries=10
p=5



echo "currently running Bash ${BASH_VERSION}"

threads="1 2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 62 64"
secondary_threads="01 02 08 64"

printf "Are you sure you want to start the script? the files in output/RAW will be deleted (y/n)"
read answer


if [[ "$answer" == "y" ]]
	then	
		[[ -d ../output/RAW ]] && rm -R ../output/RAW
		mkdir ../output/RAW
	else
		exit 1
fi
			



runExperiment(){

	# first argument ($1): experiment version
	# second argument($2): number of secondary threads	
	# third argument ($3): number of repetitions of the experiment
	

	output_name="output2-RAW-timing-vacation2-linux.csv"
	for j in $(seq -f "%02g" 1 $3)
	do
		for i in $threads
		do
			
			cd ../vacation2
			startDate="$(LC_ALL=de_DE.utf8 date)"
                        command="lein run -- -v $1 -w ${i} -s $2 -t ${num_reservations} -r ${num_flights_cars} -n ${num_queries} -p ${p}"

                        output=$(lein run -- -v $1 -w ${i} -s $2 -t ${num_reservations} -r ${num_flights_cars} -n ${num_queries} -p ${p})
			endDate="$(LC_ALL=de_DE.utf8 date)"
			RAW_TIME_LOG="-v $1 -w ${i} -s $2 -t ${num_reservations} -r ${num_flights_cars} -n ${num_queries} -p ${p}, $startDate, $endDate" 
			echo ${RAW_TIME_LOG} >> ../output/RAW/${output_name}
		done
	done
}

encapsulate(){

    runExperiment "original" "0" $1
    
    runExperiment "txact" "1" $1
    
    runExperiment "txact" "2" $1
    
    runExperiment "txact" "8" $1

    
    runExperiment "txact" "64" $1

}


start1=`date +%s`
encapsulate "1"
end=`date +%s`
runtime=$((end-start1))
echo $runtime
# echo ${output2} | sed -n "s/\([0-9]\{4\}\.[0-9]\{3\}\)/"

echo "shell program done!"
