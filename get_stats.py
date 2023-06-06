import numpy as np
import os
import fnmatch


def get_stats():
    np.set_printoptions(formatter={'all': lambda x: str(x)}, threshold=100)
    t = np.dtype(
        [('file_name', np.str_, 100), ('instCount', np.int32), ('branchMisCount', np.int32), ('branches', np.int32)])

    for i in range(0, 3):
        files = []
        write_file = []
        file_dir = ''

        if i == 0:
            write_file = 'stream-cpt-stats.txt'
            file_dir = './stream'
        elif i == 1:
            write_file = 'xs-dev-cpt-stats.txt'
            file_dir = './xs-dev'
        else:
            write_file = 'xs-dev-LTAGE-cpt-stats.txt'
            file_dir = './xs-dev-LTAGE'

        for root, dirs, theFiles in os.walk(file_dir):
            for file in theFiles:
                if fnmatch.fnmatch(os.path.join(root, file), '*/stats.txt'):
                    files.append(os.path.join(root, file))

        stats = np.zeros((len(files), 1), dtype=t)
        count = 0
        for file in files:
            f = open(file)
            tempStat = np.array([(file, 0, 0, 0)], dtype=t)

            for line in f:
                word = line.strip().split()
                if word:
                    if word[0] == 'system.cpu.commit.instsCommitted':
                        instsCommitted = (int(word[1]))
                        tempStat[0][1] += instsCommitted
                    elif word[0] == 'system.cpu.commit.branchMispredicts':
                        branchMispredicts = (int(word[1]))
                        tempStat[0][2] += branchMispredicts
                    elif word[0] == 'system.cpu.commit.branches':
                        branches = (int(word[1]))
                        tempStat[0][3] += branches

            stats[count] = tempStat
            count += 1

        w = open('./newFolder/checkpointsBranch/' + write_file, 'w')
        w.write(str(len(stats)) + '\n')
        for i in range(len(stats)):
            mpki = 0
            misRate = 0
            if stats[i][0][3] != 0:
                mpki = format(float(stats[i][0][2]) / float(stats[i][0][1]) * 1000, '.3f')
            if stats[i][0][1] != 0:
                misRate = format(float(stats[i][0][2]) / float(stats[i][0][3]) * 100, '.3f')
            path = stats[i][0][0].split('/')
            w.write(path[2] + '/' + path[3] + ' ')
            w.write(str(stats[i][0][1]) + ' ')
            w.write(str(stats[i][0][2]) + ' ')
            w.write(str(stats[i][0][3]) + ' ')
            w.write(str(mpki) + ' ')
            w.write(str(misRate) + '\n')
        w.close()

def get_stallReason(name):
    np.set_printoptions(formatter={'all': lambda x: str(x)}, threshold=100)

    label = ['NoStall', 'IcacheStall', 'ITlbStall', 'DTlbStall', 'BpStall', 'IntStall', 'TrapStall', 'FragStall',
             'SquashStall', 'FetchBufferInvalid', 'InstMisPred', 'InstSquashed', 'SerializeStall', 'LongExecute',
             'InstNotReady',
             'LoadL1Stall', 'LoadL2Stall', 'LoadL3Stall', 'StoreL1Stall', 'StoreL2Stall', 'StoreL3Stall',
             'ResumeUnblock', 'CommitSquash',
             'Other']

    for i in range(0, 4):
        files = []
        write_file = []
        file_dir = ''

        file_dir = './' + name
        stage = ''

        if i == 0:
            stage = 'fetch'
        elif i == 1:
            stage = 'decode'
        elif i == 2:
            stage = 'rename'
        else:
            stage = 'dispatch'

        for root, dirs, theFiles in os.walk(file_dir):
            for file in theFiles:
                if fnmatch.fnmatch(os.path.join(root, file), '*/stats.txt'):
                    files.append(os.path.join(root, file))

        print(len(files))
        stats = np.zeros((24, len(files)), dtype = np.int32)
        fileIndex = []
        count = 0
        for file in files:
            f = open(file)
            fileIndex.append(file)

            for line in f:
                word = line.strip().split()
                if word:
                    for index in range(0, 24):
                        if word[0] == 'system.cpu.iew.' + stage + 'StallReason::' + label[index]:
                            stats[index][count] += int(word[1])

            count += 1

        #wb = openpyxl.load_workbook('./stallReason/'+ name +'-stalls.xlsx')
        #sheet = wb[stage + 'Stall']

        #bench_name = ['']
        #for index in range(0, count):
        #    tempFile = fileIndex[index].split('/')
        #    bench_name.append(tempFile[2] + '_' + tempFile[3])
        #sheet.append(bench_name)

        #for m in range(0, 24):
        #    sheet.append([str(label[m])] + stats[m].tolist())

        #wb.save('./stallReason/'+ name +'-stalls.xlsx')


        w = open('stallReason/' + name + '-' + stage + '-cpt.txt', 'w')
        w.write(str(len(files)) + '\n')

        for index in range(0, count):
            path = fileIndex[index].split('/')
            w.write(path[2] + '/' + path[3] + ' ')
            for m in range(0, 24):
                w.write(str(stats[m][index]) + ' ')
            w.write('\n')

        w.close()

#get_stallReason('xs-dev-LTAGE')

#get_stallReason('stream')

def get_stats_IPC():
    np.set_printoptions(formatter={'all': lambda x: str(x)}, threshold=100)
    t = np.dtype(
        [('file_name', np.str_, 100), ('instCount', np.int32), ('numCycles', np.int32)])

    for i in range(0, 3):
        files = []
        write_file = []
        file_dir = ''

        if i == 0:
            write_file = 'stream-cpt-stats.txt'
            file_dir = './stream'
        elif i == 1:
            write_file = 'xs-dev-cpt-stats.txt'
            file_dir = './xs-dev'
        else:
            write_file = 'xs-dev-LTAGE-cpt-stats.txt'
            file_dir = './xs-dev-LTAGE'

        for root, dirs, theFiles in os.walk(file_dir):
            for file in theFiles:
                if fnmatch.fnmatch(os.path.join(root, file), '*/stats.txt'):
                    files.append(os.path.join(root, file))

        stats = np.zeros((len(files), 1), dtype=t)
        count = 0
        for file in files:
            f = open(file)
            tempStat = np.array([(file, 0, 0)], dtype=t)

            for line in f:
                word = line.strip().split()
                if word:
                    if word[0] == 'system.cpu.fetch.insts':
                        instsCommitted = (int(word[1]))
                        tempStat[0][1] += instsCommitted
                    elif word[0] == 'system.cpu.fetch.cycles':
                        numCycles = (int(word[1]))
                        tempStat[0][2] += numCycles

            stats[count] = tempStat
            count += 1

        w = open('./newFolder/checkpointsIPC/' + write_file, 'w')
        w.write(str(len(stats)) + '\n')
        for i in range(len(stats)):
            ipc = 0
            if stats[i][0][2] != 0:
                ipc = format(float(stats[i][0][1]) / float(stats[i][0][2]), '.3f')
            path = stats[i][0][0].split('/')
            w.write(path[2] + '/' + path[3] + ' ')
            w.write(str(ipc) + '\n')
        w.close()

get_stats_IPC()
