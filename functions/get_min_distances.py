import math

class GetMinDistance():
	#constructor of the class
	def __init__(self, struc):
		self.struc = read(struc)

	#get the distance between each atom in atoms1, atoms2
	#atoms1 = list of atoms of the one molecule
	#atoms2 = list of atoms of the second molecule
	def get_distance(self, atoms1, atoms2):
		distance = {}
		for i in atoms1:
			for j in atoms2:
				dist = math.sqrt((self.struc[i].position[0] - self.struc[j].position[0])**2 + (self.struc[i].position[1] - self.struc[j].position[1])**2 + (self.struc[i].position[2] - self.struc[j].position[2])**2)
				atom_1 = self.struc[i].symbol
				atom_2 = self.struc[j].symbol
				distance["distance: " + str(i) + "-" + str(j) + " " +  atom_1 + "-" + atom_2] = dist
		return distance 

	def get_min_distances(self, atoms1, atoms2, cut_off):
		distance = self.get_distance(atoms1, atoms2)
		sorted_distances = sorted(distance.items(), key=lambda x: x[1])
		for i ,j in sorted_distances:
			if j < cut_off:
				print(i, round(j, 3) )
