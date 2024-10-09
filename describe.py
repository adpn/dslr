import sys
from utils import parse_csv
from stats_utils import mean, std, min, max, percentile

def describe(content : dict[str, list[str]]) -> dict:
	stats : dict = {}
	for key, values in content.items():
		try:
			test = float(values[0])
			if key == "Index":
				continue
		except:
			continue

		temp = []
		for i in range(len(values)):
			try :
				temp.append(float(values[i]))
			except:
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

	header = " " * 10
	for feature in stats.keys():
		header += f"{feature[:10]}" + " " * (13 - len(feature[:10]))
	print(header)

	for stat_type in stat_types:
		line = stat_type + " " * (10 - len(stat_type))
		for feature in stats.keys():
			line += f"{stats[feature][stat_type]:.6f}" + " " * (13 - len(f"{stats[feature][stat_type]:.6f}"))
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
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())
	