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

def sum(arr):
	if len(arr) == 0:
		raise ValueError("sum() arg is an empty sequence")
	sum_val = 0
	for i in range(len(arr)):
		sum_val += arr[i]
	return sum_val

def mean(arr):
	if len(arr) == 0:
		raise ValueError("mean() arg is an empty sequence")
	return sum(arr) / len(arr)

def std(arr):
	if len(arr) == 0:
		raise ValueError("std() arg is an empty sequence")
	mean_val = mean(arr)
	variance = sum([(x - mean_val) ** 2 for x in arr]) / len(arr)
	return variance ** 0.5

def sort(arr):
	if len(arr) == 0:
		raise ValueError("sort() arg is an empty sequence")
	for i in range(len(arr)):
		for j in range(i, len(arr)):
			if arr[j] < arr[i]:
				arr[i], arr[j] = arr[j], arr[i]
	return arr
	
def percentile(arr, p):
	if p < 0 or p > 100:
		raise ValueError("percentile() arg must be between 0 and 100")
	arr = sort(arr)
	index = (len(arr) - 1) * p / 100
	if index.is_integer():
		return arr[int(index)]
	else:
		return (arr[int(index)] + arr[int(index) + 1]) / 2