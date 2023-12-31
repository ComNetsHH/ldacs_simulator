[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10073534.svg)](https://doi.org/10.5281/zenodo.10073534)

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
tl;dr: install `cppunit` (for unit testing) and `pipenv` (for Python-based graph creation) on your system, open `install.sh` and adjust the number of cores `NUM_CPUS` to use for compiling; then run `./install.sh` if you're on Linux or `./install.sh mac` if you're on Mac.

Long version: all simulator components are bundled together into one installation script `install.sh`.
By passing `mac` as an argument to the install script, it downloads the Mac version of the OMNeT++ simulator instead of the Linux version; this is the only difference between Linux and Mac versions of this simulator.
Please run it, and pay attention to the output. 
For example, it downloads the OMNeT++ simulator of the right version from GitHub. 
If this download via `wget` doesn't succeed, for example because GitHub's servers are beyond their capacity (you'll get a `503` error), then later parts of the script fail. 
This is a very simple Bash script, so peek inside, it's easy to understand, and there's no error recovery built-in, so please debug using common sense!
Also `cppunit` is used for unit testing, so please install this, it is a rather common package and should be available through your package manager.

Result parsing and graph generation is done using Python in respective scripts in `scenarios/results/`.
The packages that are required for this are installed in local `pipenv` environments, so make sure that you have `pipenv` available on your system!

## Debug mode
By default, the simulator is compiled in release mode so that simulations run faster.
To compile in debug mode, respective lines are commented-out in the `install.sh`.
Comment them in if you need debug mode.

If you get errors, chances are high that some component is still in release mode: every LDACS simulator component, the OMNeT++ simulator itself and the inet framework must *all* be in debug mode.

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

# Simulator Components
The LDACS MCSOTDMA Simulator is composed of the following parts, which the `install.sh` downloads:

## The OMNeT++ Simulator
v5.6.2 is downloaded from [GitHub.com](https://github.com/omnetpp/omnetpp/releases).

## The INET Framework
v4.2.5 in a slightly modified version is downloaded from [GitHub.com](https://github.com/eltayebmusab/inet).

## The glue Library
v1.1 is downloaded from [Zenodo.org](https://zenodo.org/record/10073046).

## The RLC Library
v1.1 is downloaded from [Zenodo.org](https://zenodo.org/record/10073044).

## The ARQ Library
v1.1 is downloaded from [Zenodo.org](https://zenodo.org/record/10073043).

## The MCSOTDMA Library
v1.0 is downloaded from [Zenodo.org](https://zenodo.org/record/8082927).

## The Channel Model
v1.0 is downloaded from [Zenodo.org](https://zenodo.org/record/8082925).

## The Trace-Based App
v1.0 is downloaded from [Zenodo.org](https://zenodo.org/record/8082929).

## The Wrapper Library
v1.1 is downloaded from [Zenodo.org](https://zenodo.org/record/10073049).

## The modified GPSR Protocol
v1.0 is downloaded from [Zenodo.org](https://zenodo.org/record/8082919).
