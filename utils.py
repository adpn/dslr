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

def max(arr):
	if len(arr) == 0:
		raise ValueError("max() arg is an empty sequence")
	max_val = arr[0]
	for i in range(1, len(arr)):
		if arr[i] > max_val:
			max_val = arr[i]
	return max_val

def min(arr):
	if len(arr) == 0:
		raise ValueError("min() arg is an empty sequence")
	min_val = arr[0]
	for i in range(1, len(arr)):
		if arr[i] < min_val:
			min_val = arr[i]
	return min_val