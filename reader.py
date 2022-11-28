import csv

time = 0
with open("/Volumes/LaCie/04_111project/data of project/201801/vdtrafonetab_info_001.csv", newline = '', encoding='utf-8') as filestream:
    datasheet = csv.reader(filestream, delimiter=',', quotechar='|')
    for row in datasheet:
        time+=1
        print(row)
        if time == 20:
            break
