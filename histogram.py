import sys
from utils import parse_csv, separateHouses
from math import isnan, isinf
import matplotlib.pyplot as plt

# doesn't keep index relations
def prepData(house_data : dict[str, dict[str, list]], feature : str) -> None:
	for values in house_data.values():
		new_list : list[float] = []
		for value in values[feature]:
			try:
				to_add = float(value)
				if isnan(to_add) or isinf(to_add):
					continue
				new_list.append(to_add)
			except:
				continue
		values[feature] = new_list

def histogram(data : dict[str, dict[str, list[str]]], feature : str):
	prepData(data, feature)
	if not len(data[next(iter(data))][feature]):
		return
	plt.clf()
	for house, values in data.items():
		plt.hist(values[feature], histtype='barstacked', alpha=0.5, label=house)
	plt.title(feature)
	plt.legend(prop={'size': 10})
	plt.savefig(f"hist_{feature}.png")

def every_histogram(data : dict[str, dict[str, list[str]]]):
	for feature in data[next(iter(data))]:
		if feature == "Index" or feature == "First Name" or feature == "Last Name":
			continue
		histogram(data, feature)

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 histogram.py <dataset>")
		return 1
	try:
		house_data = separateHouses(parse_csv(sys.argv[1]))
		histogram(house_data, "Care of Magical Creatures")
	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())
