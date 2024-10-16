import sys
from utils import parse_csv
from math import isinf, isnan
from logreg_train import logistic
# from stats_utils import max, sum

def predict(x: list[float], weights: list[float]) -> float:
    dot_product = sum(value * weight for value, weight in zip(x, weights))
    probability = logistic(dot_product)
    return probability

def predict_house(x: list[float], house_weights: dict[str, list[float]]) -> str:
    house_probabilities = {}
    for house, weights in house_weights.items():
        house_probabilities[house] = predict(x, weights)
    predicted_house = max(house_probabilities, key=house_probabilities.get)
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
		features : tuple[str] = ["Astronomy", "Herbology", "Ancient Runes"]
		data : dict = parse_csv(filename)
		student_data = format_features(data, features)
		houseweights = {'Ravenclaw': [-0.08746534561551508, 9.167919618624145, -0.09751236127920083], 'Slytherin': [-0.028803400033930178, -3.0914920753472144, -0.03220244345453278], 'Gryffindor': [0.015075712648868644, -16.119546548597317, -0.2343335972432614], 'Hufflepuff': [0.049450692724162124, 7.185971306027158, -0.07845708389339086]}
		
		NB_TESTS = 1000
		success = 0
		for i in range(NB_TESTS):
			result = predict_house(student_data[i]["scores"], houseweights)
			if result == student_data[i]["house"]:
				success += 1
			else:
				print(student_data[i]["index"], student_data[i]["house"], result)
		print("Precision:", success / NB_TESTS)


	except Exception as e:
		print("Error:", e)
		e.with_traceback()
		return 1

if __name__ == "__main__":
	exit(main())