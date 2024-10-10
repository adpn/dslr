import sys
from utils import parse_csv, separateHouses
import math
import matplotlib.pyplot as plt

def remove_everywhere(data : dict[str, list[str]], index : int):
	for key, values in data.items():
		values.pop(index)

# negative correlation found between Astronomy and Defense Against the Dark Arts
def generate_every_scatter_plot(house_data : dict[str, dict[str, list[str]]]):
	courses = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"]
	for name in courses:
		for name2 in courses:
			if name == name2:
				continue
			print("Generating " + name + "_" + name2)
			for key, values in house_data.items():
				plt.scatter(values[name], values[name2], label=key, alpha=0.5)
			plt.xlabel(name)
			plt.ylabel(name2)
			plt.legend()
			plt.savefig("scatter/" + name + "_" + name2 + ".png")
			plt.clf()

def generate_scatter_plot(house_data : dict[str, dict[str, list[str]]]):
	features = ("Astronomy", "Defense Against the Dark Arts")
	print("Generating " + features[0] + "_" + features[1])
	for key, values in house_data.items():
		plt.scatter(values[features[0]], values[features[1]], label=key, alpha=0.5)
	plt.xlabel(features[0])
	plt.ylabel(features[1])
	plt.legend()
	plt.savefig(features[0] + "_" + features[1] + ".png")
	plt.clf()

def format_features(data : dict[str, list[str]]):
	courses = {"Arithmancy" : [], "Astronomy" : [], "Herbology" : [], "Defense Against the Dark Arts" : [], "Divination" : [], "Muggle Studies" : [], "Ancient Runes" : [], "History of Magic" : [], "Transfiguration" : [], "Potions" : [], "Care of Magical Creatures" : [], "Charms" : [], "Flying" : []}
	for key in courses.keys():
		courses[key] = data[key]

	for key, values in courses.items():
		temp = []
		i = 0
		while i < len(values):
			try :
				value = float(values[i])
				if math.isnan(value) or math.isinf(value):
					remove_everywhere(courses, i)
					continue
				temp.append(value)
			except:
				remove_everywhere(courses, i)
				continue
			i += 1

		if (len(temp) == 0):
			continue

		courses[key] = temp
	return courses

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 describe.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		data : dict = parse_csv(filename)
		house_data = separateHouses(data)
		for key in house_data.keys():
			house_data[key] = format_features(house_data[key])
		generate_scatter_plot(house_data)
		print("Done")
	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())