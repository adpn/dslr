import sys
from utils import parse_csv, separateHouses
import math
import matplotlib.pyplot as plt

def remove_everywhere(data : dict[str, list[str]], index : int):
	for _, values in data.items():
		values.pop(index)

def generate_scatter_plot(house_data : dict[str, dict[str, list[str]]], features : tuple[str]):
	print(f"Generating {features[0]}_{features[1]}")
	for key, values in house_data.items():
		plt.scatter(values[features[0]], values[features[1]], label=key, alpha=0.5)
	plt.xlabel(features[0])
	plt.ylabel(features[1])
	plt.legend()
	plt.savefig(f"{features[0]}_{features[1]}.png")
	plt.clf()

def format_features(data : dict[str, list[str]], features_to_keep : tuple[str]):
	courses = {}
	for key in features_to_keep:
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
		print("Usage: python3 scatter_plot.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		data : dict = parse_csv(filename)
		house_data = separateHouses(data)
		features = ("Astronomy", "Defense Against the Dark Arts")
		for key in house_data.keys():
			house_data[key] = format_features(house_data[key], features)
		generate_scatter_plot(house_data, features)
		print("Done")
	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())