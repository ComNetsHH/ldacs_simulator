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


json_label_reps = 'num_reps'
json_label_n_users = 'n_users'
json_label_beacon_rx_vals = 'beacon_rx_time_vals'
json_label_beacon_rx_times = 'beacon_rx_time_times'

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


def parse(dir, num_users, num_reps, json_filename):
	beacon_rx_times_mat = []
	beacon_rx_vals_mat = []
	bar_max_i = num_reps
	bar_i = 0
	print('parsing ' + str(bar_max_i) + ' result files')
	bar = progressbar.ProgressBar(max_value=bar_max_i, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()			
	for rep in range(num_reps):		
		try:
			filename = dir + '/n=' + str(num_users) + '-#' + str(rep)
			filename_sca = filename + '.sca.csv'
			filename_vec = filename + '.vec.csv'
			results_vec = pd.read_csv(filename_vec)			
			beacon_rx_results = results_vec[(results_vec.type=='vector') & (results_vec.name=='mcsotdma_statistic_first_neighbor_beacon_rx_delay:vector') & (results_vec.module=='NW_TX_RX.rxNode.wlan[0].linkLayer')]			
			beacon_rx_vals = beacon_rx_results['vecvalue']
			beacon_rx_vals = [float(s) for s in beacon_rx_vals.values[0].split(' ')]
			beacon_rx_vals_mat.append(beacon_rx_vals)			
			beacon_rx_times = beacon_rx_results['vectime']
			beacon_rx_times = [float(s) for s in beacon_rx_times.values[0].split(' ')]			
			beacon_rx_times_mat.append(beacon_rx_times)
			bar_i += 1
			bar.update(bar_i)
		except FileNotFoundError as err:
			print(err)
	bar.finish()		

	# save to JSON
	json_data = {}
	json_data[json_label_n_users] = num_users
	json_data[json_label_reps] = num_reps
	for rep in range(num_reps):
		json_data[json_label_beacon_rx_times + '_' + str(rep)] = np.array(beacon_rx_times_mat[rep]).tolist()
		json_data[json_label_beacon_rx_vals + '_' + str(rep)] = np.array(beacon_rx_vals_mat[rep]).tolist()
	with open(json_filename, 'w') as outfile:
		json.dump(json_data, outfile)
	print("Saved parsed results in '" + json_filename + "'.")    	


def plot(json_filename, graph_filename_delays, graph_filename_distribution, graph_filename_comparison, time_slot_duration, sfg_csv_file):
	"""
	Reads 'json_filename' and plots the values to 'graph_filename'.
	"""
	with open(json_filename) as json_file:		
		# load JSON
		json_data = json.load(json_file)
		num_users = np.array(json_data[json_label_n_users])
		num_reps = np.array(json_data[json_label_reps])
		beacon_rx_times_mat = []
		beacon_rx_vals_mat = []
		beacon_rx_mean = []
		for rep in range(num_reps):
			# the lists are of uneven length, because users transmit different numbers of times per simulation repetition
			beacon_rx_times_mat.append(np.array(json_data[json_label_beacon_rx_times + '_' + str(rep)]))
			beacon_rx_vals_mat.append(np.array(json_data[json_label_beacon_rx_vals + '_' + str(rep)]))
			# so we need this awkward mean computation, too
			beacon_rx_mean.append(np.mean(beacon_rx_vals_mat[rep]))
		beacon_rx_mean = np.mean(beacon_rx_mean) * time_slot_duration
   				
		plt.rcParams.update({
			'font.family': 'serif',
			"font.serif": 'Times',
			'font.size': 9,
			'text.usetex': True,
			'pgf.rcfonts': False
		})
		# empirical delay graph
		fig = plt.figure()
		max_y = 0
		for rep in range(num_reps):
			plt.scatter(beacon_rx_times_mat[rep], np.multiply(beacon_rx_vals_mat[rep], time_slot_duration), s=.25, color='k')
			if np.max(np.multiply(beacon_rx_vals_mat[rep], time_slot_duration)) > max_y:
				max_y = np.max(np.multiply(beacon_rx_vals_mat[rep], time_slot_duration))
		plt.axhline(beacon_rx_mean, linestyle='--', color='lightgray', linewidth=1, label='empirical mean')
		plt.yticks([0, int(beacon_rx_mean), (max_y + int(beacon_rx_mean)) / 2 , max_y])
		plt.ylabel('Delay until reception [ms]')
		plt.xlabel('Simulation time $t$ [s]')
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center')
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width, settings.fig_height*1.12), forward=False)
		fig.savefig(graph_filename_delays, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_delays)    
		plt.close()

		# analytical CDF graph
		x = None
		y = None
		# read CDF from Matlab output file
		with open(sfg_csv_file) as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			x = [float(s) for s in next(reader)]
			y = [float(s) for s in next(reader)]
		distribution_mean = np.sum(np.multiply(x, y)) * time_slot_duration  # compute mean from the SFG's distrubtion
		nearest_99_index = find_nearest(np.cumsum(y), 0.99)  # find nearest index to 99% in CDF
		fig = plt.figure()		
		plt.plot(np.multiply(x, time_slot_duration), np.cumsum(y), label='analytical', linestyle='--', color='gray')
		plt.axvline(distribution_mean, linestyle='--', color='gray', linewidth=.5, label='analytical mean')
		plt.axvline(np.multiply(x, time_slot_duration)[nearest_99_index], linestyle='-.', color='gray', linewidth=.5, label='99\%')
		plt.xlabel('Delay $x$ [ms]')
		plt.ylabel('$P(X \leq x)$')
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.25), ncol=2)
		plt.xticks([distribution_mean, np.multiply(x, time_slot_duration)[nearest_99_index], np.max(np.multiply(x, time_slot_duration))])
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width, settings.fig_height*1.12), forward=False)
		fig.savefig(graph_filename_distribution, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_distribution)    
		# comparison with Matlab-generated Signal Flow Graph model output	
				
		all_vals = [value*time_slot_duration for sublist in beacon_rx_vals_mat for value in sublist]  # flat list from repetitions-array
		bin_width = 50
		fig = plt.figure()		
		# compute empirical CDF from simulation data
		plt.plot(np.multiply(x, time_slot_duration), np.cumsum(y), label='analytical', linestyle='--', color='gray')
		plt.axvline(distribution_mean, linestyle='--', color='gray', linewidth=.5, label='analytical mean')
		plt.hist(all_vals, density=True, cumulative=True, histtype='step', color='k', label='empirical', bins=range(0, int(max(all_vals)), bin_width))
		plt.xticks([distribution_mean, np.max(all_vals)])
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='lower center')
		plt.xlabel('Delay $x$ [ms]')
		plt.ylabel('$P(X \leq x)$')
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width, settings.fig_height*1.12), forward=False)
		fig.savefig(graph_filename_comparison, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_comparison)    
		plt.close()


if __name__ == "__main__":        	
	parser = argparse.ArgumentParser(description='Parse OMNeT++-generated .csv result files and plot them.')
	parser.add_argument('--filename', type=str, help='Base filename for result and graphs files.', default='sh_sfg_comparison')
	parser.add_argument('--dir', type=str, help='Directory path that contains the result files.', default='unspecified_directory')
	parser.add_argument('--no_parse', action='store_true', help='Whether *not* to parse result files.')		
	parser.add_argument('--no_plot', action='store_true', help='Whether *not* to plot predictions errors from JSON results.')			
	parser.add_argument('--n', type=int, help='Number of transmitters.', default=5)
	parser.add_argument('--num_reps', type=int, help='Number of repetitions that should be considered.', default=1)
	parser.add_argument('--time_slot_duration', type=int, help='Duration of a time slot in milliseconds.', default=24)
	parser.add_argument('--sfg_csv_file', type=str, help='Filename of Matlab-generated CSV that contains the output of the Signal Flow Grpah (SFG) model.', default='unspecified')	

	args = parser.parse_args()	
 
	expected_dirs = ['_imgs', '_data']
	for dir in expected_dirs:
		if not os.path.exists(dir):
			os.makedirs(dir)
		
	output_filename_base = args.filename + "_n-" + str(args.n) + "-rep" + str(args.num_reps)
	json_filename = "_data/" + output_filename_base + ".json"
	graph_filename_delays = "_imgs/" + output_filename_base + "_delay.pdf"
	graph_filename_distribution = "_imgs/" + output_filename_base + "_dist.pdf"		
	graph_filename_comparison = "_imgs/" + output_filename_base + "_comparison.pdf"		
	if not args.no_parse:		
		parse(args.dir, args.n, args.num_reps, json_filename)
	if not args.no_plot:
		plot(json_filename, graph_filename_delays, graph_filename_distribution, graph_filename_comparison, args.time_slot_duration, args.sfg_csv_file) 
    