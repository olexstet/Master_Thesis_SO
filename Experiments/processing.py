#Libraries
import os
import shutil
import re
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d
import numpy as np 

#Path definition 
pc_paths = ["Linux-PF0222", "MESSY"]
experiment_paths = ["Experiment1","Experiment2","Experiment3","Experiment4"]
log_files_path = "energy-efficiency/output/Logging"
output_path = "Visualization"

# Allows to generate paths for using logging files (experimental data) and for storing the output data 
def paths_generation(pc_paths, experiment_paths,log_files_path,output_path):
    inter_path = []
    #Generate paths for experiments
    for pc in pc_paths: 
        for exp in experiment_paths: 
            inter_path.append(pc+"/"+exp)
    
    paths = []
    #Generate paths for logging and output 
    for p in inter_path: 
        paths.append([p + "/" + log_files_path, p + "/" + output_path])
    
    return paths

# Get Joules value from text to float 
def get_value_Double_Joules(string):
    count = string.count('.')
    count2 = string.count(",")
    # Manage exceptions and problems of the string with . and ,  
    if count  == 1 and count2 == 0: 
        string = string.replace(".",",")
    if count >= 1 and count2 == 1: 
        string = string.replace(".","")
    
    #regular exception for finding value in string 
    value_string = re.search(r'\d+,\d+', string).group()

    return float(value_string.replace(",",".")) # get float from string 

# Used for getting execution time (double) from string 
def get_value_Double_Exec_Time(string):
    value_string = re.search(r'\d+.\d+', string).group()
    return float(value_string)

# Used for getting integers from string 
def get_value_Int(string):
    value_string = re.search(r'\d+', string).group()
    return int(value_string)

# Used for preprocessing the logging data for an experiment. The goal is to organize experimental data in tables 
def preprocessing(tuple_path):
    names_dir = ["original","txact-01","txact-02","txact-08","txact-64"] # folders where data is stored for each configuration 
    dir_files = {}
    
    path_logging = tuple_path[0]
    path_output = tuple_path[1]

    # Set files in correct order for reading (sorting based on integers values in files name)
    for dir_name in names_dir: 
        files_in_dir = os.listdir(path_logging+"/"+dir_name)
        lenght = len(files_in_dir) 
        i = 1
        files_names = []
        # indetify the right files in correct order 
        while i < lenght+1:
            for file in files_in_dir: 
                if i < 10 and "output0"+str(i) in file: 
                    files_names.append(file)
                if i >= 10 and "output"+str(i) in file:
                    files_names.append(file)
            i += 1

        dir_files[dir_name] = files_names

    data = {}
    #Extract data from each file. Data extracted is: Options, execution time, cores, ram, gpu, pkg, seconds (perf execution time)
    for dir_name in names_dir: 
        file_data = []
        for file_name in dir_files[dir_name]:
            file_path = path_logging + "/" + dir_name + "/"+ file_name
            f = open(file_path, "r") # assess the file (open file)
            data_option = []
            end = False 
            option = ""
            #read each line in the opened file and extracted relevant data based on keywords for each line. 
            for line in f: 
                if "options" in line: 
                    option = line[11:len(line)-2]

                if "execution time" in line:
                    data_option.append(["execution time",get_value_Double_Exec_Time(line)])

                if "cores" in line: 
                    data_option.append(["cores",get_value_Double_Joules(line)]) 
                    
                if "ram" in line: 
                    data_option.append(["ram",get_value_Double_Joules(line)])

                if "gpu" in line: 
                    data_option.append(["gpu",get_value_Double_Joules(line)])

                if "pkg" in line: 
                    data_option.append(["pkg",get_value_Double_Joules(line)])
                    
                if "seconds" in line: 
                    data_option.append(["seconds",get_value_Double_Joules(line)])
                    end = True 
                
                if end == True: # Decide when all data for one option is retrieved (data is obtained for one perf file)
                    file_data.append([option, data_option])
                    data_option = []
                    option = ""
                    end = False  

        data[dir_name] = file_data # Store results of all files for a version as a dictionary 
    
    #Variables to retrieve from the data
    options = []
    results_cores = []
    results_ram = []
    results_gpu = []
    results_pkg = []
    results_time_perf = []
    results_time_exec = []
    results_power_cores = []
    results_power_ram = []
    results_power_gpu = []
    results_power_pkg = []
    results_ratio_time = []

    options_version = []
    options_n_workers = []
    options_n_secondary_workers = []
    options_n_reservations = []
    options_n_relations = []
    options_n_queries = []
    options_password_work_factor = []

    # Get result from the dictionary based on key (version) 
    for version in data: 
        for values in data[version]: # get values (option, data_option) from the dictionary 
            
            option = values[0] # options
            result = values[1] # data obtained for a single run based on option setup 

            # Store results in the right variables 
            options.append(option)
            results_time_exec.append(round(result[0][1]/1000,7))
            results_cores.append(result[1][1])
            results_ram.append(result[2][1])
            results_gpu.append(result[3][1])
            results_pkg.append(result[4][1])
            results_time_perf.append(round(result[5][1],7))
            
            # Compute power 
            power_cores = round(result[1][1]/result[5][1],2)
            power_ram = round(result[2][1]/result[5][1],2)
            power_gpu = round(result[3][1]/result[5][1],2)
            power_pkg = round(result[4][1]/result[5][1],2)
            
            # Compute ratio between execution time and perf time 
            ratio_time = round(round(result[0][1]/1000,7)/result[5][1],7) 

            results_power_cores.append(power_cores)
            results_power_ram.append(power_ram)
            results_power_gpu.append(power_gpu)
            results_power_pkg.append(power_pkg)
            results_ratio_time.append(ratio_time)

            # Split the option because option is a concatenation of several variables, the code below obtain all the variables individually 

            split_string = option.split(",")
            corrected_split = []
            for o in split_string:
                corrected_split.append(o.replace(":",""))
            
            option_single = []
            if "original" in corrected_split[0]:
                option_single.append(["version","original"])
            if "txact" in corrected_split[0]:
                option_single.append(["version","txact"])

            for i in range(1,len(corrected_split)):
                value_int = get_value_Int(corrected_split[i])
                key = corrected_split[i].replace(str(value_int),"")
                option_single.append([key,value_int])

            # Store option variables 
            options_version.append(option_single[0][1])
            options_n_workers.append(option_single[1][1])
            options_n_secondary_workers.append(option_single[2][1])
            options_n_reservations.append(option_single[3][1])
            options_n_relations.append(option_single[4][1])
            options_n_queries.append(option_single[5][1])
            options_password_work_factor.append(option_single[6][1])

    # Set columns to be used in dataframes and the variables related to these columns 
    data = {
        "Option": options,
        "Energy Cores": results_cores,
        "Energy Ram": results_ram,
        "Energy Gpu": results_gpu,
        "Energy Pkg": results_pkg,
        "Time (perf) (s)": results_time_perf, 
        "Time (exec) (s)": results_time_exec,
        "Ratio time (%)": results_ratio_time,
        "Power_Cores": results_power_cores,
        "Power_Ram": results_power_ram,
        "Power_Gpu": results_power_gpu,
        "Power_Pkg": results_power_pkg
    }

    data_full = {
        "version": options_version,
        "n-workers": options_n_workers,
        "n-secondary-workers": options_n_secondary_workers,
        "n-reservations": options_n_reservations,
        "n-relations": options_n_relations,
        "n-queries": options_n_queries,
        "password-work-factor": options_password_work_factor,
        "Energy Cores": results_cores,
        "Energy Ram": results_ram,
        "Energy Gpu": results_gpu,
        "Energy Pkg": results_pkg,
        "Time (perf) (s)": results_time_perf, 
        "Time (exec) (s)": results_time_exec,
        "Ratio time (%)": results_ratio_time,
        "Power_Cores": results_power_cores,
        "Power_Ram": results_power_ram,
        "Power_Gpu": results_power_gpu,
        "Power_Pkg": results_power_pkg
    }

    # Created dataframes and store the results in a csv table 
    df_simple = pd.DataFrame(data)
    df_simple.to_csv(path_output+"/"+"Table_simple.csv", index = False, sep=',', encoding='utf-8')

    df_full = pd.DataFrame(data_full)
    df_full.to_csv(path_output+"/"+"Table_full.csv", index = False, sep=',', encoding='utf-8')

    return df_full
        

#----------------------------- Graphs creation ----------------------------------

# Used for creating graphs where y-axis is for Cores, GPU, Ram and Pkg and x-axis is for threads 

def graph_Threads(df,column_name, path_output):
    threads = list(dict.fromkeys(df["n-workers"].tolist())) # Remove duplicates, get all possible threads up to 64 
    
    records = df[["version","n-secondary-workers"]].to_records(index=False) # get a list of version and secondary actors, for instance (original, 0) or (txact, 1),...
    versions = []
    # get individual versions 
    for v in list(records):
        if v not in versions: 
            versions.append(v)

    # Get values of energy consumption based on version, secondary workes and primary workers (threads) 
    for version in versions: 
        results_median = []
        for tr in threads: 
            if column_name in ["Cores","Ram","Gpu","Pkg"]: # Retrieve data, if column name is one of these four  attributes 
                # Get median of energy consuption for one attribute 
                value_median = round(df[(df["n-workers"] == tr) & (df["version"] == version[0]) & (df["n-secondary-workers"] == version[1])]["Energy " + column_name].median(),2)
                results_median.append((tr,value_median))
            else: # If column name doesn't belong to one of these four attributes 
                # Get median of energy consuption for one attribute 
                value_median = round(df[(df["n-workers"] == tr) & (df["version"] == version[0]) & (df["n-secondary-workers"] == version[1])][column_name].median(),2)
                results_median.append((tr,value_median))
        
        # Create graph 

        x = []
        y = []
        # Set values to apply to x and y axis 
        for result in results_median:
            x.append(result[0])
            y.append(result[1])
        
        string = "Using " +version[0] + " actors, s = " + str(version[1])
        plt.plot(x, y, label = string) # Plot values for one version and secondary actors 
    
    # Set title, names of x and y axis based on column name 
    if "Time" not in column_name:
        plt.xlabel('p-workers(threads)')
        # naming the y axis
        if "Power" not in column_name:
            plt.ylabel('Energy (Joules)')
            # giving a title to my graph
            plt.title('Median energy consumption of '+ column_name +' by threads')
        else:
            plt.ylabel('Power (W)')
            # giving a title to my graph
            plt.title('Median power consumption of '+ column_name +' by threads')
        
        
        # show a legend on the plot
        plt.legend()
        if "Power" not in column_name:
            plt.savefig(path_output + "/" + "Output_" + column_name + "/"+"Energy_Threads_"+column_name+".png")
        else:
            plt.savefig(path_output + "/" + "Output_" + column_name + "/"+column_name+"_Threads.png")
      
    else:
        plt.xlabel('p-workers(threads)')
        # naming the y axis
        plt.ylabel('Seconds (s)')
        # giving a title to my graph
        plt.title('Median Time by threads')
        
        # show a legend on the plot
        plt.legend()

        plt.savefig(path_output + "/" + "Output_Time/Time(perf)_Threads.png")
    
    plt.clf()
    #plt.show()


# Create graphs for energy and power with respect to threads for individual version 
def graphs_Power_and_Energy(df, column_name, path_output):
    threads = list(dict.fromkeys(df["n-workers"].tolist())) # Remove duplicates, get individual threads
    
    records = df[["version","n-secondary-workers"]].to_records(index=False)
    versions = []
    # get individual versions 
    for v in list(records):
        if v not in versions: 
            versions.append(v)
    # Get values of energy consumption based on version, secondary workes and perf time 
    for version in versions: 
        results_median = []
        for tr in threads: 
            if "Power" not in column_name: # if in column name, there is no word "Power"
                value_median_energy = round(df[(df["n-workers"] == tr) & (df["version"] == version[0]) & (df["n-secondary-workers"] == version[1])]["Energy " + column_name].median(),2) # Get Energy values and compute median  
                results_median.append((tr,value_median_energy))
            else:
                value_median_power = round(df[(df["n-workers"] == tr) & (df["version"] == version[0]) & (df["n-secondary-workers"] == version[1])][column_name].median(),2) # Get power values and compute median 
                results_median.append((tr,value_median_power))
       
        # Create graphs 

        if "Power" not in column_name: # If Energy 
            x = []
            y = []
            # set values for x and y axis 
            for result in results_median:
                x.append(result[0]) # threads 
                y.append(result[1]) # energy median values 

            string = "Using " +version[0] + " actors, s = " + str(version[1])
            plt.plot(x,y, label = string)

            plt.xlabel('Threads')

            # naming the y axis
            plt.ylabel('Energy (Joules)')
            # giving a title to my graph
            plt.title('Energy(' + column_name+ ') vs #Threads')

            # show a legend on the plot
            plt.legend()

            plt.savefig(path_output + "/" + "Output_" + column_name + "/"+"Energy_Threads " +version[0] + " actors, s = " + str(version[1])+".png")

        else: # If Power 
            x = []
            y = []
            for result in results_median:
                x.append(result[0])
                y.append(result[1])

            string = "Using " +version[0] + " actors, s = " + str(version[1]) # version and secondary actors 
            plt.plot(x,y, label = string)

            plt.xlabel('#Threads')

            # naming the y axis
            plt.ylabel('Power (W)')
            # giving a title to my graph
            plt.title(column_name+' vs #Threads')
        
            # show a legend on the plot
            plt.legend()

            plt.savefig(path_output + "/" + "Output_" + column_name + "/"+column_name+"_Threads " +version[0] + " actors, s = " + str(version[1])+".png")
        plt.clf()

# Clean all folders for storing new data 
def clean(paths):
    for p in paths:
        output_path = p[1]
        try:
            shutil.rmtree(output_path + "/" + "Output_Cores")
            shutil.rmtree(output_path + "/" + "Output_Ram")
            shutil.rmtree(output_path + "/" + "Output_Gpu")
            shutil.rmtree(output_path + "/" + "Output_Pkg")
            shutil.rmtree(output_path + "/" + "Output_Time")
            shutil.rmtree(output_path + "/" + "Output_Power_Cores")
            shutil.rmtree(output_path + "/" + "Output_Power_Ram")
            shutil.rmtree(output_path + "/" + "Output_Power_Gpu")
            shutil.rmtree(output_path + "/" + "Output_Power_Pkg")    

        except:
            pass

        os.mkdir(output_path + "/" + "Output_Cores")
        os.mkdir(output_path + "/" + "Output_Ram")
        os.mkdir(output_path + "/" + "Output_Gpu")
        os.mkdir(output_path + "/" + "Output_Pkg")
        os.mkdir(output_path + "/" + "Output_Time")
        os.mkdir(output_path + "/" + "Output_Power_Cores")
        os.mkdir(output_path + "/" + "Output_Power_Ram")
        os.mkdir(output_path + "/" + "Output_Power_Gpu")
        os.mkdir(output_path + "/" + "Output_Power_Pkg")

def main():
    print("Start")
    paths = paths_generation(pc_paths, experiment_paths,log_files_path,output_path) # get paths 
    clean(paths)
    for tuple_path in paths: 
        df_full = preprocessing(tuple_path)
        graph_Threads(df_full,"Cores",tuple_path[1])
        graph_Threads(df_full,"Ram",tuple_path[1])
        graph_Threads(df_full,"Gpu",tuple_path[1])
        graph_Threads(df_full,"Pkg",tuple_path[1])

        graph_Threads(df_full,"Time (perf) (s)",tuple_path[1])

        graph_Threads(df_full,"Power_Cores",tuple_path[1])
        graph_Threads(df_full,"Power_Ram",tuple_path[1])
        graph_Threads(df_full,"Power_Gpu",tuple_path[1])
        graph_Threads(df_full,"Power_Pkg",tuple_path[1])

        graphs_Power_and_Energy(df_full,"Cores",tuple_path[1])
        graphs_Power_and_Energy(df_full,"Ram",tuple_path[1])
        graphs_Power_and_Energy(df_full,"Gpu",tuple_path[1])
        graphs_Power_and_Energy(df_full,"Pkg",tuple_path[1])

        graphs_Power_and_Energy(df_full,"Power_Cores",tuple_path[1])
        graphs_Power_and_Energy(df_full,"Power_Ram",tuple_path[1])
        graphs_Power_and_Energy(df_full,"Power_Gpu",tuple_path[1])
        graphs_Power_and_Energy(df_full,"Power_Pkg",tuple_path[1])

    print("End")


main()    

