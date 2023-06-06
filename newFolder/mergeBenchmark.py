import numpy as np

def merge_benchmark(str):
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

        file = open('benchmarkStallReason/'+ str + '-' + stage + '-cpt.txt')
        stats = np.zeros((len(workloadName), 24), dtype=np.float32)

        for line in file:
            bmName = line.strip().split()[0]
            wlName = line.strip().split()[0].split('_')[0]

            for i in range(len(benchmarksName)):
                if bmName == benchmarksName[i]:
                    for j in range(len(workloadName)):
                        if wlName == workloadName[j]:
                            for k in range(24):
                                stats[j][k] += float(line.strip().split()[k + 1]) * float(benchmarksCoe[i])

        statsList = stats.tolist()
        writeFile = open('workloadStallReason/' + str + '-' + stage + '-cpt.txt', 'w')
        for i in range(len(workloadName)):
            writeFile.write(workloadName[i] + ' ')
            for j in range(24):
                writeFile.write('%f'%statsList[i][j])
                writeFile.write(' ')
            writeFile.write('\n')


def merge_benchmark_branch():
    name = ''

    for i in range(3):
        if i == 0:
            name = 'stream'
        elif i == 1:
            name = 'xs-dev'
        else:
            name = 'xs-dev-LTAGE'

        file = open('benchmarkBranch/' + name + '-stats.txt')
        stats = np.zeros((int(benchmarksFileSize), 5), dtype=np.float32)

        for line in file:
            bmName = line.strip().split()[0]
            wlName = line.strip().split()[0].split('_')[0]

            for i in range(len(benchmarksName)):
                if bmName == benchmarksName[i]:
                    for j in range(len(workloadName)):
                        if wlName == workloadName[j]:
                            for k in range(5):
                                stats[j][k] += float(line.strip().split()[k + 1]) * float(benchmarksCoe[i])

        statsList = stats.tolist()
        writeFile = open('workloadBranch/' + name + '.txt', 'w')
        writeFile.write(str(len(workloadName)) + '\n')
        for i in range(len(workloadName)):
            writeFile.write(workloadName[i] + ' ')
            for j in range(5):
                writeFile.write('%f'%statsList[i][j])
                writeFile.write(' ')
            writeFile.write('\n')

def merge_benchmark_ipc():
    name = ''

    for i in range(3):
        if i == 0:
            name = 'stream'
        elif i == 1:
            name = 'xs-dev'
        else:
            name = 'xs-dev-LTAGE'

        file = open('benchmarkIPC/' + name + '-stats.txt')
        stats = np.zeros((int(benchmarksFileSize), 1), dtype=np.float32)

        for line in file:
            bmName = line.strip().split()[0]
            wlName = line.strip().split()[0].split('_')[0]

            for i in range(len(benchmarksName)):
                if bmName == benchmarksName[i]:
                    for j in range(len(workloadName)):
                        if wlName == workloadName[j]:
                            stats[j][0] += float(line.strip().split()[1]) * float(benchmarksCoe[i])

        statsList = stats.tolist()
        writeFile = open('workloadIPC/' + name + '.txt', 'w')
        writeFile.write(str(len(workloadName)) + '\n')
        for i in range(len(workloadName)):
            writeFile.write(workloadName[i] + ' ')
            writeFile.write('%f'%statsList[i][0])
            writeFile.write('\n')


benchmarksName = []
benchmarksNum = []
benchmarksCoe = []
workloadName = []
workloadNum = []

benchmarksFile = open('gcb-06-o2.txt')
benchmarksFileSize = benchmarksFile.readline()
for line in benchmarksFile:
    benchmarksName.append(line.strip().split()[0])
    benchmarksNum.append(int(line.strip().split()[1]))
    benchmarksCoe.append(float(0))

    exist = False
    for i in range(len(workloadName)):
        if line.strip().split()[0].split('_')[0] == workloadName[i]:
            exist = True
            workloadNum[i] += int(line.strip().split()[1])
            break

    if not exist:
        workloadName.append(line.strip().split()[0].split('_')[0])
        workloadNum.append(int(line.strip().split()[1]))

for i in range(len(benchmarksName)):
    for j in range(len(workloadName)):
        if benchmarksName[i].split('_')[0] == workloadName[j]:
            benchmarksCoe[i] = float(benchmarksNum[i]) / float(workloadNum[j])
            break

#merge_benchmark('xs-dev')
#merge_benchmark('xs-dev-LTAGE')
#merge_benchmark('stream')
merge_benchmark_ipc()