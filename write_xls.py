import openpyxl
import numpy as np

def write_xls():
    np.set_printoptions(formatter={'all': lambda x: str(x)}, threshold=100)

    coupled_mpki = []
    coupled_misRate = []
    #decoupled_mpki = []
    #decoupled_misRate = []
    decoupled_update_mpki = []
    decoupled_update_misRate = []
    #decoupled_last_mpki = []
    #decoupled_last_misRate = []

    for i in range(0, 2):
        read_file = []
        graph_name = []

        if i == 0:
            read_file = 'decoupled_update_stats.txt'
            graph_name = 'decoupled_update'
        #elif i == 1:
        #    read_file = 'decoupled_last_stats.txt'
        #    graph_name = 'decoupled_last'
        #elif i == 2:
        #    read_file = 'decoupled_stats.txt'
        #    graph_name = 'decoupled'
        else:
            read_file = 'coupled_stats.txt'
            graph_name = 'coupled'

        f1 = open('benchmarks/' + read_file)

        length = int(f1.readline())

        workload_name = []
        mpki = []
        misRate = []

        for line in f1:
            stat = line.split()
            workload_name.append(str(stat[0]))
            mpki.append(float(stat[1]))
            misRate.append(float(stat[2]))

        if i == 0:
            decoupled_update_misRate = misRate
            decoupled_update_mpki = mpki
        #elif i == 1:
        #    decoupled_last_misRate = misRate
        #    decoupled_last_mpki = mpki
        #elif i == 2:
        #    decoupled_misRate = misRate
        #    decoupled_mpki = mpki
        else:
            coupled_misRate = misRate
            coupled_mpki = mpki

    wb = openpyxl.load_workbook('xls/MPKI.xlsx')
    sheet = wb['Sheet']

    for i in range(len(decoupled_update_mpki)):
        #sheet.append([str(workload_name[i]), str(decoupled_update_mpki[i]), str(decoupled_last_mpki[i]), str(decoupled_mpki[i]), str(coupled_mpki[i])])
        sheet.append([str(workload_name[i]), str(decoupled_update_mpki[i]), str(coupled_mpki[i])])
    wb.save('xls/MPKI.xlsx')

    wb2 = openpyxl.load_workbook('xls/misRate.xlsx')
    sheet2 = wb2['Sheet']

    for i in range(len(decoupled_update_misRate)):
        #sheet2.append([str(workload_name[i]), str(decoupled_update_misRate[i]), str(decoupled_last_misRate[i]), str(decoupled_misRate[i]), str(coupled_misRate[i])])
        sheet2.append([str(workload_name[i]), str(decoupled_update_misRate[i]), str(coupled_misRate[i])])
    wb2.save('xls/misRate.xlsx')