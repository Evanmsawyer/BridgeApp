import csv

def writerow(row, fd):
    #writes trick record row to file fd
    sep = '\",\"'
    res = ''
    res += row[0] + ',' + row[1] + ',\"' + row[2] + sep + row[3] + sep + row[4] + '\"'
    print(res, file=fd)

#specify file paths
difference_path = "./diff.txt"
csv_path = "./CSVs/trick.csv"

#get discrepancies from difference_path
with open(difference_path, "r") as f:
    diff = [row.strip() for row in f]

#write rows that do not match discrepancies
with open(csv_path, "r") as input, open("./CSVs/trick_new.csv", "w") as output:
    reader = csv.reader(input)
    for row in reader:
        if row[1] not in diff:
            writerow(row, output)
