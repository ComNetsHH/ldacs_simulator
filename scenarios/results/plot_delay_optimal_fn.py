# The L-Band Digital Aeronautical Communications System (LDACS) simulator provides an installation script for the simulator that downloads the other simulator components, defines simulation scenarios and provides result evaluation and graph creation.
# Copyright (C) 2023  Sebastian Lindner, Konrad Fuger, Musab Ahmed Eltayeb Ahmed, Andreas Timm-Giel, Institute of Communication Networks, Hamburg University of Technology, Hamburg, Germany
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path
import csv
import matplotlib.pyplot as plt
import settings
import numpy as np
import math


if __name__ == "__main__":
	delay_fn_filename = 'plot_d.csv'
	derivative_delay_fn_filename = 'plot_derivative_of_d.csv'
	# check that files exist
	if not Path(delay_fn_filename).is_file():
		print(f"CSV file that contains Matlab-generated values of the delay function named {delay_fn_filename} was not found! Have you run 'compute_delay_optimal_fn.m?'")
		exit(-1)
	if not Path(derivative_delay_fn_filename).is_file():
		print(f"CSV file that contains Matlab-generated values of the derivative of the delay function named {derivative_delay_fn_filename} was not found! Have you run 'compute_delay_optimal_fn.m?'")
		exit(-1)
	graph_filename_d = '_imgs/expected_delay.pdf'
	graph_filename_derivative_d = '_imgs/expected_delay_derivative.pdf'

	# parse and plot d(n,q)
	x = None
	y = None
	# read CDF from Matlab output file
	with open(delay_fn_filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		x = np.array([float(s) for s in next(reader)])
		y = np.array([float(s) for s in next(reader)])

		plt.rcParams.update({
			'font.family': 'serif',
			"font.serif": 'Times',
			'font.size': 8,
			'text.usetex': True,
			'pgf.rcfonts': False
		})
		fig, ax = plt.subplots()
		plt.plot(x, y, label='$d($fixed $n,q)$')
		min_index = np.where(y == y.min())[0][0]		
		plt.axvline(x=x[min_index], linestyle='--', color='k', linewidth=.75)
		plt.text(x[min_index] + .025, y.max() - 0.6*y.max(), f'minimum', rotation=90)
		plt.xlabel('target collision probability $q$')
		plt.xticks([0, 0.25, 1.-1./math.exp(1), 1], [0, 0.25, '$1-\\frac{1}{e}$', 1])		
		plt.ylabel('slots')
		ax.set_yticklabels([])
		ax.set_yticks([])
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.25), ncol=1)
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_d, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_d)

	with open(derivative_delay_fn_filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		x = np.array([float(s) for s in next(reader)])
		y = np.array([float(s) for s in next(reader)])

		plt.rcParams.update({
			'font.family': 'serif',
			"font.serif": 'Times',
			'font.size': 8,
			'text.usetex': True,
			'pgf.rcfonts': False
		})
		fig, ax = plt.subplots()
		plt.plot(x, y, label='$\\frac{\\partial{}}{\\partial{q}} d(n,q) = 0$')
		plt.axhline(1.-1./math.exp(1), linestyle='--', color='black', linewidth=.75)
		plt.xlabel('number of neighbors $n$')
		plt.legend(framealpha=0.0, prop={'size': 7}, loc='upper center', bbox_to_anchor=(.5, 1.25), ncol=1)		
		plt.yticks([0.5, 1.-1./math.exp(1)], [0.5, '$1-\\frac{1}{e}$'])		
		fig.tight_layout()
		settings.init()
		fig.set_size_inches((settings.fig_width, settings.fig_height), forward=False)
		fig.savefig(graph_filename_derivative_d, dpi=500, bbox_inches = 'tight', pad_inches = 0.01)		
		print("Graph saved to " + graph_filename_derivative_d)