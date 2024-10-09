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
