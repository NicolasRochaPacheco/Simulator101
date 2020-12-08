#! /usr/bin/python3

import sys
from argparse import ArgumentParser
from simulator.core import SimulatorCore


def main(filepath):

		# Minimal run for simulator
		simulator = SimulatorCore()
		simulator.set_target_file(filepath)
		simulator.run()


# Decent way to start a Python program
if __name__ == '__main__':
	
	# Creates the argument parser for simulator
	parser = ArgumentParser(description="A program to generate golden files for Core101.")

	# Creates the required aruments group
	required_group = parser.add_argument_group("Required arguments")

	# Creates the HEX file argument
	required_group.add_argument(
		"-f",
		"--file", 
		help="File path of HEX file that will be simulated.",
		type=str,
		required=True
	)

	# Parses arguments
	args = parser.parse_args()

	# Starts simulator with given flag
	sys.exit(main(args.file))