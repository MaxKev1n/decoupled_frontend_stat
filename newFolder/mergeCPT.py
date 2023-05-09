import numpy as np

def merge_cpt(str):
    stage = 0

    for i in range(4):
        if i == 0:
            stage = 'fetch'
        elif i == 1:
            stage = 'decode'
        elif i == 2:
            stage = 'rename'
        else:
            stage = 'dispatch'

        file = open('../stallReason/'+ str + '-' + stage + '-cpt.txt')
        stats = np.zeros((int(benchmarksFileSize), 24), dtype=np.float32)

        for line in file:
            cptName = line.strip().split()[0]
            bmName = line.strip().split()[0].split('/')[0]

            for i in range(int(cptFileSize)):
                if cptName == cptsNames[i]:
                    for j in range(int(benchmarksFileSize)):
                        if bmName == benchmarksName[j]:
                            for k in range(24):
                                stats[j][k] += float(line.strip().split()[k + 1]) * float(cptsCoe[i])

        statsList = stats.tolist()
        writeFile = open('benchmarkStallReason/' + str + '-' + stage + '-cpt.txt', 'w')
        for i in range(int(benchmarksFileSize)):
            writeFile.write(benchmarksName[i] + ' ')
            for j in range(24):
                writeFile.write('%f'%statsList[i][j])
                writeFile.write(' ')
            writeFile.write('\n')

def merge_cpt_branch():
    name = ''

    for i in range(3):
        if i == 0:
            name = 'stream'
        elif i == 1:
            name = 'xs-dev'
        else:
            name = 'xs-dev-LTAGE'

        file = open('checkpointsBranch/' + name + '-cpt-stats.txt')
        stats = np.zeros((int(benchmarksFileSize), 5), dtype=np.float32)

        for line in file:
            cptName = line.strip().split()[0]
            bmName = line.strip().split()[0].split('/')[0]

            for i in range(int(cptFileSize)):
                if cptName == cptsNames[i]:
                    for j in range(int(benchmarksFileSize)):
                        if bmName == benchmarksName[j]:
                            for k in range(5):
                                stats[j][k] += float(line.strip().split()[k + 1]) * float(cptsCoe[i])

        statsList = stats.tolist()
        writeFile = open('benchmarkBranch/' + name + '-stats.txt', 'w')
        for i in range(int(benchmarksFileSize)):
            writeFile.write(benchmarksName[i] + ' ')
            for j in range(5):
                writeFile.write('%f' % statsList[i][j])
                writeFile.write(' ')
            writeFile.write('\n')


cptsNames = []
cptsCoe = []

cptFile = open('gcb-06-o2-summary.txt')
cptFileSize = cptFile.readline()
for line in cptFile:
    cptsNames.append(line.strip().split()[0])
    cptsCoe.append(line.strip().split()[1])

benchmarksName = []

benchmarksFile = open('gcb-06-o2.txt')
benchmarksFileSize = benchmarksFile.readline()
for line in benchmarksFile:
    benchmarksName.append(line.strip().split()[0])
print(benchmarksName)

#merge_cpt('xs-dev')
#merge_cpt('xs-dev-LTAGE')
#merge_cpt('stream')

merge_cpt_branch()
