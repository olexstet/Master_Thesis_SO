#!/bin/bash

# last modified: 15/12/2021

echo "Starting Automation Script..."







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

printf "Are you sure you want to start the script? all output files will be deleted (y/n)"
read answer

if [[ "$answer" == "y" ]]
	then	
		cd ..
		[[ -d output ]] && rm -R output
		mkdir output
		cd src
	else
		exit 1
fi
			
printf "Collecting machine and system information..."

OS_INFO=$(lsb_release -a)
SYS_INFO=$(dmidecode -t system | grep -A8 '^System Information')
PROCESSOR_INFO1=$(sudo dmidecode -t processor | grep -A6 '^Processor Information')
PROCESSOR_INFO2=$(sudo dmidecode -t processor | grep -A17 'Version')
MEMORY_INFO=$(dmidecode -t memory | grep -B18 'Configured Memory Speed: [0-9]* MT/s')


echo creating the folders neccessary for the replication of the experiment...

folderNames="Logging RAW meta-data"
subfolderNames="original txact-01 txact-02 txact-08 txact-64"
for i in $folderNames; do mkdir ../output/"$i" ; done
for i in $subfolderNames; do mkdir ../output/Logging/"$i" ; done

# creates the following folders:
# /Logging 
# /RAW
# /graphs


[[ -e ../output/meta-data/system-information.txt  ]] && rm ../output/meta-data/system-information.txt

printf "Writing system information into output/meta-data/system-information.txt ..."

DATE=$(LC_ALL=de_DE.utf8 date)

printf -- "-----------------------------------------\n" >> ../output/meta-data/system-information.txt
echo "|   Author: BOGHOS YOUSEEF                |" >> ../output/meta-data/system-information.txt
echo "|   Email: boghos.youseef@outlook.com     |" >> ../output/meta-data/system-information.txt
echo "|   Date: ${DATE} |" >> ../output/meta-data/system-information.txt
printf -- "-----------------------------------------\n\n\n" >> ../output/meta-data/system-information.txt

printf -- "\n------ OS Information ------\n" >> ../output/meta-data/system-information.txt
echo "$OS_INFO" >> ../output/meta-data/system-information.txt

printf -- "---------------------------------------\n\n" >> ../output/meta-data/system-information.txt

printf -- "------ System Information ------\n" >> ../output/meta-data/system-information.txt
echo "$SYS_INFO" >> ../output/meta-data/system-information.txt

printf -- "---------------------------------------\n\n" >> ../output/meta-data/system-information.txt
printf -- "------ Processor Information ------\n" >> ../output/meta-data/system-information.txt
echo  "$PROCESSOR_INFO1" >> ../output/meta-data/system-information.txt
printf -- "\n\n\n" >> ../output/meta-data/system-information.txt
echo  "$PROCESSOR_INFO2" >> ../output/meta-data/system-information.txt
printf -- "---------------------------------------\n" >> ../output/meta-data/system-information.txt
printf -- "\n------ Memory Information ------ \n"  >> ../output/meta-data/system-information.txt
echo "$MEMORY_INFO" >> ../output/meta-data/system-information.txt
printf -- "---------------------------------------\n" >> ../output/meta-data/system-information.txt

runExperiment(){

	# first argument ($1): experiment version
	# second argument($2): number of secondary threads	
	# third argument ($3): number of repetitions of the experiment

	if [[ "$1" == "original" ]];
		then 	
			local outputDir='original'
	else
		if [[ "$2" == "64" ]];
			then 
				local outputDir="txact-$2"
		else

			local outputDir="txact-0$2"
		fi
		echo --------------------output dir: $outputDir
	fi

	#for j in $( seq 1 $3 )
	for j in $(seq -f "%02g" 1 $3)
	do
		for i in $threads
		do
			
			#echo current working directory: "$(pwd)"
			cd ../vacation2

			#echo current working directory: "$(pwd)"
			#echo now in loop number "$i"

			echo "Running the script with the following options:  -v $1 -w ${i} -s $2 -t ${num_reservations} -r ${num_flights_cars} -n ${num_queries} -p ${p}"
		
			output=$(lein run -- -v $1 -w ${i} -s $2 -t ${num_reservations} -r ${num_flights_cars} -n ${num_queries} -p ${p})
			output_name="output${j}-$1-$2-vacation2-linux.txt"
			echo ${output_name}

			cd ../output/Logging/$outputDir
			
			#echo current working directory: "$(pwd)"
			#echo Now writing the results to "$output_name".
			echo "${output}" >> ./"${output_name}"
			cd ../../
			
			#echo current working directory: "$(pwd)"
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
encapsulate "30"
end=`date +%s`
runtime=$((end-start1))
echo $runtime

echo "shell program done!"
