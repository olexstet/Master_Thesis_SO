#!/bin/bash

### functions ###


cleanDirectory(){
	
	[[ -d execution-times ]] && rm -R execution-times && printf 'Directory (/execution-times) has been cleaned!\n'
	[[ -d graphs ]] && rm -R graphs && printf 'Directory (/graphs) has been cleaned!\n'



}

createFolderStructure(){
	mkdir execution-times
	mkdir graphs
	mkdir execution-times/original
	

	local folderNumbers="01 02 08 64"
	for folderName in $folderNumbers; do	mkdir execution-times/txact-"$folderName"; done
	
	printf 'Created full folder structure for experiment validation!\n'
}

extractExecutionTimes(){ 
	
	cd ../output/Logging/$1/
        for f in *;
        do 
		
		#printf 'file name generated: execution-time%s\n' $f
		mawk '/time/ {print $(NF - 1)}' "$f" >> ../../../validation/execution-times/"$1"/execution-time-"$f"
        done  

       printf 'Extracted all time executions from output/Logging/%s!\n' $1	
       cd ../../../validation
}


### variables ###
folderNames="original txact-01 txact-02 txact-08 txact-64"

### main function ###
main(){

	cleanDirectory
	
	createFolderStructure
	
	for folder in $folderNames
		do	
			extractExecutionTimes "$folder"
		done
	
	python3 plotting-program.py
}

main

