import sys
from utils import parse_csv
from math import isinf, isnan
from logreg_train import logistic
from json import load
from stats_utils import max, sum

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

def format_features(data : dict[str, list[str]], features_to_keep : tuple[str]) -> list[dict[str, str | list[float]]]:
	students : list[dict[str, str | list[float]]] = []
	for i in range(len(data["Index"])):
		student : dict[str, str | list[float]]= {}
		if len(data["Index"][i]) < 1:
			continue
		student["house"] = data["Hogwarts House"][i]
		student["index"] = data["Index"][i]
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
		print("Usage: python3 logreg_predict.py <dataset>")
		return 1
	try:
		filename = sys.argv[1]
		data : dict = parse_csv(filename)
		house_weights : dict = load(open("weights.json", 'r'))	# open argv weight file instead
		features : tuple[str] = house_weights["features"]
		house_weights.pop("features")
		student_data = format_features(data, features)
		
		NB_TESTS = 1000
		success = 0
		for i in range(NB_TESTS):
			result = predict_house(student_data[i]["scores"], house_weights)
			if result == student_data[i]["house"]:
				success += 1
			else:
				print(student_data[i]["index"], student_data[i]["house"], result)
		print("Precision:", success / NB_TESTS)

	except Exception as e:
		print("Error:", e)
		return 1

if __name__ == "__main__":
	exit(main())
