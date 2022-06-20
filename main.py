
import sys
import os
import numpy
from pareto_random_samples import pareto_random_samples
from poisson_process import poisson_process
from Event import Event
from splay_tree import Node
import queue as Q
from splay_tree import Tree
from check_inputs import check_inputs
from OrderedQueue import OrderedQueue
from LRU_Cache import LRU_Cache
from MRU_Cache import MRU_Cache
from datetime import datetime

#This is the main function in which we pass the parameters as the file we have,requests and the capacity of cache

def main(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity, R_c, R_a, cache_policy):
	round_trip_prop_time = .4 


	now = datetime.now().time()
	timeof_event = poisson_process(lamb,num_requests)
	sizes_file = pareto_random_samples(alpha_s,int(num_files))
	file_qis = pareto_random_samples(alpha_p,num_files)
	pis_file = file_qis / numpy.sum(file_qis)
	now = datetime.now().time()

#Initialize the event list below that will be used to store the events 
	listof_event = []
 
	for time in timeof_event:
		file_id = numpy.random.choice(len(pis_file), 1, True,pis_file)
		file_size = sizes_file[file_id]
		listof_event.append(Event(time, file_size, file_id))

	
	cache = None
	if cache_policy == "MRU":
		cache = MRU_Cache(cache_capacity)
	elif cache_policy == "LRU":
		cache = LRU_Cache(cache_capacity)
	elif cache_policy == "LIFO":
		cache = OrderedQueue(cache_capacity, True)
	else:
		cache = OrderedQueue(cache_capacity, False)

	cache_util = []
	event_next = None
	present_time = 0
	


	for i in range(0,len(listof_event)):
		current_event = listof_event[i]
		
		if i == 0:
			present_time = current_event.arrival_time
		if i == len(listof_event) -1:
			event_next = None
		else:
			event_next = listof_event[i+1]
		if cache.search(current_event.file_id[0]) == -1:
			
			cache.put(current_event.file_id[0], current_event.size[0])
			current_event.finish_time = present_time + round_trip_prop_time + file_size / R_a + file_size / R_c
		else:
			
			current_event.finish_time = present_time + current_event.size / R_c
		if event_next is not None:
			present_time = max(current_event.finish_time, event_next.arrival_time)
		else:
			present_time = current_event.finish_time
			
	mean_turnaround_time = sum((event.finish_time - event.arrival_time) for event in listof_event) / len(listof_event)
	return mean_turnaround_time


if __name__ == "__main__":
	lamb = float(input("Give lambda value: "))
	num_files = int(input("Give the files possible: "))
	alpha_s = float(input("Give alpha_s value > 1: "))
	alpha_p = float(input("Give alpha_p value > 1: "))
	num_requests = int(input("Number of requests to server: "))
	cache_capacity = int(input("Capacity of cache in MB: "))
	R_c = float(input("Cache speed in MB/s: "))
	R_a = float(input("Network speed in MB/s: "))
	iterations = int(input("Number of iterations to simulate with these parameters"))
	try:
		lru_times = 0
		mru_times = 0
		fifo_times = 0
		lifo_times = 0
		for i in range(0,iterations):
			print("Running iteration ", i)
			lru_times += main(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity,R_c, R_a, "LRU")
			mru_times += main(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity,R_c, R_a, "MRU")
			fifo_times += main(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity,R_c, R_a, "FIFO")
			lifo_times += main(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity,R_c, R_a, "LIFO")

		print("Average turnaround time using lru : ", lru_times /iterations)
		print("Average turnaround time using mru : ", mru_times /iterations)
		print("Average turnaround time using lifo : ", lifo_times /iterations)
		print("Average turnaround time using fifo : ", fifo_times /iterations)
	except:
		print("Invalid input given")