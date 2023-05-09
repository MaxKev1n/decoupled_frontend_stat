import os
import re

def getFiles():
    filenames = os.listdir(r'../weight/gcb-06-o2')
    instNums = []
    benchNames = []

    for file in filenames:
        f1 = open("../weight/gcb-06-o2/" + file)
        for line in f1:
            pass
        last_line = re.sub('\x1b.*?m', '', line).strip().split()

        if len(file.strip().split('.')) <= 2:
            benchNames.append(file.strip().split('.')[0])
        else:
            benchNames.append(file.strip().split('.')[0] + '.' + file.strip().split('.')[1])
        instNums.append(int(last_line[5]))


    return benchNames, instNums

names, insts = getFiles()

f = open("gcb-06-o2.txt", 'w')

f.write(str(len(names)) + '\n')

for i in range(len(names)):
    f.write(names[i] + ' ')
    f.write(str(insts[i]) + '\n')