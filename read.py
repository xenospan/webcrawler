#
#
#
def ReadFile(filename):
	f = open(filename, "r");

	strs = f.read();
	arr = strs.split("\n");


	#for i in range(len(arr)-1):
		#print(arr[i]);
	f.close();
	return arr;


def sanitiseData(my_str):
	my_list = list(my_str)
	for i in range(len(my_list)):
		if (my_list[i] == "\""):
			my_list[i] = ''
		elif(my_list[i] == "\\"):
			my_list[i] = ''
		elif(my_list[i] == "#"):
			my_list[i] = ''
	
	#print ("".join(my_list))
	return("".join(my_list))


def sanitiseData2(my_str):
	my_list = list(my_str)
	for i in range(len(my_list)):
		if (my_list[i] == "\""):
			my_list[i] = ''
		elif(my_list[i] == "\\"):
			my_list[i] = ''
		elif(my_list[i] == "#"):
			my_list[i] = ''
		elif(my_list[i] == "\n"):
			my_list[i] = ''
	
	#print ("".join(my_list))
	return("".join(my_list))

	
	#print ("".join(my_list))
	return("".join(my_list))


#---Test(sanitiseData)---#
#a = '.a"a\\a#a.'
#print(a)
#print(sanitiseData(a))
