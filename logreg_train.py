import sys
from utils import parse_csv, separateHouses
from math import exp, log10, isinf, isnan

# hθ(x) hypothesis function
# return value should be between 0 and 1
# return is a probability
def hypothesis(x : list[float], weights : list[float]) -> float:
	dot_product : float = 0
	for value, weight in zip(x, weights):
		dot_product += value * weight
	return logistic(dot_product)

# g(z) logistic sigmoid function
# return value should be between 0 and 1
# return is a probability
def logistic(z : float) -> float:
	return 1 / (1 + exp(-z))

# return a list of students, as dictionnary with the house name and scores
def format_features(data : dict[str, list[str]], features_to_keep : tuple[str]) -> list[dict[str, str | list[float]]]:
	students : list[dict[str, str | list[float]]] = []
	for i in range(len(data["Hogwarts House"])):
		student : dict[str, str | list[float]]= {}
		if len(data["Hogwarts House"][i]) < 1:
			continue
		student["house"] = data["Hogwarts House"][i]
		student["scores"] = []
		try:
			for feature in features_to_keep:
				student["scores"].append(float(data[feature][i]))
				if isnan(student["scores"][-1]) or isinf(student["scores"][-1]):
					continue
		except:
			continue
		students.append(student)
	return students

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 logreg_train.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		data : dict = parse_csv(filename)
		students = format_features(data, ("Astronomy", "Herbology", "Ancient Runes"))
		print(students)
	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())
