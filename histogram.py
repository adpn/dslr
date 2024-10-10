import sys
from utils import parse_csv, separateHouses
from math import isnan, isinf
import matplotlib.pyplot as plt

# doesn't keep index relations
def prepData(house_data : dict[str, dict[str, list]], feature : str) -> None:
	for house, house_dict in house_data.items():
		new_list : list[float] = []
		for value in house_dict[feature]:
			try:
				to_add = float(value)
				if isnan(to_add) or isinf(to_add):
					continue
				new_list.append(to_add)
			except:
				continue
		house_dict[feature] = new_list

def histogram(data : dict[str, dict[str, list[str]]]):
	feature = "Care of Magical Creatures"
	# first_house : str = next(iter(data))
	# for feature in data[first_house]:
	# 	if feature == "index":
	# 		continue
	prepData(data, feature)
	# if not len(data[first_house][feature]):
	# 	continue
	fig, ax = plt.subplots()
	for house, values in data.items():
		ax.hist(values[feature], histtype='barstacked', alpha=0.5, label=house)
	ax.set_title(feature)
	ax.legend(prop={'size': 10})
	plt.savefig(f"hist_{feature}.png")

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 histogram.py <dataset>")
		return 1
	try:
		house_data = separateHouses(parse_csv(sys.argv[1]))
		histogram(house_data)
	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())
