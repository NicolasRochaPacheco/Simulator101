

from simulator.instruction import Instruction


class HEXProcessing:

	def __init__(self):
		
		self.file = None

		self.instructions = {}


	def read_hex_file(self, filepath):

		# Opens file given by filepath
		self.file = open(filepath, 'r')

		# Variable to store last processed address
		last_address = None

		# Iterates over file 
		for line in self.file:

			# Checks if line starts with '@'
			if line.startswith('@'):

				# Process an address line
				last_address = self.__process_address(line)				

			else:

				self.__process_instruction(line, last_address)

		# Returns instructions dictionary
		return self.instructions


	def __process_address(self, line):

		# Gets address from line
		address = int(line.replace('@', ''))

		# Checks if address exists within dictionary
		if address not in self.instructions.keys():

			# Prints address being processed for debug purposes
			print("Processing adress: {}".format(address))

			# Creates the key in instructions dictionary
			self.instructions[address] = None

		else:

			# If an address is duplicated, an error is shown.
			print("ERROR: An address is duplicated.")

		# Returns address
		return address


	def __process_instruction(self, line, address):

		# Removes unwanted line break
		line = line.replace('\n', '')

		# Breaks line into HEX bytes
		hex_bytes = line.split(' ')

		# Checks that bytes are valid
		print("Are instructions valid? {}".format(len(hex_bytes) % 4 == 0))

		# Creates the list in dictionary if needed
		if self.instructions[address] == None:

			self.instructions[address] = []

		# Iterates over bytes and merges them to form instructions
		for indx in range(int(len(hex_bytes)/4)):
			
			# Retrieves and merges bytes to form instructions
			hex_instruction  = hex_bytes[4 * indx + 3]
			hex_instruction += hex_bytes[4 * indx + 2]
			hex_instruction += hex_bytes[4 * indx + 1]
			hex_instruction += hex_bytes[4 * indx + 0]

			# Converts HEX to BIN
			bin_instruction = bin(int(hex_instruction, 16))[2:].zfill(32)

			# Converts binary instruction into object instance
			instruction = Instruction(bin_instruction)
		
			# Adds instruction to dictionary
			self.instructions[address].append(instruction)
		