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


json_label_unicast_delay_vec = 'unicast_mac_delay_vec'
json_label_unicast_delay_vec_time = 'unicast_mac_delay_vec_time'

def calculate_confidence_interval(data, confidence):
	n = len(data)
	m = np.mean(data)
	std_dev = scipy.stats.sem(data)
	h = std_dev * scipy.stats.t.ppf((1 + confidence) / 2, n - 1)
	return [m, m - h, m + h]

def parse(dir, json_filename):			
	delay_mat = None
	delay_time = None
	bar_max_i = 1
	bar_i = 0
	print('parsing ' + str(bar_max_i) + ' result files')
	bar = progressbar.ProgressBar(max_value=bar_max_i, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()				
	try:				
		filename = dir + '/n=1-#0.vec.csv'
		results = pd.read_csv(filename)
		delay_mat = results[(results.type=='vector') & (results.name=='mcsotdma_statistic_unicast_mac_delay:vector') & (results.module=='NW_LINK_ESTABLISHMENT.txNode[0].wlan[0].linkLayer')].vecvalue.tolist()			
		delay_time = results[(results.type=='vector') & (results.name=='mcsotdma_statistic_unicast_mac_delay:vector') & (results.module=='NW_LINK_ESTABLISHMENT.txNode[0].wlan[0].linkLayer')].vectime.tolist()
		delay_mat = [float(val) for val in delay_mat[0].split(' ')]		
		delay_time = [float(val) for val in delay_time[0].split(' ')]					
		bar_i += 1
		bar.update(bar_i)
	except FileNotFoundError as err:
		print(err)			
	bar.finish()	

	# Save to JSON.
	json_data = {}	
	json_data[json_label_unicast_delay_vec] = delay_mat
	json_data[json_label_unicast_delay_vec_time] = delay_time
	with open(json_filename, 'w') as outfile:
		json.dump(json_data, outfile)
	print("Saved parsed results in '" + json_filename + "'.")    	


def plot(json_filename, graph_filename, time_slot_duration):
	"""
	Reads 'json_filename' and plots the values to 'graph_filename'.
	"""
	with open(json_filename) as json_file:
		# Load JSON
		json_data = json.load(json_file)		
		delay_mat = np.array(json_data[json_label_unicast_delay_vec])		
		delay_time = np.array(json_data[json_label_unicast_delay_vec_time])		
   				
		plt.rcParams.update({
			'font.family': 'serif',
			"font.serif": 'Times',
			'font.size': 9,
			'text.usetex': True,
			'pgf.rcfonts': False
		})
		fig = plt.figure()						
		plt.scatter(delay_time, delay_mat*time_slot_duration, alpha=.75)		
		plt.axhline(max(set(delay_mat), key=list(delay_mat).count)*time_slot_duration, color='k', linestyle='--', linewidth=0.75)
		plt.yticks([max(set(delay_mat), key=list(delay_mat).count)*time_slot_duration, np.max(delay_mat)*time_slot_duration/2, np.max(delay_mat)*time_slot_duration])
		plt.xlabel('Simulation Time [s]')
		plt.ylabel('Delay [ms]')		
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename)    
		plt.close()  


if __name__ == "__main__":        	
	parser = argparse.ArgumentParser(description='Parse OMNeT++-generated .csv result files and plot them.')
	parser.add_argument('--filename', type=str, help='Base filename for result and graphs files.', default='pp_voice')
	parser.add_argument('--dir', type=str, help='Directory path that contains the result files.', default='unspecified_directory')
	parser.add_argument('--no_parse', action='store_true', help='Whether *not* to parse result files.')		
	parser.add_argument('--no_plot', action='store_true', help='Whether *not* to plot predictions errors from JSON results.')					
	parser.add_argument('--time_slot_duration', type=float, help='Time slot duration.', default=24)

	args = parser.parse_args()	
 
	expected_dirs = ['_imgs', '_data']
	for dir in expected_dirs:
		if not os.path.exists(dir):
			os.makedirs(dir)
		
	output_filename_base = args.filename
	json_filename = "_data/" + output_filename_base + ".json"
	graph_filename = "_imgs/" + output_filename_base + ".pdf"		
	if not args.no_parse:		
		parse(args.dir, json_filename)
	if not args.no_plot:
		plot(json_filename, graph_filename, args.time_slot_duration) 
    