import numpy as np
import os
import fnmatch

def get_stats():
    np.set_printoptions(formatter={'all': lambda x: str(x)}, threshold=100)
    t = np.dtype(
        [('file_name', np.str_, 100), ('instCount', np.int32), ('branchMisCount', np.int32), ('branches', np.int32)])

    for i in range(0, 2):
        files = []
        write_file = []
        file_dir = ''

        if i == 0:
            write_file = 'decoupled_update_cpt_stats.txt'
            file_dir = './decoupled_update'
        #elif i == 1:
        #    write_file = 'decoupled_last_cpt_stats.txt'
        #    file_dir = './decoupled_last'
        #elif i == 2:
        #    write_file = 'decoupled_cpt_stats.txt'
        #    file_dir = './decoupled_ori'
        else:
            write_file = 'coupled_cpt_stats.txt'
            file_dir = './coupled'

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
                    elif word[0] == 'system.cpu.branchPred.indirectMispredicted':
                        branches = (int(word[1]))
                        tempStat[0][3] += branches

            stats[count] = tempStat
            count += 1

        w = open('checkpoint/' + write_file, 'w')
        w.write(str(len(stats)) + '\n')
        for i in range(len(stats)):
            mpki = 0
            misRate = 0
            if stats[i][0][1] != 0:
                mpki = format((float(stats[i][0][2]) - float(stats[i][0][3])) / float(stats[i][0][1]) * 1000, '.3f')
                misRate = format(float(stats[i][0][3]) / float(stats[i][0][1]) * 1000, '.3f')
            path = stats[i][0][0].split('/')

            w.write(path[2] + '/' + path[3] + ' ')
            w.write(str(stats[i][0][1]) + ' ')
            w.write(str(stats[i][0][2]) + ' ')
            w.write(str(stats[i][0][3]) + ' ')
            w.write(str(mpki) + ' ')
            w.write(str(misRate) + '\n')
        w.close()


