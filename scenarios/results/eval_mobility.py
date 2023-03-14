import settings
from datetime import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import sub
import argparse
import json
import scipy.stats
import os
import progressbar
import csv
import math
from utils import calculate_confidence_interval


json_label_num_users_per_swarm = 'num_users_group1'
json_label_reps = 'num_reps'
json_label_num_active_neighbors_vals_swarm_1 = 'num_active_neighbors_vals_swarm_1'
json_label_num_active_neighbors_times_swarm_1 = 'num_active_neighbors_times_swarm_1'
json_label_num_active_neighbors_vals_swarm_2 = 'num_active_neighbors_vals_swarm_2'
json_label_num_active_neighbors_times_swarm_2 = 'num_active_neighbors_times_swarm_2'

json_label_num_collisions_vals = 'num_collisions_vals_swarm_1'
json_label_num_collisions_times = 'num_collisions_times_swarm_1'

json_label_mac_delay_vals_1 = 'mac_delays_swarm_1'
json_label_mac_delay_vals_2 = 'mac_delays_swarm_2'
json_label_mac_window_times = 'mac_delays_sliding_window_times'

# from https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array/2566508#2566508
def find_nearest(array, value):
	array = np.asarray(array)
	idx = (np.abs(array - value)).argmin()
	return idx


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
		# append a new list for this repetition
		num_active_neighbors_times_mat_1.append([])
		num_active_neighbors_vals_mat_1.append([])
		num_active_neighbors_times_mat_2.append([])
		num_active_neighbors_vals_mat_2.append([])
		avg_collision_vals.append([])
		avg_mac_delay_1.append([])
		avg_mac_delay_2.append([])
		try:
			filename = dir + '/#' + str(rep)
			filename_sca = filename + '.sca.csv'
			filename_vec = filename + '.vec.csv'
			results_vec = pd.read_csv(filename_vec)			
			
			this_rep_avg_collisions = []			
			this_rep_mac_vals_swarm_1 = []
			this_rep_mac_times_swarm_1 = []
			this_rep_mac_vals_swarm_2 = []
			this_rep_mac_times_swarm_2 = []
			max_simulation_time = 0
			for i in range(num_users_per_swarm):
				this_rep_avg_collisions.append([])
				this_rep_mac_vals_swarm_1.append([])
				this_rep_mac_times_swarm_1.append([])
				this_rep_mac_vals_swarm_2.append([])
				this_rep_mac_times_swarm_2.append([])
				# no of neighbors
				num_active_neighbors_results_1 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_num_active_neighbors:vector') & (results_vec.module=='mobility.aircraft_group1[' + str(i) + '].wlan[0].linkLayer')]
				num_active_neighbors_results_2 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_num_active_neighbors:vector') & (results_vec.module=='mobility.aircraft_group2[' + str(i) + '].wlan[0].linkLayer')]				
				num_active_neighbors_times_mat_1[rep].append([float(s) for s in num_active_neighbors_results_1['vectime'].values[0].split(' ')])
				num_active_neighbors_times_mat_2[rep].append([float(s) for s in num_active_neighbors_results_2['vectime'].values[0].split(' ')])
				num_active_neighbors_vals_mat_1[rep].append([float(s) for s in num_active_neighbors_results_1['vecvalue'].values[0].split(' ')])
				num_active_neighbors_vals_mat_2[rep].append([float(s) for s in num_active_neighbors_results_2['vecvalue'].values[0].split(' ')])

				# packet collisions
				collision_results_1 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_dropped_packets_over_last_ten_time_slots:vector') & (results_vec.module=='mobility.aircraft_group1[' + str(i) + '].wlan[0].linkLayer')]
				collision_results_2 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_dropped_packets_over_last_ten_time_slots:vector') & (results_vec.module=='mobility.aircraft_group2[' + str(i) + '].wlan[0].linkLayer')]				
								
				this_rep_collision_vals_1 = np.array([float(s) for s in collision_results_1['vecvalue'].values[0].split(' ')])
				this_rep_collision_vals_2 = np.array([float(s) for s in collision_results_2['vecvalue'].values[0].split(' ')])								
				this_rep_avg_collisions[-1].append(np.add(this_rep_collision_vals_1, this_rep_collision_vals_2))
				if rep==0 and i==0:
					avg_collision_times = [float(s) for s in collision_results_1['vectime'].values[0].split(' ')]

				# MAC delays
				mac_results_1 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_broadcast_mac_delay:vector') & (results_vec.module=='mobility.aircraft_group1[' + str(i) + '].wlan[0].linkLayer')]				
				this_rep_mac_vals_swarm_1[-1].extend(np.array([float(s) for s in mac_results_1['vecvalue'].values[0].split(' ')]))
				this_rep_mac_times_swarm_1[-1] = [float(s) for s in mac_results_1['vectime'].values[0].split(' ')]
				if np.max(this_rep_mac_times_swarm_1[-1]) > max_simulation_time:
					max_simulation_time = np.max(this_rep_mac_times_swarm_1[-1])

				mac_results_2 = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_broadcast_mac_delay:vector') & (results_vec.module=='mobility.aircraft_group2[' + str(i) + '].wlan[0].linkLayer')]				
				this_rep_mac_vals_swarm_2[-1].extend(np.array([float(s) for s in mac_results_2['vecvalue'].values[0].split(' ')]))
				this_rep_mac_times_swarm_2[-1] = [float(s) for s in mac_results_2['vectime'].values[0].split(' ')]
					
			this_rep_avg_collisions = np.array(this_rep_avg_collisions)
			for t in range(len(this_rep_avg_collisions[0][0])):
				avg_collision_vals[rep].append(np.sum(this_rep_avg_collisions[:,0,t]))

			# captured MAC delays are saved for each user 
			# now get mean delay over all users in a swarm as sliding window over simulation time
			max_simulation_time = int(max_simulation_time)  # in seconds
			# for each user
			mean_mac_delays_per_user_1 = []
			mean_mac_delays_per_user_2 = []
			for n in range(num_users_per_swarm):
				# swarm 1
				user_mac_times = np.array(this_rep_mac_times_swarm_1[n])				
				user_mac_vals = np.array(this_rep_mac_vals_swarm_1[n])
				mean_mac_delays_per_user_1.append([])
				last_i = 0
				for t in range(5, max_simulation_time, 5):					
					# find index closest to this simulation time
					i = find_nearest(user_mac_times, t)
					mean_mac_delays_per_user_1[-1].append(np.mean(user_mac_vals[last_i:i]))
					last_i = i

				# swarm 2
				user_mac_times = np.array(this_rep_mac_times_swarm_2[n])
				user_mac_vals = np.array(this_rep_mac_vals_swarm_2[n])
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
				avg_mac_delay_1[rep].append(np.mean(mean_mac_delays_per_user_1[:,i]))
				avg_mac_delay_2[rep].append(np.mean(mean_mac_delays_per_user_2[:,i]))
			if rep == 0:
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

	json_data[json_label_num_collisions_times] = np.array(avg_collision_times).tolist()
	json_data[json_label_num_collisions_vals] = np.array(avg_collision_vals).tolist()

	json_data[json_label_mac_delay_vals_1] = np.array(avg_mac_delay_1).tolist()
	json_data[json_label_mac_delay_vals_2] = np.array(avg_mac_delay_2).tolist()
	json_data[json_label_mac_window_times] = np.array(avg_mac_times).tolist()
				
	with open(json_filename, 'w') as outfile:
		json.dump(json_data, outfile)
	print("Saved parsed results in '" + json_filename + "'.")  

def get_trajectories(t_max = 9999999):
	trajectories = []
	lines = []
	with open('../mobility_data/mobility_group1.txt') as f:
		lines += f.readlines()

	with open('../mobility_data/mobility_group2.txt') as f:
		lines += f.readlines()

	for ac, l in enumerate(lines):
		path = []
		entries = l.split(' ')
		i = 0
		while i < len(entries):
			t = float(entries[i])
			x = float(entries[i + 1])
			y = float(entries[i + 2])
			z = float(entries[i + 3])
			if t <= t_max:
				path.append({
					'id': f"ac_{ac}",
					't': t,
					'x': x,
					'y': y,
					'z': z
				})

			i += 4

		trajectories.append(path)
	return trajectories

def get_ac_position_at_time(trajectory, time):
	for i in range(1, len(trajectory)):
		if trajectory[i]['t'] >= time:
			prev = trajectory[i-1]
			nxt = trajectory[i]
			x = prev['x'] + (nxt['x']- prev['x'])  * (time - prev['t']) / (nxt['t']- prev['t'])
			y = prev['y'] + (nxt['y']- prev['y'])  * (time - prev['t']) / (nxt['t']- prev['t'])
			z = prev['z'] + (nxt['z']- prev['z'])  * (time - prev['t']) / (nxt['t']- prev['t'])
			return (x,y,z)

def get_topology_at_time(trajectories, t=0, scale = 5/10000):
	x = []
	y = []

	for trajectory in trajectories:
		(xi, yi, _) = get_ac_position_at_time(trajectory, t)
		x.append(xi)
		y.append(yi)

	x = np.array(x)
	y = np.array(y)

	x_range = x.max() - x.min()
	y_range = y.max() - y.min()

	x_center = x.min() + x_range / 2
	y_center = y.min() + y_range / 2

	x = (x-x_center) * scale
	y = (y-y_center) * scale

	return (x, y)


def get_aspect(ax):
    # Total figure size
    figW, figH = ax.get_figure().get_size_inches()
    # Axis size on figure
    _, _, w, h = ax.get_position().bounds
    # Ratio of display units
    disp_ratio = (figH * h) / (figW * w)
    # Ratio of data units
    # Negative over negative because of the order of subtraction
    data_ratio = sub(*ax.get_ylim()) / sub(*ax.get_xlim())

    return disp_ratio / data_ratio  	

def plot_inset(ax, center, t, x=[], y=[], R=0, inset_width = 240):
		inset_height = 7
		aspect = get_aspect(ax)
		ax.plot([center[0] - inset_width/2 , center[0] + inset_width/2, center[0] + inset_width/2, center[0] - inset_width/2, center[0] - inset_width/2],[center[1] - inset_height/2, center[1] - inset_height/2, center[1] + inset_height/2, center[1] + inset_height/2, center[1] - inset_height/2, ], color= '#333', lw=0.7)

		ax.plot([center[0], t],[center[1]- inset_height / 2, -1], color='#333', lw=0.5)
		ax.plot([t, t],[center[1]- inset_height / 2, -1], color='#333', lw=0.5)
		ax.plot([t, t],[center[1]+ inset_height / 2, 30], color='#333', lw=0.5)

		for i in range(len(x)):
			for j in range(len(x)):
				if i!=j:
					x1 = x[i]
					x2 = x[j]
					y1 = y[i]
					y2 = y[j]
					dist = math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
					if(dist <= R):
						ax.plot([center[0] + x1, center[0] + x2],[center[1] + y1 / aspect,center[1] + y2 / aspect], color='#808080', alpha=0.5, lw=0.05)

		ax.scatter(center[0] + np.array(x), center[1] + np.array(y) / aspect, s=0.2, zorder=20, color='#333')


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

		avg_collision_times = np.array(json_data[json_label_num_collisions_times])
		avg_collision_vals = np.array(json_data[json_label_num_collisions_vals])

		max_simulation_time = int(np.max(num_active_neighbors_times_mat_1))
		# find average number of neighbors in half-a-second steps until maximum simulation time
		# no. of active users has shape (num_reps, num_users, time_steps)ev
		# so we'll compute the three-valued confidence interval (mean, minus, plus) for every point in time
		avg_neighbors_1 = np.zeros((3, max_simulation_time*2))
		avg_neighbors_2 = np.zeros((3, max_simulation_time*2))
		avg_neighbors_both = np.zeros((3, max_simulation_time*2))
		times_vec = np.zeros(max_simulation_time*2)
		mean_collisions = np.zeros((3, len(times_vec)))
		last_i_collisions = 0
		# for each point in time
		for i in range(max_simulation_time*2):
			t = 0 + i*0.5
			times_vec[i] = t
			# swarm 1
			# for every rep
			mean_avg_neighbors_per_rep = []
			for rep in range(num_reps):
				# find the index that is closest to the current moment in time t
				idx_1 = find_nearest(num_active_neighbors_times_mat_1[rep, 0], t)
				# compute the mean no. of neighbors for this repetition over all users at this moment in time
				mean_avg_neighbors_per_rep.append(np.mean(num_active_neighbors_vals_mat_1[rep, :, idx_1]))
			avg_neighbors_1[:,i] = calculate_confidence_interval(mean_avg_neighbors_per_rep)
			
			# swarm 2
			# for every rep
			mean_avg_neighbors_per_rep = []
			for rep in range(num_reps):
				# find the index that is closest to the current moment in time t
				idx_2 = find_nearest(num_active_neighbors_times_mat_2[rep, 0], t)
				# compute the mean no. of neighbors for this repetition over all users at this moment in time
				mean_avg_neighbors_per_rep.append(np.mean(num_active_neighbors_vals_mat_2[rep, :, idx_1]))
			avg_neighbors_2[:,i] = calculate_confidence_interval(mean_avg_neighbors_per_rep)

			# mean over both swarms
			avg_neighbors_both[:,i] = np.mean([avg_neighbors_1[:,i], avg_neighbors_2[:,i]])

			# and also for collision values
			id_3 = find_nearest(avg_collision_times, t)
			sum_of_reps = np.zeros(num_reps)
			for rep in range(num_reps):
				sum_of_reps[rep] = np.sum(avg_collision_vals[rep,last_i_collisions:id_3])
			mean_collisions[:,i] = calculate_confidence_interval(sum_of_reps)
			last_i_collisions = id_3

		plt.rcParams.update({
			'font.family': 'serif',
			"font.serif": 'Times',
			'font.size': 9,
			'text.usetex': True,
			'pgf.rcfonts': False
		})

		# plot no of neighbors over simulation time
		fig, ax1 = plt.subplots()
		ax1.plot(times_vec, avg_neighbors_both[0,:], color='tab:blue', linewidth=.75, alpha=1, linestyle=':')
		ax1.fill_between(times_vec, avg_neighbors_both[1,:], avg_neighbors_both[2,:], color='tab:blue', alpha=.5)
		ax1.tick_params(axis='y', colors='tab:blue')
		ax1.set_ylabel('avg no. of neighbors')

		scale = 6/10000
		R = 277800 * scale

		trajectories = get_trajectories()
		t0 = 140
		(x,y) = get_topology_at_time(trajectories, t0, scale)
		inset_center = (180, 9)
		plot_inset(ax1, inset_center, t0, x, y, R, 320)

		t1 = 270.55
		(x,y) = get_topology_at_time(trajectories, t1, scale)
		inset_center = (500, 9)
		plot_inset(ax1, inset_center, t1, x, y, R, 300)

		t2 = 564
		(x,y) = get_topology_at_time(trajectories, t2, scale)
		inset_center = (760, 9)
		plot_inset(ax1, inset_center, t2, x, y, R, 200)


		ax1.set_ylim([-1, 30])
		
		plt.xlabel('Simulation time $t$ [s]')
		ax1.set_xticks([0, t0, 200, t1, 400, t2, 600, 800])
		ax1.set_xticklabels(['0', '$t_0$', '', '$t_1$', '400', '$t_2$', '', '800'])
		# and the no. of dropped packets on a second y-axis
		ax2 = ax1.twinx()
		ax2.plot(times_vec, mean_collisions[0,:], color='tab:orange', linewidth=.75, alpha=1, linestyle=':')
		ax2.fill_between(times_vec, mean_collisions[1,:], mean_collisions[2,:], color='tab:orange', alpha=.5)
		ax2.set_ylabel('sliding window over packet drops')		
		ax2.tick_params(axis='y', colors='tab:orange')		
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width*2, settings.fig_height*1.12), forward=False)
		fig.savefig(graph_filename_active_neighbors, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_active_neighbors)
		plt.close()


		# plot average MAC delay over simulation time
		avg_mac_delay_1 = np.array(json_data[json_label_mac_delay_vals_1])
		avg_mac_delay_2 = np.array(json_data[json_label_mac_delay_vals_2])
		avg_mac_times = np.array(json_data[json_label_mac_window_times])
		# compute confidence interval over all delay values
		avg_mac_delay_both_swarms = np.zeros((3, len(avg_mac_times)))
		for t in range(len(avg_mac_times)):
			ci_1 = calculate_confidence_interval(avg_mac_delay_1[:,t])
			ci_2 = calculate_confidence_interval(avg_mac_delay_2[:,t])
			avg_mac_delay_both_swarms[:,t] = np.mean([ci_1, ci_2], axis=0)

		fig, ax1 = plt.subplots()
		ax1.plot(times_vec, avg_neighbors_both[0,:], color='tab:blue', linewidth=.75, alpha=1, linestyle=':')
		ax1.fill_between(times_vec, avg_neighbors_both[1,:], avg_neighbors_both[2,:], color='tab:blue', alpha=.5)
		ax1.tick_params(axis='y', colors='tab:blue')
		ax1.set_ylabel('avg no. of neighbors')
		plt.xlabel('Simulation time $t$ [s]')
		ax2 = ax1.twinx()		
		ax2.plot(avg_mac_times, avg_mac_delay_both_swarms[0,:] * time_slot_duration, color='tab:orange', linewidth=.75, alpha=1, linestyle='-')
		ax2.fill_between(avg_mac_times, avg_mac_delay_both_swarms[1,:] * time_slot_duration, avg_mac_delay_both_swarms[2,:] * time_slot_duration, color='tab:orange', alpha=.5)
		ax2.set_ylabel('sliding window over MAC delay [ms]', fontsize=7)
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
	graph_filename_num_active_neighbors = "_imgs/" + output_filename_base + "_num_active_neighbors.png"	
	graph_filename_delays = "_imgs/" + output_filename_base + "_delays.png"	
	if not args.no_parse:		
		parse(args.dir, args.num_reps, args.num_users_per_swarm, json_filename)
	if not args.no_plot:
		plot(json_filename, graph_filename_num_active_neighbors, args.time_slot_duration, graph_filename_delays) 
    