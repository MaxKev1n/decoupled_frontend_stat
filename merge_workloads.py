import numpy as np

def merge_workloads():
    np.set_printoptions(formatter={'all': lambda x: str(x)}, threshold=100)
    t = np.dtype([('benchmark_name', np.str_, 100), ('workload_name', np.str_, 100), ('number', np.int_), ('coe', np.float_), ('benchmark_full_name', np.str_, 100)])
    t1 = np.dtype([('benchmark_name', np.str_, 100), ('number', np.int_), ('mpki', np.float_), ('misRate', np.float_)])
    t2 = np.dtype([('file_name', np.str_, 100), ('weight', np.float32), ('coe', np.float32)])

    for i in range(0, 2):
        write_file = []
        read_file = []
        weight_file = 'simpoints_06.txt'

        if i == 0:
            write_file = 'decoupled_update_stats.txt'
            read_file = 'decoupled_update_stats.txt'
        else:
            write_file = 'coupled_stats.txt'
            read_file = 'coupled_stats.txt'

        f1 = open('workload/' + read_file)
        f2 = open(weight_file)

        length = int(f1.readline())
        benchmarks = np.zeros((length, 1), dtype=t)
        benchmarks_num = np.zeros((length, 1), dtype=t1)
        weights = np.zeros((int(f2.readline()), 1), dtype=t2)
        workload_set = set()

        count = 0
        count2 = 0

        for line in f2:
            fullName = line.strip().split()[0]
            firstName = line.strip().split('_')
            instNum = 0
            benchmarkName = firstName[0]
            secondName = ''
            if len(firstName) > 1:
                secondName = firstName[1].split()[0]
                instNum = int(firstName[1].split()[1])
            else:
                instNum = int((firstName[0].split())[1])
                benchmarkName = (firstName[0].split())[0]

            tempBenchMark = np.array([(benchmarkName, secondName, instNum, float(0), fullName)], dtype=t)
            benchmarks[count2] = tempBenchMark
            count2 += 1

            exist = False
            for bench in benchmarks_num:
                if tempBenchMark[0][0] == bench[0][0]:
                    bench[0][1] += tempBenchMark[0][2]
                    exist = True
                    break

            if not exist:
                tempBench = np.array([(tempBenchMark[0][0], tempBenchMark[0][2], 0, 0)], dtype=t1)
                benchmarks_num[count] = tempBench
                count += 1

            if count2 == length:
                break

        benchmarks_num = benchmarks_num[0:count,:]

        for bench in benchmarks:
            for benchNum in benchmarks_num:
                if bench[0][0] == benchNum[0][0]:
                    bench[0][3] = bench[0][2] / benchNum[0][1]
                    break;

        for line in f1:
            workloadName = line.strip().split()[0]
            mpki = line.strip().split()[1]
            misRate = line.strip().split()[2]
            for bench in benchmarks:
                if bench[0][4] == workloadName:
                    for benchNum in benchmarks_num:
                        if benchNum[0][0] == bench[0][0]:
                            benchNum[0][2] += float(mpki) * bench[0][3]
                            benchNum[0][3] += float(misRate) * bench[0][3]
                            break
                    break

        w = open('benchmarks/' + write_file, 'w')
        w.write(str(len(benchmarks_num)) + '\n')
        for line in benchmarks_num:
            w.write(line[0][0] + ' ')
            w.write(str(line[0][2]) + ' ')
            w.write(str(line[0][3]) + '\n')
        w.close()