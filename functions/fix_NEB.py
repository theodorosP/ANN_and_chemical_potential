import os
import re

here = str( os.getcwd() )


#loc = the directory where the CONTCAR file exists
#here is the current directory
#folder is the a string 01, 02, 03 04 05 06 depending on the folder we want toa access in loc and here
def apply_changes(loc, here, folder):
	os.system("cp " + loc + folder + "/CONTCAR " + here + "/" + folder + "/POSCAR")
	with open( loc + folder + "/OUTCAR", "r") as file:
		for line in file:
			if "UPDATED" in line:
				last_updated = line
	res = re.findall(r'\b(\d+\.\d+)\b', last_updated)
	res = float(res[0])
	print(res)
	with open(here + "/" + folder + "/TPOTCAR", "a") as file:
		file.write(str(res))
