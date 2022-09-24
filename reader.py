import csv

time = 0
with open("../201801/vdtrafonetab_info_001.csv", newline = '', encoding='utf-8') as filestream:
    datasheet = csv.reader(filestream, delimiter=',', quotechar='|')
    for row in datasheet:
        time+=1
        print(row)
        if time == 5:
            break
