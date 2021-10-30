import json
import csv

# open json file
with open('emp.json') as json_file:
	data = json.load(json_file)
print(data)
# find first key in json format
for i in data.keys():
	x = i
	print(x)
	break

# represent first key as variable
json_data = data[x]

print(json_data)

# open/create csv file
csv_file = open("test.csv", 'w', newline='')
# create the csv writer object
csv_writer = csv.writer(csv_file)

count = 0

for element in json_data:
	if count == 0:
		header = element.keys()
		print(header)
		csv_writer.writerow(header)
		count += 1
	csv_writer.writerow(element.values())
csv_file.close()
