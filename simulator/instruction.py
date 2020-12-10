

from simulator.constants import OPCODE_MAJOR_DICT
from simulator.constants import OPCODE_FORMAT_DICT
from simulator.constants import OPCODE_EXEC_UNIT_DICT

from simulator.exceptions import InvalidInstructionError
from simulator.exceptions import NotSupportedInstructionError


class Instruction(object):
	""" Instruction abstract class for simulator.

	Args:
		binary (str): a string with the binary encoding of the instruction.

	Attributes:
		ins_format (str): a character indicating the instruction format based
			on opcode from binary encoding. Possible values are: 'R', 'I', 'S',
			'B', 'U', 'J'.
		rd (int): value of destination register. Possible values range from 0 
			to 31 inclusive or None if not used.
		rs1 (int): value of first source register. Possible values range from 0 
			to 31 inclusive or None if not used.
		rs2 (int): value of second source register. Possible values range from 0 
			to 31 inclusive or None if not used.
		imm (int): value of encoded immediate value. Possible values range from
			-X to +X or None if not used.
		funct3 (int): value encoding major function value. None if not used.
		funct7 (int): value encoding minor function value. None if not used.
		execution_unit (int): value encoding used execution unit for instruction.
			Possible values are: 1 for INT, 2 for BRU or 3 for LSU.
		uop (int): value encoding uOP that will be executed on instruction 
			execution unit. Possible values range from 0 to 15 inclusive.

	"""

	def __init__(self, binary):

		# Checks that instruction is 32 bits long
		if len(binary) != 32:
			raise InvalidInstructionError("Instruction must be 32 bits long")
		
		# Attribute that holds the instruction type
		try:
			self.ins_format = OPCODE_FORMAT_DICT[int(binary[32-7:32], 2)]
		except KeyError:
			raise NotSupportedInstructionError()

		# Sets attributes that holds the registers addresses
		self.rd, self.rs1, self.rs2 = self.__get_registers(binary, self.ins_format)

		# Sets the immediate attribute
		self.imm = self.__get_immediate(binary, self.ins_format)

		# Sets the funct3 and funct7 attributes
		self.funct3, self.funct7 = __get_funct(binary, self.ins_format)

		# Sets the execution unit selection
		self.execution_unit = OPCODE_EXEC_UNIT_DICT[int(binary[32-7:32], 2)]

		# Sets the execution unit uOP
		self.uop = __get_uop()


	def __get_registers(self, binary, ins_format):

		# Intializes registers as None
		rd, rs1, rs2 = None, None, None

		if ins_format == 'R':
			rd  = int(binary[32-11:32-7], 2)
			rs1 = int(binary[32-19:32-15], 2)
			rs2 = int(binary[32-24:32-20], 2)

		elif ins_format == 'I':
			rd  = int(binary[32-11:32-7], 2)
			rs1 = int(binary[32-19:32-15], 2)
		
		elif ins_format == 'S':
			rs1 = int(binary[32-19:32-15], 2)
			rs2 = int(binary[32-24:32-20], 2)
		
		elif ins_format == 'B':
			rs1 = int(binary[32-19:32-15], 2)
			rs2 = int(binary[32-24:32-20], 2)
		
		elif ins_format == 'U':
			rd  = int(binary[32-11:32-7], 2)
		
		elif ins_format == 'J':
			rd  = int(binary[32-12:32-7], 2) 

		return rd, rs1, rs2


	def __get_immediate(self, binary, ins_format):

		immediate = None
		imm_bin = None

		# Retrieves and concatenates binary to form imm value
		if ins_format == 'I':
			imm_bin = binary[0:32-20]

		if ins_format == 'S':
			imm_bin = binary[32-32:32-25] + binary[32-7:32-11]

		if ins_format == 'B':
			imm_bin = binary[0] + binary[32-7] + binary[1:32-25] + binary[32-11:32-8]

		if ins_format == 'U':
			imm_bin = binary[32-24:32-20] + ['0' for i in range(12)]

		if ins_format == 'J':
			imm_bin = binary[0] + binary[32-19:32-12] + binary[32-20] + binary[32-31:32-21] + '0'

		# Checks that immediate value exists
		if imm_bin != None:

			# Sign extends the immediate
			if imm_bin[0] == '0':
				imm_bin = imm_bin.zfill(32)

			else:
				imm_bin = imm_bin.rjust(32, '1')

			# Calculates immediate value
			immediate = int(imm_bin, 2)

		return immediate


	def __get_funct(self, binary, ins_format):

		# Intializes funct3 and funct7 variables with None
		funct3, funct7 = None, None

		# 
		if ins_format in ['R', 'I', 'S', 'B']:
			funct3 = int(binary[32-14:32-12], 2)

		if ins_format in ['R']:
			funct7 = int(binary[32-32:32-25], 2)

		return funct3, funct7


	def __get_uop(self, funct3, funct7, opcode):

		# Initializes uop variable
		uop = None

		major = OPCODE_MAJOR_DICT[opcode]

		# If major opcode is a load
		if major == "LOAD":

			if funct3 == 0:
				uop = 1
			if funct3 == 1:
				uop = 2
			if funct3 == 2:
				uop = 3
			if funct3 == 4:
				uop = 5
			if funct3 == 5:
				uop = 6

		if major == "MISC-MEM":
			uop = 0

		if major == "OP-IMM":

			if funct3 == 0:
				uop = 0 
			if funct3 == 1:
				uop = 15
			if funct3 == 2:
				uop = 10
			if funct3 == 3:
				uop = 11
			if funct3 == 4:
				uop = 4
			if funct3 == 5:
				if funct7 == 0:
					uop = 14
				else:
					uop = 13
			if funct3 == 6:
				uop = 2
			if funct3 == 7:
				uop = 3

		if major == "AUIPC":
			uop = 0

		if major == "STORE":
			
			if funct3 == 0:
				uop = 9
			if funct3 == 1:
				uop = 10
			if funct3 == 2:
				uop = 12

		if major == "OP":

			if funct3 == 0:
				if funct7 == 0:
					uop = 0
				else:
					uop = 1
			if funct3 == 1:
				uop = 15
			if funct3 == 2:
				uop = 10
			if funct3 == 3:
				uop = 11
			if funct3 == 4:
				uop = 4
			if funct3 == 5:
				if funct7 == 0:
					uop = 14
				else:
					uop = 13
			if funct3 == 6:
				uop = 2
			if funct3 == 7:
				uop = 3

		if major == "LUI":
			uop = 9

		if major == "BRANCH":

			if funct3 == 0:
				uop = 0
			if funct3 == 1:
				uop = 1
			if funct3 == 4:
				uop = 2
			if funct3 == 5:
				uop = 3
			if funct3 == 6:
				uop = 6
			if funct3 == 7:
				uop = 7

		if major == "JALR":
			uop = 0

		if major == "JAL":
			uop = 8

		if major == "SYSTEM":
			uop = 9

		return uop
