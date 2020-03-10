input_file = open("Input", "r")
object_code_file = open("ObjectCode", "w")

input_file = input_file.read()

LC = 1

random_var_val = 1

opcode_dict = dict (CLA= "0000", LAC= "0001", SAC= "0010", ADD= "0011", SUB= "0100", BRZ= "0101", BRN= "0110", BRP= "0111", INP= "1000", DSP=0b1001,
                    MUL= "1010", DIV= "1011", STP= "1100")

# dictionary class defined for ease addition of items

class my_dictionary (dict):
	
	def __init__(self):
		self = dict ()
	
	def add (self, key):
		
		global random_var_val
		value = format( random_var_val, '08b')
		self[key] = value
		random_var_val += 1
	
	def add_label(self, key):
		global LC
		print(LC)
		value = format(LC, "08b")
		self[key] = value
		
		

variable_dict = my_dictionary()

label_dict  = my_dictionary()

# In the first pass the label and variable dictionaries will be created

def firstpass():
	
	global LC
	
	input_list = input_file.split("\n")

	for items in input_list:
		
		if items[0:3] == "INP":
			#print(LC)
			val = items.split(" ")
			variable_dict.add(val[1])
			#object_code_file.writelines(opcode_dict.get("INP") + str(variable_dict.get(val[1])))
			
		if items[0:3] == "BRN" or items[0:3] == "BRZ" or items[0:3] == "BRP":
			#print(LC)
			val = items.split(" ")
			if val[1] not in label_dict:          # to check whether the labels are already created or not
				label_dict.add_label(val[1])
				
		
		
		LC += 1
		
	print(variable_dict)
	print(label_dict)


			
	#print(input_list)
			
		#print(line, end = "")

firstpass()