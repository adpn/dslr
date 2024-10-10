import sys
from utils import parse_csv, separateHouses
from math import isnan, isinf
import matplotlib.pyplot as plt

def prepData(house_data : dict[str, dict[str, list[str]]]) -> dict:
	# f = open("house_test.txt",'w')
	# f.write(str(house_data))
	pass

def histogram(stats : dict):
	fig, ax = plt.subplots()
	ax.hist(stats["means"])
	plt.savefig("hist.png")

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 histogram.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		content = parse_csv(filename)
		house_data = separateHouses(content)
		# histogram(house_data)
	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())
