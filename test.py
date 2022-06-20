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
import matplotlib.pyplot as plt
def test(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity, R_c, R_a):
	round_trip_prop_time = .4 #s
	lfu_rtt = 0
	mru_rtt = 0
	lru_rtt = 0
	
	timeof_event = poisson_process(lamb,num_requests)
	sizesof_file = generate_files(alpha_s,int(num_files))
	file_qis = pareto_random_samples(alpha_p,num_files)
	pis_file = file_qis / numpy.sum(file_qis)
	event_list = []
	for time in timeof_event:
		file_id = numpy.random.choice(len(), 1, True,)
		file_size = sizesof_file[file_id]
		event_list.append(Event(time, file_size, file_id))


	policies = ["MRU", "LRU", "LFU"]
	ret = []
	for policy in policies:
		#reset event loop
		print(policy)
		for event in event_list:
			event.finish_time = None
		cache = None
		hitRate = 0
		presentTime = 0
		ret = []
		if policy == "MRU":
			cache = MRU_Cache(cache_capacity)
		elif policy == "LRU":
			cache = LRU_Cache(cache_capacity)
		elif policy == "FIFO":
			cache = OrderedQueue(cache_capacity, FIFO = True)
		elif policy == "LFU":
			cache = LFUCache(cache_capacity)
		else:
			cache = OrderedQueue(cache_capacity, FIFO = False)
		
		for i in range(0,len(event_list)):
			current_event = event_list[i]
			events_while_processing = 0
		
			if current_event.finish_time == None:
				
				if presentTime < event_list[i].arrival_time:
					presentTime = event_list[i].arrival_time

				#the events which are not present in the cache memory
    
				if cache.search(current_event.file_id[0] == -1):
        
					#adding the event and then determine how much it would take
					
					cache.put(current_event.file_id[0], current_event.size[0])
					processing_time = round_trip_prop_time + current_event.size[0] / R_a + current_event.size[0] / R_c
					current_event.finish_time = presentTime + processing_time
     
					
					
					events_while_processing = 1
					while i + events_while_processing < len(event_list):
         
						#else the event is present in the cache then answer the request directly
      
						if event_list[i + events_while_processing].arrival_time <= current_event.finish_time:
							future_event = event_list[i + events_while_processing]
							if cache.search(future_event.file_id[0]) != -1:
								if future_event.finish_time is None:
									hitRate+= 1
									future_event.finish_time = future_event.arrival_time + future_event.size[0] / R_c								
						events_while_processing += 1
					presentTime += processing_time
		rtt = sum((event.finish_time - event.arrival_time) for event in event_list) / len(event_list)
		if policy == "LFU":
			lfu_rtt = rtt
		elif policy == "MRU":
			mru_rtt = rtt
		else:
			lru_rtt = rtt
		print(rtt)
	
	return (lfu_rtt, mru_rtt, lru_rtt)
if __name__ == "__main__":
	res = input("Type Example or Interactive: ")
	if res == "Example":
		print(test(2, 200, 1.5, 1.5, 5000, 100, 1000, 20))
	
	elif res == "Big Test":
		print("Begin lambda test")
		val_Lfu = []
		mru_vals = []
		val_Lru = []
		
		for i in range(1,10):
			#five test of each
			print("iteration: ",i)
			lfu_count = 0
			mru_count = 0
			lru_count = 0
			default_nw = 10
			for j in range(0,5):
				res = test(1 + i, 200, 1.5, 1.5, 3000, 50, 1000, 20)
				lfu_count += res[0]
				mru_count += res[1]
				lru_count += res[2]
				print(lfu_count)
				print(mru_count)
				print(lru_count)
			lfu_count = lfu_count/5
			mru_count = mru_count/5
			lru_count = lru_count/5
			val_Lfu.append(lfu_count)
			mru_vals.append(mru_count)
			val_Lru.append(lru_count)

		x = [1.5,2,2.5,3,3.5,4,4.5,5,5.5]
		plt.title("alpha_s vs MTT")
		plt.xlabel("alpha_s")
		plt.ylabel("MTT(s)")
		plt.plot(x, val_Lru, label="LRU")
		plt.plot(x,val_Lfu, label="LFU")
		plt.plot(x,mru_vals, label="MRU")
		plt.legend()
		plt.show()

	else:
		try:
			lamb = float(input("Give lambda value: "))
			
			alpha_s = float(input("Type alpha_s value > 1: "))
			
			num_requests = int(input("Number of requests to the server: "))
			
			R_c = float(input("Cache speed in MB/s: "))
			alpha_p = float(input("Type alpha_p value > 1: "))
			R_a = float(input("Network speed in MB/s: "))
			num_files = int(input("Number of files possible: "))
			cache_capacity = int(input("Capacity of cache in MB: "))
			test(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity, alpha_p, alpha_s)
		except:
			print("Invalid input given")
	