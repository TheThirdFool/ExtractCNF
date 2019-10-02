
#This code is to extract the data from a genie (.CNF) file.
#Written by Daniel Foulds-Holt : Daniel_FouldsHolt@uml.edu

import os
import struct

def List_Files(): 			#Lists the '.CNF' files in the working directory.
	basepath = os.getcwd()
	#basepath = os.path.dirname(cwd)#os.path.realpath(__file__))
	print "Directory: ", basepath
	print "Files: "
	print ""
	for entry in os.listdir(basepath):
		if os.path.isfile(os.path.join(basepath, entry)):
			if ".CNF" in entry:
				print entry
	print ""

def ReadCNF(filename, x_array, y_array): #This reads the binary data format used by Genie and outputs the data to arrays.
	data = []
	with open(filename, mode='rb') as b_file: # b is important -> binary
		byte_s = b_file.read(4)
		while byte_s != "":
			try:
				buffer_b = struct.unpack('i',byte_s)[0]
				data.append(buffer_b)
				#data.append(str(byte_s))      #.decode("utf-8")) #couldnt decode besause only 3 bytes left! lost bytes!
			except ValueError:
				print "ERROR READING FILE!"
				print "bytes:"
				print byte_s
				print "^ Broken Bytes ^"
				print ""
				
			byte_s = b_file.read(4)
	#print len(data)
	offset = len(data) - 4096 #* 4) #New bin no - doesnt work - only can take 4096 

	i = offset + 1
	while i < len(data):
		x_array.append(i - offset)
		y_array.append(data[i])
		i += 1

	print "Read file ", filename, "!"


def Extract_Data():
	while True:
		print ""
		print "Which file do you want to extract from? ('l' lists files)"
		filename = raw_input("Filename = ")

		if filename == "l":
			List_Files()	#l lists the files 
			continue
		if filename == "q":
			return

		hist_name = "CNF"
		print ""
		print "Reading '.CNF' file..."
		print ""
		break

	print "What filename do you want to output to? (blank = automatic)"
	out_file = raw_input('Filename = ')

	while True:
		print ""
		print "What file type?"
		print " .txt : t"
		print " .dat : d"
		print " .csv : c"
		print ""
		file_type = raw_input("File type = ")
		print ""
		
		if file_type == "t":
			file_type = ".txt"
			break
		elif file_type == "d":
			file_type = ".dat"
			break
		elif file_type == "c":
			file_type = ".csv"
			break
		else: 
			print "Enter a value!"
			continue

	if out_file == "":
		n_fn = filename[:-4] + "_"

	endfile = out_file + file_type

	file_print = open(endfile, "w")

	x_index = []
	x_count = []
	ReadCNF(filename, x_index, x_count)
	i = 0
	while i < len(x_index):
		print >> file_print, x_index[i], ",", x_count[i]
		i += 1

	file_print.close()

	print ""
	print "Extracted ", hist_name, " from ", filename, " into ", endfile, "."
	print ""


#Main = extract data.

Extract_Data()
