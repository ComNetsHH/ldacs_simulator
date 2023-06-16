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

import numpy as np
import scipy


def calculate_confidence_interval(data, confidence=.95):
	n = len(data)
	m = np.mean(data)
	std_dev = scipy.stats.sem(data)
	h = std_dev * scipy.stats.t.ppf((1 + confidence) / 2, n - 1)
	return [m, m - h, m + h]