#this function runs all four schemes on the same generated events

import sys
import os
import numpy
from pareto_random_samples import pareto_random_samples
from poisson_process import poisson_process
from Event import Event
import queue as Q
from check_inputs import check_inputs
from LRU_Cache import LRU_Cache
from MRU_Cache import MRU_Cache
from OrderedQueue import OrderedQueue
from datetime import datetime
import collections
import numpy as np
from generate_files import generate_files
from LFUCache import LFUCache

def test_with_same_parameters(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity, R_c, R_a):
	rtpt = .1 #s

	timeof_event = poisson_process(lamb,num_requests)
	file_qis = pareto_random_samples(alpha_p,num_files)
	sizeof_file = generate_files(alpha_s,int(num_files))
	pis_file = file_qis / numpy.sum(file_qis)
 
	listof_event = []
	for time in timeof_event:
		id_file = numpy.random.choice(len(pis_file), 1, True,pis_file)
		file_size = sizeof_file[id_file]
		listof_event.append(Event(time, file_size, id_file))

	schemes = ["MRU", "LRU", "FIFO", "LIFO"]
	ret = []
	for cache_policy in schemes:

		
		for event in listof_event:
			event.finish_time = None

		cache_hit_rate = 0
		if cache_policy == "MRU":
			cache = MRU_Cache(cache_capacity)
		elif cache_policy == "LRU":
			cache = LRU_Cache(cache_capacity)
		elif cache_policy == "LIFO":
			cache = OrderedQueue(cache_capacity, True)
		elif cache_policy == "LFU":
			cache = LFUCache(cache_capacity)
		else:
			cache = OrderedQueue(cache_capacity, False)

		cache_util = []
		current_time = 0
		next_event = None
		
		for i in range(0,len(listof_event)):
			current_event = listof_event[i]
			
			events_while_processing = 0

			
			if current_event.finish_time == None:
				
    
				if current_time < listof_event[i].arrival_time:
					current_time = listof_event[i].arrival_time
					

				#Same function as the other test case where we check if the event is present in the cache or not
				#and carry out the fucntion accordingly

    
				if cache.search(current_event.id_file[0] == -1):

					
					cache.put(current_event.id_file[0], current_event.size[0])
					processing_time = rtpt + current_event.size[0] / R_a + current_event.size[0] / R_c
					current_event.finish_time = current_time + processing_time

				
    
					while listof_event[i + 1 + events_while_processing].arrival_time < current_event.finish_time:
					
     
						if i + 1 + events_while_processing < len(listof_event):
							if cache.search(listof_event[i + 1 + events_while_processing].id_file[0] != -1):
								cached_event = listof_event[i + 1 + events_while_processing]
								cached_event.finish_time = cached_event.arrival_time + cached_event.size[0] / R_c
								cache_hit_rate += 1
							events_while_processing += 1

					
					current_time += processing_time


		ret.append((cache_policy,sum((event.finish_time - event.arrival_time) for event in listof_event) / len(listof_event), cache_hit_rate/len(listof_event) ))
	return ret
if __name__ == "__main__":
	print(test_with_same_parameters(2,10,5,1.2,50,50,100,5))