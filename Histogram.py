import sys
from utils import parse_csv

def homogynousFeature(content : dict[str, list[str]]) -> dict:
	feature : str
	means : dict[str, dict]
	diff : float
	for key, values in content.items():
		key_means : dict[str, dict]
		if key == "Index" or key == "Hogwarts House":
			continue
		i = int(0);
		while i < len(values):
			house = content["Hogwarts House"][i]
			if not house:
				continue
			if not house in key_means:
				key_means[house] = {"mean": float(values[i]), "count": int(1)}
				continue
			# mean = (old_mean * n + value) / (n + 1)
			key_means[house]["mean"] = (key_means[house]["mean"] * key_means[house]["count"] + float(values[i])) / (key_means[house]["count"] + 1)
			key_means[house]["count"] += 1
			++i
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
	return {"feature": feature, "means": means}
	
# for the most homogynous feature
def histogram(stats : dict):
	print(stats)
	
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