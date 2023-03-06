import settings
from datetime import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
import scipy.stats
import os
import progressbar
import csv


json_label_num_users_per_swarm = 'num_users_group1'
json_label_reps = 'num_reps'
json_label_num_active_neighbors_vals_swarm_1 = 'num_active_neighbors_vals_swarm_1'
json_label_num_active_neighbors_times_swarm_1 = 'num_active_neighbors_times_swarm_1'
json_label_num_active_neighbors_vals_swarm_2 = 'num_active_neighbors_vals_swarm_2'
json_label_num_active_neighbors_times_swarm_2 = 'num_active_neighbors_times_swarm_2'

json_label_num_collisions_vals_swarm_1 = 'num_collisions_vals_swarm_1'
json_label_num_collisions_times_swarm_1 = 'num_collisions_times_swarm_1'
json_label_num_collisions_vals_swarm_2 = 'num_collisions_vals_swarm_2'
json_label_num_collisions_times_swarm_2 = 'num_collisions_times_swarm_2'

json_label_mac_delay_vals_1 = 'mac_delays_swarm_1'
json_label_mac_delay_vals_2 = 'mac_delays_swarm_2'
json_label_mac_window_times = 'mac_delays_sliding_window_times'

# from https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array/2566508#2566508
def find_nearest(array, value):
	array = np.asarray(array)
	idx = (np.abs(array - value)).argmin()
	return idx


def calculate_confidence_interval(data, confidence):
	n = len(data)
	m = np.mean(data)
	std_dev = scipy.stats.sem(data)
	h = std_dev * scipy.stats.t.ppf((1 + confidence) / 2, n - 1)
	return [m, m - h, m + h]


def parse(dir, num_reps, num_users_per_swarm, json_filename):	
	# swarm 1
	num_active_neighbors_times_mat_1 = []
	num_active_neighbors_vals_mat_1 = []  

	# swarm 2
	num_active_neighbors_times_mat_2 = []
	num_active_neighbors_vals_mat_2 = []  
	
	avg_collision_times = None
	avg_collision_vals = []

	avg_mac_times = []
	avg_mac_delay_1 = []
	avg_mac_delay_2 = []

	bar_max_i = num_reps
	bar_i = 0
	print('parsing ' + str(bar_max_i) + ' result files')
	bar = progressbar.ProgressBar(max_value=bar_max_i, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()			
	for rep in range(num_reps):		
		try:
			filename = dir + '/#' + str(rep)
			filename_sca = filename + '.sca.csv'
			filename_vec = filename + '.vec.csv'
			results_vec = pd.read_csv(filename_vec)			
			
			tmp_avg_collisions = []
			mean_mac_delay_swarm_1 = []
			mean_mac_delay_swarm_2 = []
			mac_vals_swarm_1 = []
			mac_times_swarm_1 = []
			mac_vals_swarm_2 = []
			mac_times_swarm_2 = []
			max_simulation_time = 0
			for i in range(num_users_per_swarm):
				tmp_avg_collisions.append([])
				mac_vals_swarm_1.append([])
				mac_times_swarm_1.append([])
				mac_vals_swarm_2.append([])
				mac_times_swarm_2.append([])
				# no of neighbors
				num_active_neighbors_results_1 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_num_active_neighbors:vector') & (results_vec.module=='mobility.aircraft_group1[' + str(i) + '].wlan[0].linkLayer')]
				num_active_neighbors_results_2 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_num_active_neighbors:vector') & (results_vec.module=='mobility.aircraft_group2[' + str(i) + '].wlan[0].linkLayer')]				
				num_active_neighbors_times_mat_1.append([float(s) for s in num_active_neighbors_results_1['vectime'].values[0].split(' ')])
				num_active_neighbors_times_mat_2.append([float(s) for s in num_active_neighbors_results_2['vectime'].values[0].split(' ')])
				num_active_neighbors_vals_mat_1.append([float(s) for s in num_active_neighbors_results_1['vecvalue'].values[0].split(' ')])
				num_active_neighbors_vals_mat_2.append([float(s) for s in num_active_neighbors_results_2['vecvalue'].values[0].split(' ')])

				# packet collisions
				collision_results_1 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_dropped_packets_over_last_ten_time_slots:vector') & (results_vec.module=='mobility.aircraft_group1[' + str(i) + '].wlan[0].linkLayer')]
				collision_results_2 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_dropped_packets_over_last_ten_time_slots:vector') & (results_vec.module=='mobility.aircraft_group2[' + str(i) + '].wlan[0].linkLayer')]				
								
				collision_vals_1 = np.array([float(s) for s in collision_results_1['vecvalue'].values[0].split(' ')])
				collision_vals_2 = np.array([float(s) for s in collision_results_2['vecvalue'].values[0].split(' ')])								
				tmp_avg_collisions[-1].append(np.add(collision_vals_1, collision_vals_2))
				if i == 0:
					avg_collision_times = [float(s) for s in collision_results_1['vectime'].values[0].split(' ')]

				# MAC delays
				mac_results_1 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_broadcast_mac_delay:vector') & (results_vec.module=='mobility.aircraft_group1[' + str(i) + '].wlan[0].linkLayer')]				
				mac_vals_swarm_1[-1].extend(np.array([float(s) for s in mac_results_1['vecvalue'].values[0].split(' ')]))
				mac_times_swarm_1[-1] = [float(s) for s in mac_results_1['vectime'].values[0].split(' ')]
				if np.max(mac_times_swarm_1[-1]) > max_simulation_time:
					max_simulation_time = np.max(mac_times_swarm_1[-1])

				mac_results_2 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_broadcast_mac_delay:vector') & (results_vec.module=='mobility.aircraft_group2[' + str(i) + '].wlan[0].linkLayer')]				
				mac_vals_swarm_2[-1].extend(np.array([float(s) for s in mac_results_2['vecvalue'].values[0].split(' ')]))
				mac_times_swarm_2[-1] = [float(s) for s in mac_results_2['vectime'].values[0].split(' ')]
					
			tmp_avg_collisions = np.array(tmp_avg_collisions)
			for t in range(len(tmp_avg_collisions[0][0])):
				avg_collision_vals.append(np.sum(tmp_avg_collisions[:,0,t]))

			# captured MAC delays are saved for each user 
			# now get mean delay over all users in a swarm as sliding window over simulation time
			max_simulation_time = int(max_simulation_time)  # in seconds
			# for each user
			mean_mac_delays_per_user_1 = []
			mean_mac_delays_per_user_2 = []
			for n in range(num_users_per_swarm):
				# swarm 1
				user_mac_times = np.array(mac_times_swarm_1[n])				
				user_mac_vals = np.array(mac_vals_swarm_1[n])
				mean_mac_delays_per_user_1.append([])
				last_i = 0
				for t in range(5, max_simulation_time, 5):					
					# find index closest to this simulation time
					i = find_nearest(user_mac_times, t)
					mean_mac_delays_per_user_1[-1].append(np.mean(user_mac_vals[last_i:i]))
					last_i = i

				# swarm 2
				user_mac_times = np.array(mac_times_swarm_2[n])
				user_mac_vals = np.array(mac_vals_swarm_2[n])
				mean_mac_delays_per_user_2.append([])
				last_i = 0
				for t in range(5, max_simulation_time, 5):
					# find index closest to this simulation time
					i = find_nearest(user_mac_times, t)
					mean_mac_delays_per_user_2[-1].append(np.mean(user_mac_vals[last_i:i]))
					last_i = i
			mean_mac_delays_per_user_1 = np.array(mean_mac_delays_per_user_1)
			mean_mac_delays_per_user_2 = np.array(mean_mac_delays_per_user_2)
			for i in range(len(mean_mac_delays_per_user_1[0])):
				# compute mean at this window over all users
				avg_mac_delay_1.append(np.mean(mean_mac_delays_per_user_1[:,i]))
				avg_mac_delay_2.append(np.mean(mean_mac_delays_per_user_2[:,i]))
			for t in range(5, max_simulation_time, 5):
				avg_mac_times.append(t)

			bar_i += 1
			bar.update(bar_i)
		except FileNotFoundError as err:
			print(err)
	bar.finish()		

	# save to JSON
	json_data = {}	
	json_data[json_label_reps] = num_reps
	json_data[json_label_num_users_per_swarm] = num_users_per_swarm	
	json_data[json_label_num_active_neighbors_times_swarm_1] = np.array(num_active_neighbors_times_mat_1).tolist()
	json_data[json_label_num_active_neighbors_vals_swarm_1] = np.array(num_active_neighbors_vals_mat_1).tolist()
	json_data[json_label_num_active_neighbors_times_swarm_2] = np.array(num_active_neighbors_times_mat_2).tolist()
	json_data[json_label_num_active_neighbors_vals_swarm_2] = np.array(num_active_neighbors_vals_mat_2).tolist()

	json_data[json_label_num_collisions_times_swarm_1] = np.array(avg_collision_times).tolist()
	json_data[json_label_num_collisions_vals_swarm_1] = np.array(avg_collision_vals).tolist()

	json_data[json_label_mac_delay_vals_1] = np.array(avg_mac_delay_1).tolist()
	json_data[json_label_mac_delay_vals_2] = np.array(avg_mac_delay_2).tolist()
	json_data[json_label_mac_window_times] = np.array(avg_mac_times).tolist()
				
	with open(json_filename, 'w') as outfile:
		json.dump(json_data, outfile)
	print("Saved parsed results in '" + json_filename + "'.")    	


def plot(json_filename, graph_filename_active_neighbors, time_slot_duration, graph_filename_delays):
	"""
	Reads 'json_filename' and plots the values to 'graph_filename'.
	"""
	with open(json_filename) as json_file:		
		# load JSON
		json_data = json.load(json_file)	
		num_users_per_swarm = json_data[json_label_num_users_per_swarm]		
		num_reps = np.array(json_data[json_label_reps])		
		num_active_neighbors_times_mat_1 = np.array(json_data[json_label_num_active_neighbors_times_swarm_1])
		num_active_neighbors_vals_mat_1 = np.array(json_data[json_label_num_active_neighbors_vals_swarm_1])
		num_active_neighbors_times_mat_2 = np.array(json_data[json_label_num_active_neighbors_times_swarm_2])
		num_active_neighbors_vals_mat_2 = np.array(json_data[json_label_num_active_neighbors_vals_swarm_2])

		avg_collision_times = np.array(json_data[json_label_num_collisions_times_swarm_1])
		avg_collision_vals = np.array(json_data[json_label_num_collisions_vals_swarm_1]) * 10  # each value is the average no. of packet collisions over the last 10 time slots, so multiplying by 10 is the no. of packet collisions

		avg_mac_delay_1 = np.array(json_data[json_label_mac_delay_vals_1])
		avg_mac_delay_2 = np.array(json_data[json_label_mac_delay_vals_2])
		avg_mac_times = np.array(json_data[json_label_mac_window_times])		

		max_simulation_time = int(np.max(num_active_neighbors_times_mat_1))
		# find average number of neighbors in half-a-second steps until maximum simulation time
		avg_neighbors_1 = np.zeros(max_simulation_time*2)
		avg_neighbors_2 = np.zeros(max_simulation_time*2)
		avg_neighbors_both = np.zeros(max_simulation_time*2)
		times_vec = np.zeros(max_simulation_time*2)
		for i in range(max_simulation_time*2):
			t = 0 + i*0.5
			times_vec[i] = t
			idx_1 = find_nearest(num_active_neighbors_times_mat_1, t)
			avg_neighbors_1[i] = np.mean(num_active_neighbors_vals_mat_1[:, idx_1])
			idx_2 = find_nearest(num_active_neighbors_times_mat_2, t)
			avg_neighbors_2[i] = np.mean(num_active_neighbors_vals_mat_2[:, idx_2])		
			avg_neighbors_both[i] = np.mean([avg_neighbors_1[i], avg_neighbors_2[i]])

		plt.rcParams.update({
			'font.family': 'serif',
			"font.serif": 'Times',
			'font.size': 9,
			'text.usetex': True,
			'pgf.rcfonts': False
		})
		# plot no of neighbors over simulation time
		fig, ax1 = plt.subplots()
		ax1.plot(times_vec, avg_neighbors_both, color='tab:blue', linewidth=.75)
		ax1.tick_params(axis='y', colors='tab:blue')
		ax1.set_ylabel('avg no. of neighbors')
		plt.xlabel('Simulation time $t$ [s]')
		ax2 = ax1.twinx()
		ax2.bar(avg_collision_times, avg_collision_vals, color='tab:orange', width=4.0)
		ax2.set_ylabel('packet drops over last 10 time slots')		
		ax2.tick_params(axis='y', colors='tab:orange')		
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width*2, settings.fig_height*1.12), forward=False)
		fig.savefig(graph_filename_active_neighbors, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_active_neighbors)    
		plt.close()

		# plot average MAC delay over simulation time
		avg_mac_delay_both_swarms = []
		for i in range(len(avg_mac_delay_1)):
			avg_mac_delay_both_swarms.append(np.mean([avg_mac_delay_1[i], avg_mac_delay_2[i]]) * time_slot_duration)
		fig, ax1 = plt.subplots()
		ax1.plot(times_vec, avg_neighbors_both, color='tab:blue', linewidth=.75)
		ax1.tick_params(axis='y', colors='tab:blue')
		ax1.set_ylabel('avg no. of neighbors')
		plt.xlabel('Simulation time $t$ [s]')
		ax2 = ax1.twinx()		
		ax2.plot(avg_mac_times, avg_mac_delay_both_swarms, color='tab:orange', linewidth=.75)
		ax2.set_ylabel('avg MAC delay over last $5s$ [ms]')
		ax2.tick_params(axis='y', colors='tab:orange')		
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width*2, settings.fig_height*1.12), forward=False)
		fig.savefig(graph_filename_delays, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_delays)    
		plt.close()


if __name__ == "__main__":        	
	parser = argparse.ArgumentParser(description='Parse OMNeT++-generated .csv result files and plot them.')
	parser.add_argument('--filename', type=str, help='Base filename for result and graphs files.', default='mobility')
	parser.add_argument('--dir', type=str, help='Directory path that contains the result files.', default='unspecified_directory')
	parser.add_argument('--no_parse', action='store_true', help='Whether *not* to parse result files.')		
	parser.add_argument('--no_plot', action='store_true', help='Whether *not* to plot predictions errors from JSON results.')				
	parser.add_argument('--num_reps', type=int, help='Number of repetitions that should be considered.', default=1)
	parser.add_argument('--num_users_per_swarm', type=int, help='Number of users in either swarm.', default=15)	
	parser.add_argument('--time_slot_duration', type=int, help='Duration of a time slot in milliseconds.', default=24)

	args = parser.parse_args()	
 
	expected_dirs = ['_imgs', '_data']
	for dir in expected_dirs:
		if not os.path.exists(dir):
			os.makedirs(dir)
		
	output_filename_base = args.filename + "-rep" + str(args.num_reps)
	json_filename = "_data/" + output_filename_base + ".json"
	graph_filename_num_active_neighbors = "_imgs/" + output_filename_base + "_num_active_neighbors.pdf"	
	graph_filename_delays = "_imgs/" + output_filename_base + "_delays.pdf"	
	if not args.no_parse:		
		parse(args.dir, args.num_reps, args.num_users_per_swarm, json_filename)
	if not args.no_plot:
		plot(json_filename, graph_filename_num_active_neighbors, args.time_slot_duration, graph_filename_delays) 
    