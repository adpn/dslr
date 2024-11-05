import sys
from utils import parse_csv
from math import isnan, nan
from logreg_train import logistic
from json import load
from stats_utils import max, min, sum

def predict(x: list[float], weights: list[float]) -> float:
    dot_product = sum([value * weight for value, weight in zip(x, weights)])
    probability = logistic(dot_product)
    return probability

def predict_house(x: list[float], house_weights: dict[str, list[float]]) -> str:
    house_probabilities = {}
    for house, weights in house_weights.items():
        house_probabilities[house] = predict(x, weights)

    houses = list(house_probabilities.keys())
    probabilities = list(house_probabilities.values())

    max_probability = max(probabilities)
    max_index = probabilities.index(max_probability)
    predicted_house = houses[max_index]
    return predicted_house

# return a list of students, as dictionary with the house name and scores list
# tracks stats for every feature (min and max)
def format_features(data : dict[str, list[str]], features_to_keep : tuple[str], feature_stats : list[list[float]]) -> list[dict[str, str | list[float]]]:
	students : list[dict[str, str | list[float]]] = []
	for i in range(len(data["Index"])):
		student : dict[str, str | list[float]]= {}
		if len(data["Index"][i]) < 1:
			continue
		student["house"] = data["Hogwarts House"][i]
		student["index"] = data["Index"][i]
		student["scores"] = []

		for feature in features_to_keep:
			try:
				student["scores"].append(float(data[feature][i]))
			except:
				student["scores"].append(nan)
		students.append(student)
		if not len(feature_stats):
			for j in range(len(student["scores"])):
				feature_stats.append([student["scores"][j], student["scores"][j]])
		else:
			for j in range(len(student["scores"])):
				if (isnan(student["scores"][j])):
					continue
				feature_stats[j][0] = min([feature_stats[j][0], student["scores"][j]])
				feature_stats[j][1] = max([feature_stats[j][1], student["scores"][j]])
	return students

def normalise_data(data : list[dict[str, str | list[float]]], feature_stats : list[list[float]], max_value : int):
	shift : list[float] = []
	ratio : list[float] = []
	for value in feature_stats:
		shift.append((value[0] + value[1]) / 2)
		ratio.append((abs(value[0]) + abs(value[1])) / 2 / max_value)
	for student in data:
		for i in range(len(shift)):
			if isnan(student["scores"][i]):
				student["scores"][i] = 0
				continue
			student["scores"][i] = (student["scores"][i] - shift[i]) / ratio[i]

def main() -> int:
	if (len(sys.argv) != 2):
		print("Usage: python3 logreg_predict.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		data : dict = parse_csv(filename)
		house_weights : dict = load(open("weights.json", 'r'))	# open argv weight file instead
		features : tuple[str] = house_weights.pop("features")
		data_max_value = house_weights.pop("normal")
		feature_stats : list[list[float]] = []
		student_data = format_features(data, features, feature_stats)
		normalise_data(student_data, feature_stats, data_max_value)

		nb_lines = len(student_data)
		with open("houses.csv", 'w') as file:
			file.write("Index,Hogwarts House\n")
			for i in range(nb_lines):
				result = predict_house(student_data[i]["scores"], house_weights)
				file.write(f'{student_data[i]["index"]},{result}\n')

	except Exception as e:
		print("Error", e)
		return 1

if __name__ == "__main__":
	exit(main())
