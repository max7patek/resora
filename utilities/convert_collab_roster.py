
import sys
import csv

assert len(sys.argv) == 2, "pass in a filepath"

filepath = sys.argv[1]

with open(filepath) as file:

    for line in csv.reader(file, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True):
        if '@' in line[2]:
            print(line[2].lower())
