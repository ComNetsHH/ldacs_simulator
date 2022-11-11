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


json_label_reps = 'num_reps'
json_label_n_users = 'n_users'
json_label_broadcast_delays = 'broadcast_mac_delays'
json_label_beacon_rx_time_means = 'beacon_rx_time_means'
json_label_beacon_rx_time_err = 'beacon_rx_time_err'
json_label_selected_slots = 'broadcast_selected_slots'
json_label_reception_rate = 'broadcast_reception_rate'
json_label_broadcast_delay_vec = 'broadcast_mac_delay_vec'
json_label_broadcast_delay_vec_time = 'broadcast_mac_delay_vec_time'
json_label_broadcast_mean_candidate_slots = 'broadcast_mac_mean_candidate_slots'
json_label_broadcast_selected_slots = 'broadcast_mac_selected_slots'
json_label_collision_rate_mat = 'collision_rate_mat'

def calculate_confidence_interval(data, confidence):
	n = len(data)
	m = np.mean(data)
	std_dev = scipy.stats.sem(data)
	h = std_dev * scipy.stats.t.ppf((1 + confidence) / 2, n - 1)
	return [m, m - h, m + h]


def parse(dirs, num_users_vec, num_reps, json_filename):		
	broadcast_delay_mat = np.zeros((len(dirs), len(num_users_vec), num_reps))
	broadcast_reception_rate_mat = np.zeros((len(dirs), len(num_users_vec), num_reps))
	avg_beacon_rx_mat_means = np.zeros((len(dirs), len(num_users_vec)))			
	avg_beacon_rx_mat_err = np.zeros((len(dirs), len(num_users_vec)))			
	bar_max_i = len(dirs)*len(num_users_vec)*num_reps
	bar_i = 0
	print('parsing ' + str(bar_max_i) + ' result files')
	bar = progressbar.ProgressBar(max_value=bar_max_i, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()	
	for j in range(len(dirs)):
		dir = dirs[j]
		# for each number of transmitters
		for i in range(len(num_users_vec)):			
			n = num_users_vec[i]				
			beacon_rx_time_mat = np.zeros(num_reps)
			# for each repetition
			for rep in range(num_reps):
				try:							
					filename = dir + '/n=' + str(n) + '-#' + str(rep) + '.sca.csv'				
					results = pd.read_csv(filename)				
					# get the total number of transmitted broadcasts
					num_broadcasts = 0
					# and the mean delay per transmitter
					delay_vec = np.zeros(n)					
					for user in range(n):											
						num_broadcasts += int(results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_num_broadcasts_sent:last') & (results.module=='NW_TX_RX.txNodes[' + str(user) + '].wlan[0].linkLayer')].value)					
						delay_vec[user] = results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_broadcast_mac_delay:mean') & (results.module=='NW_TX_RX.txNodes[' + str(user) + '].wlan[0].linkLayer')].value												
					beacon_rx_time_mat[rep] = results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_first_neighbor_beacon_rx_delay:mean') & (results.module=='NW_TX_RX.rxNode.wlan[0].linkLayer')].value
					# take the number of received broadcasts at the RX node
					broadcast_reception_rate_mat[j][i][rep] = int(results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_num_broadcasts_received:last') & (results.module=='NW_TX_RX.rxNode.wlan[0].linkLayer')].value)
					# divide by all broadcasts to get the reception rate
					broadcast_reception_rate_mat[j][i][rep] /= max(1, num_broadcasts)				
					# take the mean over the mean delays of all transmitters
					broadcast_delay_mat[j][i][rep] = np.mean(delay_vec)																				
					bar_i += 1
					bar.update(bar_i)
				except FileNotFoundError as err:
					print(err)			
			avg_beacon_rx_mat_means[j,i], _, plus = calculate_confidence_interval(beacon_rx_time_mat, confidence=.95)												
			avg_beacon_rx_mat_err[j,i] = plus - avg_beacon_rx_mat_means[j,i]
	bar.finish()		

	# Save to JSON.
	json_data = {}
	json_data[json_label_n_users] = np.array(num_users_vec).tolist()		
	json_data[json_label_reps] = num_reps
	json_data[json_label_broadcast_delays] = broadcast_delay_mat.tolist()	
	json_data[json_label_beacon_rx_time_means] = avg_beacon_rx_mat_means.tolist()		
	json_data[json_label_beacon_rx_time_err] = avg_beacon_rx_mat_err.tolist()		
	json_data[json_label_reception_rate] = broadcast_reception_rate_mat.tolist()			
	with open(json_filename, 'w') as outfile:
		json.dump(json_data, outfile)
	print("Saved parsed results in '" + json_filename + "'.")    	


def plot(json_filename, graph_filename_delays, graph_filename_reception, time_slot_duration, target_reception_rates, ylim1, ylim2):
	"""
	Reads 'json_filename' and plots the values to 'graph_filename'.
	"""
	with open(json_filename) as json_file:
		n = len(target_reception_rates)		
		# Load JSON
		json_data = json.load(json_file)
		num_users_vec = np.array(json_data[json_label_n_users])		
		broadcast_delays_mat = np.array(json_data[json_label_broadcast_delays])
		broadcast_reception_rate_mat = np.array(json_data[json_label_reception_rate])		
		avg_beacon_rx_mat_means = np.array(json_data[json_label_beacon_rx_time_means])
		avg_beacon_rx_mat_err = np.array(json_data[json_label_beacon_rx_time_err])		
		# Calculate confidence intervals
		broadcast_delays_means = np.zeros((n, len(num_users_vec)))
		broadcast_delays_err = np.zeros((n, len(num_users_vec)))
		broadcast_reception_rate_means = np.zeros((n, len(num_users_vec)))
		broadcast_reception_rate_err = np.zeros((n, len(num_users_vec)))			
		for j in range(len(target_reception_rates)):
			for i in range(len(num_users_vec)):				
				broadcast_delays_means[j,i], _, delay_p = calculate_confidence_interval(broadcast_delays_mat[j,i,:], confidence=.95)
				broadcast_delays_err[j,i] = delay_p - broadcast_delays_means[j,i]	
				broadcast_reception_rate_means[j,i], _, reception_rate_p = calculate_confidence_interval(broadcast_reception_rate_mat[j,i,:], confidence=.95)
				broadcast_reception_rate_err[j,i] = reception_rate_p - broadcast_reception_rate_means[j,i]						
   				
		plt.rcParams.update({
			'font.family': 'serif',
			"font.serif": 'Times',
			'font.size': 9,
			'text.usetex': True,
			'pgf.rcfonts': False
		})
		# 1st graph: delay		
		fig = plt.figure()				
		colors = ['tab:purple', 'tab:brown', 'tab:cyan', 'tab:olive']
		# two fake data points to add entries to the legend
		line = plt.errorbar(min(num_users_vec), 0, 0, label='MAC Delay', color='k', fmt='o', alpha=.5)
		line.remove()
		line = plt.errorbar(min(num_users_vec), 0, 0, label='E2E Delay', color='k', fmt='x', alpha=.5)
		line.remove()
		for j in range(n):
			line = plt.errorbar(num_users_vec, broadcast_delays_means[j]*time_slot_duration, broadcast_delays_err[j]*time_slot_duration, alpha=0.75, fmt='o', color=colors[j])			
			plt.plot(num_users_vec, broadcast_delays_means[j]*time_slot_duration, linestyle='--', linewidth=1, color=line[0].get_color(), alpha=0.75, label=('$q=' + str((100-target_reception_rates[j])/100) + '$' if target_reception_rates[j] != 37 else '$q=1-\\frac{1}{e}$'))							
		for j in range(n):
			line = plt.errorbar(num_users_vec, avg_beacon_rx_mat_means[j]*time_slot_duration, avg_beacon_rx_mat_err[j]*time_slot_duration, alpha=0.75, fmt='x', color=colors[j])
			plt.plot(num_users_vec, avg_beacon_rx_mat_means[j]*time_slot_duration, linestyle=':', linewidth=1, color=line[0].get_color(), alpha=.75)		
		plt.ylabel('Delays [ms]')				
		plt.xlabel('Number of users $n$')		
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.4, 1.4), ncol=3, columnspacing=0.5)				
		plt.yscale('log')		
		plt.gca().yaxis.grid(True)
		plt.gca().grid(which='major', alpha=.0)
		plt.gca().grid(which='minor', alpha=.5, linewidth=.25, linestyle='-')		
		if ylim1 is not None and ylim2 is not None:
			plt.ylim([ylim1, ylim2])
		plt.xticks(num_users_vec)	
		plt.axhline(y=10**3, color='gray', linestyle='--', alpha=0.75, linewidth=.5)
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_delays, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_delays)    
		plt.close()  

		# 2nd graph: reception rate		
		fig = plt.figure()				
		for j in range(n):			
			line = plt.errorbar(num_users_vec, broadcast_reception_rate_means[j]*100, broadcast_reception_rate_err[j]*100, alpha=0.75, fmt='o', label='$q=' + str((100-target_reception_rates[j])/100) + '$', color=colors[j])
			plt.plot(num_users_vec, broadcast_reception_rate_means[j]*100, linestyle='--', linewidth=.5, color=line[0].get_color(), alpha=0.75)
			plt.axhline(y=target_reception_rates[j], linestyle='--', linewidth=.5, color=line[0].get_color(), alpha=0.75)
		plt.ylabel('Reception rate [\%]')				
		plt.yticks(target_reception_rates + [0])
		plt.xticks(num_users_vec)	
		plt.xlabel('Number of users $n$')				
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.35), ncol=2)		
		plt.ylim([0, 100])
		fig.tight_layout()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_reception, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_reception)    
		plt.close()  


if __name__ == "__main__":        	
	parser = argparse.ArgumentParser(description='Parse OMNeT++-generated .csv result files and plot them.')
	parser.add_argument('--filename', type=str, help='Base filename for result and graphs files.', default='randomized_aloha_aggregate')
	parser.add_argument('--dirs', type=str, nargs='+', help='Directory path that contains the result files.', default=['unspecified_directory'])
	parser.add_argument('--no_parse', action='store_true', help='Whether *not* to parse result files.')		
	parser.add_argument('--no_plot', action='store_true', help='Whether *not* to plot predictions errors from JSON results.')			
	parser.add_argument('--n', type=int, nargs='+', help='Number of transmitters.', default=[5])		
	parser.add_argument('--num_reps', type=int, help='Number of repetitions that should be considered.', default=1)
	parser.add_argument('--time_slot_duration', type=int, help='Duration of a time slot in milliseconds.', default=24)	
	parser.add_argument('--target_reception_rates', nargs='+', type=int, help='Target reception rate as an integer between 0 and 100.', default=[95])	
	parser.add_argument('--ylim1', type=int, help='Minimum y-limit for delay plots.', default=None)	
	parser.add_argument('--ylim2', type=int, help='Maximum y-limit for delay plots.', default=None)	

	args = parser.parse_args()	

	if ((args.ylim1 is not None and args.ylim2 is None) or (args.ylim2 is not None and args.ylim1 is None)):
		raise RuntimeError('If you set one ylim, you have to set the other, too!')
		exit(1)
 
	expected_dirs = ['_imgs', '_data']
	for dir in expected_dirs:
		if not os.path.exists(dir):
			os.makedirs(dir)
		
	output_filename_base = args.filename + "_n-" + str(args.n) + "-rep" + str(args.num_reps)
	json_filename = "_data/" + output_filename_base + ".json"
	graph_filename_delays = "_imgs/" + output_filename_base + "_delay.pdf"
	graph_filename_reception = "_imgs/" + output_filename_base + "_reception-rate.pdf"		
	if not args.no_parse:		
		parse(args.dirs, args.n, args.num_reps, json_filename)
	if not args.no_plot:
		plot(json_filename, graph_filename_delays, graph_filename_reception, args.time_slot_duration, args.target_reception_rates, args.ylim1, args.ylim2) 
    