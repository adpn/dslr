import sys
from utils import parse_csv, max, min

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 describe.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		content : dict = parse_csv(filename)
		print(content.keys())
		print(content["First Name"])
	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())
	