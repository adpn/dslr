import sys
from utils import parse_csv, separateHouses
from math import exp

# hθ(x) hypothesis function
# return value should be between 0 and 1
# return is a probability
def hypothesis(x : float, weights : list) -> float:
	value = 0 #this should come from weights, idk how to calculate it
	return logistic(value * x)

# g(z) logistic sigmoid function
# return value should be between 0 and 1
# return is a probability
def logistic(z : float) -> float:
	return 1 / (1 + exp(-z))

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 logreg_train.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		data : dict = parse_csv(filename)
		house_data = separateHouses(data)

	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())