import sys
from utils import parse_csv
from math import exp, isinf, isnan
from json import dump
import matplotlib.pyplot as plt
from stats_utils import max, min

NB_ITERATIONS = 1000 # totally artificial number
LEARNING_RATE = 0.01 # totally artificial number
DATA_MAX_VALUE = 100 # totally artificial number
# "Divination", "Flying", "History of Magic", "Muggle Studies"
FEATURES : tuple[str] = ("Astronomy", "Herbology", "Ancient Runes", "Defense Against the Dark Arts")

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

# using the partial derivative formula
def loop_house(data : list[dict], house_weights : dict[str : list[float]]):
	for house in house_weights:
		train(data, house, house_weights[house])

# train for one class
def train(students : list[dict[str, str | list[float]]], housename : str, weights : list[float]):
	m = len(students)
	n = len(weights)
	# weight_history = [] # debug

	print(f"{housename}:", end="", flush=True)
	for i in range(NB_ITERATIONS):
		if i % int(NB_ITERATIONS / 10) == 0:
			print(f" {int(i / int(NB_ITERATIONS / 10))}", end="", flush=True)
		gradiants = [0] * n
		for student in students:
			x = student["scores"]
			y = 1 if student["house"] == housename else 0
			h = hypothesis(x, weights)

			for j in range(n):
				gradiants[j] += (h - y) * x[j]

		for j in range(n):
			weights[j] -= LEARNING_RATE * gradiants[j] / m
		# weight_history.append(weights.copy()) # debug

	# plot_weight_evolution(weight_history, housename) # debug
	print(" >END<")

def plot_weight_evolution(weight_history, housename):
	iterations = range(len(weight_history))
	n_weights = len(weight_history[0])

	plt.figure(figsize=(10, 6))

	for j in range(n_weights):
		weight_evolution = [weights[j] for weights in weight_history]
		plt.plot(iterations, weight_evolution, label=FEATURES[j])

	plt.xlabel('Iterations')
	plt.ylabel('Weight Value')
	plt.title(f'Evolution of {housename}')
	plt.legend()
	plt.grid(True)
	plt.savefig(f"{housename}.png")
	plt.clf()

# return a list of students, as dictionary with the house name and scores list
# tracks stats for every feature (min and max)
def format_features(data : dict[str, list[str]], feature_stats : list[list[float]]) -> list[dict[str, str | list[float]]]:
	students : list[dict[str, str | list[float]]] = []
	for i in range(len(data["Hogwarts House"])):
		student : dict[str, str | list[float]]= {}
		if len(data["Hogwarts House"][i]) < 1:
			continue
		student["house"] = data["Hogwarts House"][i]
		student["scores"] = []
		try:
			for feature in FEATURES:
				student["scores"].append(float(data[feature][i]))
				if isnan(student["scores"][-1]) or isinf(student["scores"][-1]):
					continue
		except:
			continue
		students.append(student)
		if not len(feature_stats):
			for j in range(len(student["scores"])):
				feature_stats.append([student["scores"][j], student["scores"][j]])
		else:
			for j in range(len(student["scores"])):
				feature_stats[j][0] = min([feature_stats[j][0], student["scores"][j]])
				feature_stats[j][1] = max([feature_stats[j][1], student["scores"][j]])
	return students

def normalise_data(data : list[dict[str, str | list[float]]], feature_stats : list[list[float]]):
	shift : list[float] = []
	ratio : list[float] = []
	for value in feature_stats:
		shift.append((value[0] + value[1]) / 2)
		ratio.append((abs(value[0]) + abs(value[1])) / 2 / DATA_MAX_VALUE)
	for student in data:
		for i in range(len(shift)):
			student["scores"][i] = (student["scores"][i] - shift[i]) / ratio[i]

def has_bad_features(data : dict[str, list[str]]) -> bool:
	result : bool = False
	for value in FEATURES:
		if value not in data:
			print(f"Feature {value}: not found in dataset")
			result = True
	return result

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 logreg_train.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		house_weights = {"Ravenclaw": [0]*len(FEATURES), "Slytherin": [0]*len(FEATURES), "Gryffindor": [0]*len(FEATURES), "Hufflepuff": [0]*len(FEATURES)}
		data : dict = parse_csv(filename)
		if has_bad_features(data):
			return 1
		feature_stats : list[list[float]] = []
		student_data = format_features(data, feature_stats)
		normalise_data(student_data, feature_stats)
		loop_house(student_data, house_weights)
		house_weights["features"] = FEATURES
		house_weights["normal"] = DATA_MAX_VALUE
		dump(house_weights, open('weights.json', 'w'))

	except Exception as e:
		print("Error", e)
		return 1

if __name__ == "__main__":
	exit(main())
