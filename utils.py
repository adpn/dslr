import csv

def parse_csv(filepath : str) -> dict:
	with open(filepath, newline='') as csvfile:
		reader = csv.reader(csvfile)
		headers = next(reader)
		columns = {header: [] for header in headers}
		for row in reader:
			for header, value in zip(headers, row):
				columns[header].append(value)
	return columns

def separateHouses(content : dict[str, list[str]]) -> dict[str, dict[str, list[str]]]:
	house_data : dict[str, dict[str, list[str]]] = {}
	for key, values in content.items():
		if key == "Hogwarts House":
			continue
		for i in range(len(values)):
			house = content["Hogwarts House"][i]
			if not house:
				continue
			if house not in house_data:
				house_data[house] = {}
			if key not in house_data[house]:
				house_data[house][key] = []
			house_data[house][key].append(values[i])
	return house_data
