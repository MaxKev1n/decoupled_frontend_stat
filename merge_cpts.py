import numpy as np

def merge_cpts():
    np.set_printoptions(formatter={'all': lambda x: str(x)}, threshold=100)
    t = np.dtype([('file_name', np.str_, 100), ('mpki', np.float32), ('misRate', np.float32)])
    t2 = np.dtype([('file_name', np.str_, 100), ('weight', np.float32), ('coe', np.float32)])

    for i in range(0, 4):
        write_file = []
        read_file = []
        weight_file = 'simpoints06_weights.txt'

        if i == 0:
            write_file = 'decoupled_update_stats.txt'
            read_file = 'decoupled_update_cpt_stats.txt'
        #elif i == 1:
        #    write_file = 'decoupled_last_stats.txt'
        #    read_file = 'decoupled_last_cpt_stats.txt'
        #elif i == 2:
        #    write_file = 'decoupled_stats.txt'
        #    read_file = 'decoupled_cpt_stats.txt'
        else:
            write_file = 'coupled_stats.txt'
            read_file = 'coupled_cpt_stats.txt'

        f1 = open('checkpoint/' + read_file)
        f2 = open(weight_file)

        length = int(f1.readline())
        stats = np.zeros((length, 1), dtype=t)
        weights = np.zeros((int(f2.readline()), 1), dtype=t2)
        workload_set = set()

        count = 0
        count2 = 0

        for line in f2:
            word = line.strip().split()
            tempWeight = np.array([(word[0], float(word[1]), float(word[2]))], dtype=t2)
            weights[count2] = tempWeight
            count2 += 1

        for line in f1:
            word = line.strip().split()
            for line2 in weights:
                if str(line2[0][0]) == str(word[0]):
                    tempStat = np.array(
                        [(word[0], (float(word[4]) * line2[0][1] * line2[0][2]), (float(word[5]) * line2[0][1]))],
                        dtype=t)
                    stats[count] = tempStat
                    break

            count += 1
            workload_set.add(word[0].split('/')[0])

        count3 = 0
        result = np.zeros((len(workload_set), 1), dtype=t)

        for workload in workload_set:
            tempStat = np.array([(str(workload), 0, 0)], dtype=t)
            result[count3] = tempStat
            count3 += 1

        for line in stats:
            cptName = str(line[0][0])
            cpt = cptName.split('/')
            for workload in result:
                if str(workload[0][0]) == str(cpt[0]):
                    workload[0] = np.array([(cpt[0], workload[0][1] + line[0][1], workload[0][2] + line[0][2])],
                                           dtype=t)
                    break

        w = open('workload/' + write_file, 'w')
        w.write(str(len(result)) + '\n')
        for line in result:
            w.write(line[0][0] + ' ')
            w.write(str(line[0][1]) + ' ')
            w.write(str(line[0][2]) + '\n')
        w.close()
