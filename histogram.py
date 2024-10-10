import sys
from utils import parse_csv
from math import isnan, isinf
import matplotlib.pyplot as plt

# need to do this with std deviation or sumn i think
def homogynousFeature(content : dict[str, list[str]]) -> dict:
	feature : str = ""
	means : dict[str, dict]
	diff : float
	# separate data by house
	for key, values in content.items():
		key_means : dict[str, dict] = {}
		if key == "Index" or key == "Hogwarts House":
			continue
		i = int(0)
		while i < len(values):
			i += 1
			house = content["Hogwarts House"][i - 1]
			if not house:
				continue
			try:
				value = float(values[i - 1])
				if isnan(value) or isinf(value):
					continue
				if not house in key_means:
					key_means[house] = {"mean": value, "count": int(1)}
					continue
				# mean = (old_mean * n + value) / (n + 1)
				key_means[house]["mean"] = (key_means[house]["mean"] * key_means[house]["count"] + value) / (key_means[house]["count"] + 1)
				key_means[house]["count"] += 1
			except:
				continue
		if not len(key_means):
			continue
		# homogeneity test
		means_mean = float(0)
		for house, duo in key_means.items():
			means_mean += duo["mean"]
		means_mean /= len(key_means)
		key_diff = float(0)
		for house, duo in key_means.items():
			key_diff += abs(means_mean - duo["mean"])
		if not feature or key_diff < diff:
			feature = key
			means = key_means
			diff = key_diff
	res_houses : list[str] = []
	res_means : list[float] = []
	for key, values in means.items():
		res_houses.append(key)
		res_means.append(values["mean"])
	return {"feature": feature, "houses": res_houses, "means": res_means}

def histogram(stats : dict):
	fig, ax = plt.subplots()
	ax.hist(stats["means"])
	plt.savefig("hist.png")

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 describe.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		content = parse_csv(filename)
		feature = homogynousFeature(content)
		histogram(feature)
	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())
