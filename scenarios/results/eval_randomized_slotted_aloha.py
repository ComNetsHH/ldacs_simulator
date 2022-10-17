from datetime import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
import scipy.stats
import os
import progressbar
import settings


json_label_reps = 'num_reps'
json_label_n_users = 'n_users'
json_label_broadcast_delays = 'broadcast_mac_delays'
json_label_selected_slots = 'broadcast_selected_slots'
json_label_reception_rate = 'broadcast_reception_rate'
json_label_broadcast_delay_vec = 'broadcast_mac_delay_vec'
json_label_broadcast_delay_vec_time = 'broadcast_mac_delay_vec_time'
json_label_broadcast_mean_candidate_slots = 'broadcast_mac_mean_candidate_slots'
json_label_broadcast_selected_slots = 'broadcast_mac_selected_slots'
json_label_collision_rate_mat = 'collision_rate_mat'
json_label_duty_cycle_mat = 'duty_cycle_mat'

def calculate_confidence_interval(data, confidence):
	n = len(data)
	m = np.mean(data)
	std_dev = scipy.stats.sem(data)
	h = std_dev * scipy.stats.t.ppf((1 + confidence) / 2, n - 1)
	return [m, m - h, m + h]


def parse(dir, num_users_vec, num_reps, json_filename):		
	broadcast_delay_mat = np.zeros((len(num_users_vec), num_reps))			
	broadcast_reception_rate_mat = np.zeros((len(num_users_vec), num_reps))	
	collision_rate_mat = np.zeros((len(num_users_vec), num_reps))	
	broadcast_mean_num_candidate_slots_mat = np.zeros((len(num_users_vec), num_reps))
	broadcast_mean_selected_slots_mat = np.zeros((len(num_users_vec), num_reps))
	duty_cycle_mat = np.zeros((len(num_users_vec), num_reps))
	bar_max_i = len(num_users_vec)*num_reps
	bar_i = 0
	print('parsing ' + str(bar_max_i) + ' result files')
	bar = progressbar.ProgressBar(max_value=bar_max_i, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()	
	# for each number of transmitters
	for i in range(len(num_users_vec)):			
		n = num_users_vec[i]				
		# for each repetition
		for rep in range(num_reps):
			try:							
				filename = dir + '/n=' + str(n) + '-#' + str(rep) + '.sca.csv'				
				results = pd.read_csv(filename)				
				# get the total number of transmitted broadcasts
				num_broadcasts = 0
				# and the mean delay per transmitter
				delay_vec = np.zeros(n)
				num_candidate_slots_per_transmitter = np.zeros(n)
				selected_slot_per_transmitter = np.zeros(n)
				duty_cycle_per_transmitter = np.zeros(n)
				for transmitter in range(n):											
					num_broadcasts += int(results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_num_broadcasts_sent:last') & (results.module=='NW_TX_RX.txNodes[' + str(transmitter) + '].wlan[0].linkLayer')].value)					
					delay_vec[transmitter] = results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_broadcast_mac_delay:mean') & (results.module=='NW_TX_RX.txNodes[' + str(transmitter) + '].wlan[0].linkLayer')].value
					num_candidate_slots_per_transmitter[transmitter] = results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_broadcast_candidate_slots:mean') & (results.module=='NW_TX_RX.txNodes[' + str(transmitter) + '].wlan[0].linkLayer')].value					
					selected_slot_per_transmitter[transmitter] = results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_broadcast_selected_candidate_slot:mean') & (results.module=='NW_TX_RX.txNodes[' + str(transmitter) + '].wlan[0].linkLayer')].value											
					duty_cycle_per_transmitter[transmitter] = float(results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_duty_cycle:mean') & (results.module=='NW_TX_RX.txNodes[' + str(transmitter) + '].wlan[0].linkLayer')].value)					
				duty_cycle_mat[i][rep] = np.mean(duty_cycle_per_transmitter)				
				# take the number of received broadcasts at the RX node
				broadcast_reception_rate_mat[i][rep] = int(results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_num_broadcasts_received:last') & (results.module=='NW_TX_RX.rxNode.wlan[0].linkLayer')].value)
				# divide by all broadcasts to get the reception rate
				broadcast_reception_rate_mat[i][rep] /= max(1, num_broadcasts)				
				# take the mean over the mean delays of all transmitters
				broadcast_delay_mat[i][rep] = np.mean(delay_vec)										
				broadcast_mean_num_candidate_slots_mat[i][rep] = np.mean(num_candidate_slots_per_transmitter)										
				broadcast_mean_selected_slots_mat[i][rep] = np.mean(selected_slot_per_transmitter)										
				# get the mean number of collisions
				collision_rate_mat[i][rep] = results[(results.type=='scalar') & (results.name=='mcsotdma_statistic_num_packet_collisions:last') & (results.module=='NW_TX_RX.rxNode.wlan[0].linkLayer')].value / max(1, num_broadcasts)				
				bar_i += 1
				bar.update(bar_i)
			except FileNotFoundError as err:
				print(err)			
	bar.finish()		

	# Save to JSON.
	json_data = {}
	json_data[json_label_n_users] = np.array(num_users_vec).tolist()	
	json_data[json_label_broadcast_mean_candidate_slots] = broadcast_mean_num_candidate_slots_mat.tolist()
	json_data[json_label_broadcast_selected_slots] = broadcast_mean_selected_slots_mat.tolist()	
	json_data[json_label_reps] = num_reps
	json_data[json_label_broadcast_delays] = broadcast_delay_mat.tolist()	
	json_data[json_label_reception_rate] = broadcast_reception_rate_mat.tolist()		
	json_data[json_label_collision_rate_mat] = collision_rate_mat.tolist()
	json_data[json_label_duty_cycle_mat] = duty_cycle_mat.tolist()	
	with open(json_filename, 'w') as outfile:
		json.dump(json_data, outfile)
	print("Saved parsed results in '" + json_filename + "'.")    	


def plot(json_filename, graph_filename_delays, graph_filename_reception, graph_filename_no_of_candidate_slots, graph_filename_selected_slot, graph_filename_collisions, graph_filename_duty_cycle, time_slot_duration, target_reception_rate, target_duty_cycle, delay_max_val):
	"""
	Reads 'json_filename' and plots the values to 'graph_filename'.
	"""
	with open(json_filename) as json_file:
		# Load JSON
		json_data = json.load(json_file)
		num_users_vec = np.array(json_data[json_label_n_users])		
		broadcast_delays_mat = np.array(json_data[json_label_broadcast_delays])
		broadcast_reception_rate_mat = np.array(json_data[json_label_reception_rate])
		broadcast_mean_num_candidate_slots_mat = np.array(json_data[json_label_broadcast_mean_candidate_slots])
		broadcast_mean_selected_slots_mat = np.array(json_data[json_label_broadcast_selected_slots])
		collision_rate_mat = np.array(json_data[json_label_collision_rate_mat])
		duty_cycle_mat = np.array(json_data[json_label_duty_cycle_mat])
		# Calculate confidence intervals
		broadcast_delays_means = np.zeros(len(num_users_vec))
		broadcast_delays_err = np.zeros(len(num_users_vec))			
		broadcast_reception_rate_means = np.zeros(len(num_users_vec))
		broadcast_reception_rate_err = np.zeros(len(num_users_vec))
		broadcast_mean_num_candidate_slots_mat_means = np.zeros(len(num_users_vec))
		broadcast_mean_num_candidate_slots_mat_err = np.zeros(len(num_users_vec))
		broadcast_mean_selected_slots_mat_means = np.zeros(len(num_users_vec))
		broadcast_mean_selected_slots_mat_err = np.zeros(len(num_users_vec))
		collision_rate_mat_means = np.zeros(len(num_users_vec))
		collision_rate_mat_err = np.zeros(len(num_users_vec))
		duty_cycle_mat_means = np.zeros(len(num_users_vec))
		duty_cycle_mat_err = np.zeros(len(num_users_vec))
		for i in range(len(num_users_vec)):				
			broadcast_delays_means[i], _, delay_p = calculate_confidence_interval(broadcast_delays_mat[i,:], confidence=.95)
			broadcast_delays_err[i] = delay_p - broadcast_delays_means[i]	
			broadcast_reception_rate_means[i], _, reception_rate_p = calculate_confidence_interval(broadcast_reception_rate_mat[i,:], confidence=.95)
			broadcast_reception_rate_err[i] = reception_rate_p - broadcast_reception_rate_means[i]
			broadcast_mean_num_candidate_slots_mat_means[i], _, candidate_slots_p = calculate_confidence_interval(broadcast_mean_num_candidate_slots_mat[i,:], confidence=.95)
			broadcast_mean_num_candidate_slots_mat_err[i] = candidate_slots_p - broadcast_mean_num_candidate_slots_mat_means[i]
			broadcast_mean_selected_slots_mat_means[i], _, selected_slots_p = calculate_confidence_interval(broadcast_mean_selected_slots_mat[i,:], confidence=.95)
			broadcast_mean_selected_slots_mat_err[i] = selected_slots_p - broadcast_mean_selected_slots_mat_means[i]
			collision_rate_mat_means[i], _, collision_p = calculate_confidence_interval(collision_rate_mat[i,:], confidence=.95)
			collision_rate_mat_err[i] = collision_p - collision_rate_mat_means[i]
			duty_cycle_mat_means[i], _, duty_cycle_p = calculate_confidence_interval(duty_cycle_mat[i,:], confidence=.95)
			duty_cycle_mat_err[i] = duty_cycle_p - duty_cycle_mat_means[i]
   				
		plt.rcParams.update({
			'font.family': 'serif',
			"font.serif": 'Times',
			'font.size': 9,
			'text.usetex': True,
			'pgf.rcfonts': False
		})
		# 1st graph: delay		
		fig = plt.figure()		
		line = plt.errorbar(num_users_vec, broadcast_delays_means*time_slot_duration, broadcast_delays_err*time_slot_duration, alpha=0.5, fmt='o')
		plt.plot(num_users_vec, broadcast_delays_means*time_slot_duration, linestyle='--', linewidth=.5, color=line[0].get_color(), alpha=.5)		
		if delay_max_val is not None:
			plt.ylim([0, delay_max_val])
		plt.ylabel('Packet delays [ms]')		
		plt.xlabel('Number of transmitters $n$')		
		# plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.5), ncol=3)		
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_delays, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_delays)    
		plt.close()  

		# 2nd graph: reception rate		
		fig = plt.figure()				
		line = plt.errorbar(num_users_vec, broadcast_reception_rate_means*100, broadcast_reception_rate_err*100, alpha=0.5, fmt='o', label='simulation')
		plt.plot(num_users_vec, broadcast_reception_rate_means*100, linestyle='--', linewidth=.5, color=line[0].get_color(), alpha=0.5)
		plt.axhline(y=target_reception_rate, label='target', linestyle='--', linewidth=.75, color = 'k')
		plt.ylabel('Reception rate [\%]')		
		plt.ylim([0, 105])
		plt.xlabel('Number of transmitters $n$')		
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.15), ncol=3)		
		fig.tight_layout()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_reception, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_reception)    
		plt.close()  

		# 3rd graph: no. of candidate slots
		fig = plt.figure()				
		line = plt.errorbar(num_users_vec, broadcast_mean_num_candidate_slots_mat_means, broadcast_mean_num_candidate_slots_mat_err, alpha=0.5, fmt='o')
		plt.plot(num_users_vec, broadcast_mean_num_candidate_slots_mat_means, linestyle='--', linewidth=.5, color=line[0].get_color(), alpha=0.5)
		plt.ylabel('No. of candidate slots')		
		plt.xlabel('Number of transmitters $n$')		
		# plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.5), ncol=3)		
		fig.tight_layout()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_no_of_candidate_slots, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_no_of_candidate_slots)    
		plt.close()  

		# 4th graph: selected slots
		fig = plt.figure()				
		line = plt.errorbar(num_users_vec, broadcast_mean_selected_slots_mat_means, broadcast_mean_selected_slots_mat_err, alpha=0.5, fmt='o')
		plt.plot(num_users_vec, broadcast_mean_selected_slots_mat_means, linestyle='--', linewidth=.5, color=line[0].get_color(), alpha=0.5)
		plt.ylabel('Mean selected slot')		
		plt.xlabel('Number of transmitters $n$')		
		# plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.5), ncol=3)		
		fig.tight_layout()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_selected_slot, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_selected_slot)    
		plt.close()  

		# 5th graph: collision rate
		fig = plt.figure()				
		line = plt.errorbar(num_users_vec, collision_rate_mat_means*100, collision_rate_mat_err*100, alpha=0.5, fmt='o', label='simulation')
		plt.plot(num_users_vec, collision_rate_mat_means*100, linestyle='--', linewidth=.5, color=line[0].get_color(), alpha=0.5)		
		plt.axhline(y=100-target_reception_rate, label='target', linestyle='--', linewidth=.75, color = 'k')
		plt.ylabel('Collision Rate [\%]')		
		plt.ylim([0, 105])
		plt.xlabel('Number of transmitters $n$')		
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.15), ncol=3)		
		fig.tight_layout()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_collisions, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_collisions)    
		plt.close()  

		# 6th graph: duty cycle
		fig = plt.figure()				
		line = plt.errorbar(num_users_vec, duty_cycle_mat_means*100, duty_cycle_mat_err*100, alpha=0.5, fmt='o', label='simulation')
		plt.plot(num_users_vec, duty_cycle_mat_means*100, linestyle='--', linewidth=.5, color=line[0].get_color(), alpha=0.5)		
		plt.axhline(y=target_duty_cycle, label='target', linestyle='--', linewidth=.75, color = 'k')
		plt.ylabel('Duty Cycle [\%]')		
		plt.ylim([0, 105])
		plt.yticks([0, target_duty_cycle, 25, 50, 75, 100])
		plt.xlabel('Number of transmitters $n$')		
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.15), ncol=3)		
		fig.tight_layout()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_duty_cycle, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_duty_cycle)    
		plt.close()  


if __name__ == "__main__":        	
	parser = argparse.ArgumentParser(description='Parse OMNeT++-generated .csv result files and plot them.')
	parser.add_argument('--filename', type=str, help='Base filename for result and graphs files.', default='broadcast_delays')
	parser.add_argument('--dir', type=str, help='Directory path that contains the result files.', default='unspecified_directory')
	parser.add_argument('--no_parse', action='store_true', help='Whether *not* to parse result files.')		
	parser.add_argument('--no_plot', action='store_true', help='Whether *not* to plot predictions errors from JSON results.')			
	parser.add_argument('--n', type=int, nargs='+', help='Number of transmitters.', default=[5])		
	parser.add_argument('--num_reps', type=int, help='Number of repetitions that should be considered.', default=1)
	parser.add_argument('--time_slot_duration', type=int, help='Duration of a time slot in milliseconds.', default=24)	
	parser.add_argument('--target_reception_rate', type=int, help='Target reception rate as an integer between 0 and 100.', default=95)	
	parser.add_argument('--target_duty_cycle', type=int, help='Target duty cycle an integer between 0 and 100.', default=10)	
	parser.add_argument('--delay_max_val', type=int, help='Optionally set to have the same limits on the delay graphs.', default=None)	

	args = parser.parse_args()	
 
	expected_dirs = ['_imgs', '_data']
	for dir in expected_dirs:
		if not os.path.exists(dir):
			os.makedirs(dir)
		
	output_filename_base = args.filename + "_n-" + str(args.n) + "-rep" + str(args.num_reps)
	json_filename = "_data/" + output_filename_base + ".json"
	graph_filename_delays = "_imgs/" + output_filename_base + "_delay.pdf"
	graph_filename_reception = "_imgs/" + output_filename_base + "_reception-rate.pdf"	
	graph_filename_no_of_candidate_slots = "_imgs/" + output_filename_base + "_num-candidate-slots.pdf"
	graph_filename_selected_slot = "_imgs/" + output_filename_base + "_selected-slot.pdf"
	graph_filename_collisions = "_imgs/" + output_filename_base + "_collision-rate.pdf"
	graph_filename_duty_cycle = "_imgs/" + output_filename_base + "_duty-cycle.pdf"
	if not args.no_parse:		
		parse(args.dir, args.n, args.num_reps, json_filename)
	if not args.no_plot:
		plot(json_filename, graph_filename_delays, graph_filename_reception, graph_filename_no_of_candidate_slots, graph_filename_selected_slot, graph_filename_collisions, graph_filename_duty_cycle, args.time_slot_duration, args.target_reception_rate, args.target_duty_cycle, args.delay_max_val) 
    