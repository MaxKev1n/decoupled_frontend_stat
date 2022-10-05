import matplotlib
import numpy as np
from matplotlib.ticker import MultipleLocator

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use("ggplot")

np.set_printoptions(formatter={'all':lambda x: str(x)},threshold=100)

coupled_mpki= []
coupled_misRate = []
decoupled_mpki= []
decoupled_misRate = []

for i in range(0,2):
    read_file = []
    graph_name = []

    if i == 0:
        read_file = 'decoupled_stats.txt'
        graph_name = 'decoupled'
    else:
        read_file = 'coupled_stats.txt'
        graph_name = 'coupled'

    f1 = open('workload/' + read_file)

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
        decoupled_misRate = misRate
        decoupled_mpki = mpki
    else:
        coupled_misRate = misRate
        coupled_mpki = mpki


plt.figure(figsize=(24, 15), dpi=80)
x_ticks = range(len(workload_name))
plt.bar(x_ticks, decoupled_misRate, width=0.4, label='decoupled')
plt.bar([i + 0.4 for i in x_ticks], coupled_misRate, width=0.4, label='coupled')
plt.legend()
plt.xticks(x_ticks, workload_name)
plt.xticks(rotation=90)
#plt.title('Mispredicted Rate')
plt.savefig('graph/misRate', bbox_inches='tight')
plt.clf()

plt.figure(figsize=(24, 15), dpi=80)
x_ticks = range(len(workload_name))
plt.bar(x_ticks, decoupled_mpki, width=0.4, label='decoupled')
plt.bar([i + 0.4 for i in x_ticks], coupled_mpki, width=0.4, label='coupled')
plt.legend()
plt.xticks(x_ticks, workload_name)
plt.xticks(rotation=90)
#plt.title('MPKI')
plt.savefig('graph/mpki', bbox_inches='tight')
plt.clf()
