#!/bin/bash

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

sbatch s_broadcast-voice.sh
sbatch s_mac-aloha.sh
sbatch s_mac-mcsotdma-05-slotadv.sh
sbatch s_mac-mcsotdma-05.sh
sbatch s_mac-mcsotdma-75-slotadv.sh
sbatch s_mac-mcsotdma-75.sh
sbatch s_mac-mcsotdma-95-slotadv.sh
sbatch s_mac-mcsotdma-95.sh
sbatch s_mac-mcsotdma-opt-slotadv.sh
sbatch s_mac-mcsotdma-opt.sh
sbatch s_mac-sotdma.sh
sbatch s_pp-link-estbl.sh
sbatch s_pp-voice.sh
