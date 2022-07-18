from os import listdir
from itertools import islice
import matplotlib.pyplot as plt
from statistics import median
import numpy as np


def extract_time_stamps(file_name):
   
    # a function that opens a time-stamps.txt file and
    # extracts the time stamp on each line. returns a list.


    time_stamps = []
    with open(file_name, "r") as fname:

        lines = fname.readlines()
        for i in lines:
            time_stamps.append(float(i.replace("\n", " ").replace(",",""))) 

   # print(f"time stamp extraction from {file_name} is done!")

    return time_stamps

def create_graph(points, title):
    
    output_location = "graphs/"
#    print(f"The time-stamp list is now {timestamps_list}")
    number_of_threads = [i for i in range(4, 66, 2)]
    number_of_threads.insert(0, 1) 
    plt.figure()
    plt.plot(number_of_threads, points, 'go-', color='black', linewidth=2)
    
#    plt.annotate(f" Original  p = {number_of_threads[0]}, execution time = {points[0]}", (number_of_threads[0], points[0]))
    plt.annotate(f" Original  p = {number_of_threads[0]}, execution time = {points[0]}", (number_of_threads[0], points[0]),  xycoords='data',
            xytext=(0.8, 0.95), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=4),
            horizontalalignment='right', verticalalignment='top',
            )

    shortest_time_thread_index = points.index(min(points))
    plt.annotate(f" shortest time  p = {number_of_threads[shortest_time_thread_index]}, execution time = {min(points)}", (number_of_threads[shortest_time_thread_index], min(points)),  xycoords='data',
            xytext=(0.9, 0.5), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=4, connectionstyle="angle3,angleA=0,angleB=-90"),
            horizontalalignment='right', verticalalignment='bottom')

#   plt.annotate(f"  p = {number_of_threads[3]}, execution time = {points[3]} , ", (number_of_threads[3], points[3]))
    
    plt.xlabel("p-workers (threads)")
    plt.ylabel("Execution time /ms")
    plt.title(f"{title}")
    plt.savefig(f"{output_location}{title}.png")
     
def median_of_all_time_stamps(path):
    
    LIST_OF_FILES = listdir(path) 
    LIST_OF_TIME_STAMPS_LISTS = [] 
    LIST_OF_MEDIAN_TIME_STAMPS = []

    LIST_OF_ORDERED_TIME_STAMPS = []

    for file in LIST_OF_FILES:
       
        
        TEMP_LIST =  extract_time_stamps(path+"/"+file)
        LIST_OF_TIME_STAMPS_LISTS.append(TEMP_LIST)
   
    for TIME_STAMP in range(len(LIST_OF_TIME_STAMPS_LISTS[0])):
        TEMP_TIME_STAMP_LIST = []
        for LIST in LIST_OF_TIME_STAMPS_LISTS:
            TEMP_TIME_STAMP_LIST.append(LIST[TIME_STAMP])
        
        LIST_OF_ORDERED_TIME_STAMPS.append(TEMP_TIME_STAMP_LIST)
    
    for ORDERED_LIST in LIST_OF_ORDERED_TIME_STAMPS:
        LIST_OF_MEDIAN_TIME_STAMPS.append(median(ORDERED_LIST))

    

    return  LIST_OF_MEDIAN_TIME_STAMPS

def calculateSpeedUp(point, list_of_points):

    new_list = []
    for element in list_of_points:
        new_list.append(point/element)
    
    return new_list

def paralellListElementSwap(listOfLists, pos1, pos2):

    for alist in listOfLists:
            
        alist[pos1], alist[pos2] = alist[pos2], alist[pos1]
     
    return listOfLists

if __name__ == "__main__":
    
    path = "execution-times/"
    
    all_paths = [path + i for i in listdir(path)]

    labels = [f"Using tx actors, s = {int(i[6:])}" if i != "original" else i for i in listdir(path)]
    median_time_executions = []
    for item in all_paths:
        median_time_executions.append(median_of_all_time_stamps(item))

    ref_point = median_time_executions[-1][0]
    
    speed_up_lists = [calculateSpeedUp(ref_point, i) for i in median_time_executions]

#    median_time_executions.sort()
#    swapPositions(median_time_executions, -2, -3)
#
#
#
#    labels.sort() 
#    swapPositions(labels, -2, -3)
    
#    newLists = paralellListElementSwap([median_time_executions, speed_up_lists, labels], -2, -3)
#    median_time_executions = newLists[0]
#    speed_up_lists = newLists[1]
#    labels = newLists[2]
#    print(labels)

    number_of_threads = [i for i in range(2, 66, 2)]
    number_of_threads.insert(0, 1)
    plt.figure()
    jet = plt.get_cmap('jet')
    colors = iter(jet(np.linspace(0,1,10)))
    #labels = ["original", "txact s = 1", "txact s = 2", "txact s = 8","txact s = 64"]
    for index,  number_list in enumerate(median_time_executions):
        plt.plot(number_of_threads, number_list, 'go-', color=next(colors),linewidth=1.5, label=labels[index])
    
    plt.legend()
    title = "execution times vacation2 benchmark"
    plt.xlabel("p-workers (threads)")
    plt.ylabel("Execution time /ms")
    plt.title(f"{title}")
    plt.grid(True)
    plt.savefig(f"graphs/{title.replace(' ', '_')}.png")
     
    plt.figure()


    for index, number_list in enumerate(speed_up_lists):
        plt.plot(number_of_threads, number_list, 'go-', color=next(colors),linewidth=1.5, label=labels[index])

    plt.legend()

    title = "speedup vacation2 benchmark"
    plt.xlabel("p-workers (threads)")
    plt.ylabel("speed-up")
    plt.title(f"{title}")

    plt.grid(True)
    plt.savefig(f"graphs/{title.replace(' ', '_')}.png")
    plt.show()


