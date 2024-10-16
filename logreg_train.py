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
	# if z:										# debug
	# 	print(f"logistic with -z = {-z}")		# debug
	return 1 / (1 + exp(-z))

def loop_feature(data : list[dict], weights : list[float], house : str, j : int) -> float:
	# print("we loopin features")			# debug
	sum : float = 0
	for student in data:
		sum += (hypothesis(student["scores"], weights) - int(house == student["house"])) #* student["scores"][j]
	# print(f"return {sum}")				# debug
	return sum

def loop_weight(data : list[dict], weights : list[float], house : str):
	# print("we loopin weights")			# debug
	m = len(data)
	for j in range(len(weights)):
		weights[j] = loop_feature(data, weights, house, j) / m
		# print (f"new weight just dropped: {weights[j]}")	# debug

# using the partial derivative formula
def loop_house(data : list[dict], house_weights : dict[str : list[float]]):
	# print("we loopin houses")			# debug
	for house in house_weights:
		loop_weight(data, house_weights[house], house)


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
		features : tuple[str] = ["Astronomy", "Herbology", "Ancient Runes"]
		house_weights = {"Ravenclaw": [0]*len(features), "Slytherin": [0]*len(features), "Gryffindor": [0]*len(features), "Hufflepuff": [0]*len(features)}
		# print(f"before: {house_weights}")			# debug
		data : dict = parse_csv(filename)
		student_data = format_features(data, features)
		for i in range(1000):
			loop_house(student_data, house_weights)
			if not (i % 100):
				print(".", end="", flush=True)
		print(f"\nAFTER 1000: \n{house_weights}")	# debug

	except Exception as e:
		print("Error:", e)
		e.with_traceback()
		return 1

if __name__ == "__main__":
	exit(main())
