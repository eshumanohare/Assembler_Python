input_file = open ("Input", "r")
object_code_file = open ("ObjectCode", "w")

input_file = input_file.read ()

check = 0  # counter for checking if START has appeared or not

LC = 1

random_var_val = 1

opcode_dict = dict (CLA="0000", LAC="0001", SAC="0010", ADD="0011", SUB="0100", BRZ="0101", BRN="0110", BRP="0111",
                    INP="1000", DSP="1001",
                    MUL="1010", DIV="1011", STP="1100")


# dictionary class defined for ease addition of items

class my_dictionary (dict):
	
	def __init__ (self):
		self = dict ()
	
	def add (self, key):
		global random_var_val
		value = format (random_var_val, '08b')
		self [key] = value
		random_var_val += 1
	
	def add_label (self, key, temp_count):
		# global LC
		# print(LC)
		value = format (temp_count, "08b")
		self [key] = value


variable_dict = my_dictionary ()

label_dict = my_dictionary ()


# In the first pass the label and variable dictionaries will be created

def firstpass ():
	global label_dict
	global variable_dict
	global LC
	global check
	
	input_list = input_file.split ("\n")
	
	for items in input_list:
		
		# error for START not given in the start of the program
		l = items.split(" ")
		if "START" != l[0] and check != 1:
			check = 1
			print ("ERROR >> START address not given in the program")
			continue
		
		if items[0:3] == "INP":
			# print(LC)
			val = items.split(" ")
			
			# error for checking if variable name is not same any label name and multiple declaration
			if val [1] in label_dict or val [1] in variable_dict:
				print ("ERROR >> Variable name already used, multiple declaration is not allowed")
				continue
			
			# error - invalid variable name handling according to basic identifier naming rule
			s = val [1]
			if not s [0].isalnum () and s [0] != "_":
				print ("ERROR >> Variable name not well defined according to standard naming convention")
				continue
			
			# error - invalid number of operands given in INP opcode
			if len (val) > 2:
				print ("ERROR >> " + str (len (val) - 2) + " extra operands given for INP opcode")
				continue
			if len (val) == 1:
				print ("ERROR >> Too less operands given for INP opcode")
				continue
			
			variable_dict.add (val [1])
		
		if items [0:3] == "BRN" or items [0:3] == "BRZ" or items [0:3] == "BRP":
			
			val = items.split (" ")
			
			# error - invalid label name handling according to basic identifier naming rule
			s = val [1]
			if not s [0].isalnum () and s [0] != "_":
				print ("ERROR >> Label name not well defined according to standard naming convention")
				continue
			
			# error - invalid number of operands given in the BRP, BRN, BRZ opcode
			if len (val) > 2:
				print ("ERROR >> " + str (len (val) - 2) + " extra operands given for " + str (val [0]) + " opcode")
				continue
			if len (val) == 1:
				print ("ERROR >> Too less operands given for " + str (val [0]) + " opcode")
				continue
			
			if val [1] not in label_dict:  # to check whether the labels are already created or not
				temp_count = 0
				label_check = False
				for temp in input_list:
					temp_count = temp_count + 1
					if (":" in temp):
						label = temp [0:temp.find (":")]
						# print(label)
						if (label == val [1]):
							label_check = True
							label_dict.add_label (val [1], temp_count)
							break
				if (label_check == False):
					print ("ERROR >> Label " + val [1] + " not found")
					exit ()
		
		LC += 1
	
	print (variable_dict)
	print (label_dict)


def secondPass ():
	global LC
	LC = 0
	
	input_list = input_file.split ("\n")
	
	for items in input_list:
		
		if items == "CLA":
			object_code_file.writelines (opcode_dict.get (items) * 3 + "\n")
		
		if items [0:3] == "INP":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + variable_dict.get ((val [1])) + "\n")
		
		if items [0:3] == "LAC":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + variable_dict.get (val [1]) + "\n")
		
		if items [0:3] == "SAC":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + variable_dict.get (val [1]) + "\n")
		
		if items [0:3] == "ADD":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + variable_dict.get (val [1]) + "\n")
		
		if items [0:3] == "SUB":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + variable_dict.get (val [1]) + "\n")
		
		if items [0:3] == "MUL":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + variable_dict.get (val [1]) + "\n")
		
		if items [0:3] == "DIV":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + variable_dict.get (val [1]) + "\n")
		
		if items [0:3] == "BRN":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + label_dict.get (val [1]) + "\n")
		
		if items [0:3] == "BRP":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + label_dict.get (val [1]) + "\n")
		
		if items [0:3] == "BRZ":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + label_dict.get (val [1]) + "\n")
		
		if items [0:3] == "DSP":
			val = items.split (" ")
			object_code_file.writelines (opcode_dict.get (val [0]) + variable_dict.get (val [1]) + "\n")
		
		if items [0:2] in label_dict:
			val = items.split (" ")
			if val [1] == "STP":
				object_code_file.writelines (opcode_dict.get (val [1]) + "0" * 8 + "\n")
				continue
			else:
				object_code_file.writelines (opcode_dict.get (val [1]) + variable_dict.get (val [2]) + "\n")
				continue


# print(input_list)

# print(line, end = "")

firstpass ()
secondPass ()