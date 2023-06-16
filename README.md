    The L-Band Digital Aeronautical Communications System (LDACS) simulator provides an installation script for the simulator that downloads the other simulator components, defines simulation scenarios and provides result evaluation and graph creation.
    Copyright (C) 2023  Sebastian Lindner, Konrad Fuger, Musab Ahmed Eltayeb Ahmed, Andreas Timm-Giel, Institute of Communication Networks, Hamburg University of Technology, Hamburg, Germany

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

This repository is part of the L-Band Digital Aeronautical Communications System (LDACS) Air-Air (A/A) mode simulator that implements the proposed Medium Access Control (MAC) protocol "Multi Channel Self-Organized TDMA (MCSOTDMA)".

This repository provides an installation script for the simulator that downloads the other simulator components, defines simulation scenarios and provides result evaluation and graph creation.

# Overview
Hi there!
This is the main repository for all things MCSOTDMA-related.

The simulator is OMNeT++ v5.6.2, together with the inet framework v4.2.5.
All custom code is C++, mostly in libraries.
To track development on these, they are in their own repos.
A wrapper integrates the different components into OMNeT++.
All result evaluation and plotting is done with Python.

# Installation
tl;dr: open `install.sh` or `install_mac.sh` and adjust the number of cores `NUM_CPUS` to use for compiling; then run `./install.sh` or `./install_mac.sh`.

Long version: all simulator components are bundled together into one installation script `install.sh` or `install_mac.sh`. 
Please run it, and pay attention to the output. 
For example, it downloads the OMNeT++ simulator of the right version from GitHub. 
If this download via `wget` doesn't succeed, for example because GitHub's servers are beyond their capacity (you'll get a `503` error), then later parts of the script fail. 
This is a very simple Bash script, so peek inside, it's easy to understand, and there's no error recovery built-in, so please debug using common sense!

# Navigation
## Code
All custom code lives under `omnetpp-5.6.2/workspace/<component>`.
Except `omnetpp-5.6.2/workspace/inet4`, that's the a very slightly modified `inet` framework that comes with the OMNeT++ simulator.
Note that the `omnetpp-5.6.2/workspace` folder is only populated after installation.

## Simulations
All network scenarios live under `scenarios`.
At first, you won't want to touch these files, but to see the nitty and gritty of the simulation setups, this is where you'll find it.

All results are generated from the `scenarios/results` folder.
Please go there and read its readme after installation!