import sys
from utils import parse_csv, separateHouses
from scatter_plot import format_features
import matplotlib.pyplot as plt

def generate_pair_plot(house_data : dict[str, dict[str, list[str]]], features : tuple[str]):
	num_features = len(features)
	fig, axes = plt.subplots(nrows=num_features, ncols=num_features, figsize=(30, 30))
	plt.subplots_adjust(wspace=0.1, hspace=0.1)
	print("Generating Pair Plot Matrix.png")
	for i in range(num_features):
		for j in range(num_features):
			name, name2 = features[i], features[j]
			ax = axes[i, j]
			if i == j:
				for key, values in house_data.items():
					ax.hist(values[name], histtype='barstacked', label=key, alpha=0.5)
			else:
				for key, values in house_data.items():
					ax.scatter(values[name], values[name2], label=key, alpha=0.5)

			if i == num_features - 1:
				ax.set_xlabel(features[j])
			else:
				ax.set_xticklabels([])

			if j == 0:
				ax.set_ylabel(features[i])
			else:
				ax.set_yticklabels([])
	plt.suptitle('Pair Plot Matrix', fontsize=30)
	plt.savefig("Pair Plot Matrix.png")
	plt.clf()

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 pair_plot.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		data : dict = parse_csv(filename)
		house_data = separateHouses(data)
		features = ("Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
			  		"Divination", "Muggle Studies", "Ancient Runes", "History of Magic",
					"Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying")
		for key in house_data.keys():
			house_data[key] = format_features(house_data[key], features)
		generate_pair_plot(house_data, features)
		print("Done")
	except Exception as e:
		print("Error", e)
		return 1

if __name__ == "__main__":
	exit(main())