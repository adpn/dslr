import sys
from utils import parse_csv
from stats_utils import mean, std, min, max, percentile
import math

COLUMN_WIDTH = 12
TOTAL_WIDTH = 15

def describe(data : dict[str, list[str]]) -> dict:
	stats : dict = {}
	for key, values in data.items():
		if key == "Index":
			continue

		temp = []
		for value in values:
			try :
				value = float(value)
				if math.isnan(value) or math.isinf(value):
					continue
				temp.append(value)
			except:
				continue

		if (len(temp) == 0):
			continue

		stats[key] = {
			"Count": len(temp),
			"Mean": mean(temp),
			"Std": std(temp),
			"Min": min(temp),
			"25%": percentile(temp, 25),
			"50%": percentile(temp, 50),
			"75%": percentile(temp, 75),
			"Max": max(temp)
		}

	return stats
	
def print_stats(stats : dict):
	stat_types = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]

	header = " " * COLUMN_WIDTH
	for feature in stats.keys():
		header += f"{feature[:COLUMN_WIDTH]}" + " " * (TOTAL_WIDTH - len(feature[:COLUMN_WIDTH]))
	print(header)

	for stat_type in stat_types:
		line = stat_type + " " * (COLUMN_WIDTH - len(stat_type))
		for feature in stats.keys():
			line += f"{stats[feature][stat_type]:.6f}" + " " * (TOTAL_WIDTH - len(f"{stats[feature][stat_type]:.6f}"))
		print(line)

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 describe.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		content : dict = parse_csv(filename)
		stats : dict = describe(content)
		print_stats(stats)
	except Exception as e:
		print("Error", e)
		return 1

if __name__ == "__main__":
	exit(main())
	