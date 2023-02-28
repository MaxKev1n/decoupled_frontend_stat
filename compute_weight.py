import json

simpoints_file = './gcb-06-o2-summary.json'

names = []
weights = []
coes = []

with open(simpoints_file) as jf:
    simpoints = json.load(jf)
    for workload in simpoints:
        total = 0
        tempWeights = []
        for key in simpoints[workload]:
            names.append(workload + '/' + key)
            tempWeights.append(simpoints[workload][key])
            total += float(simpoints[workload][key])
        coe = 1 / total
        for weight in tempWeights:
            weights.append(weight)
            coes.append(coe)

w = open('weight/gcb-06-o2-summary.txt', 'w')
w.write(str(len(names)) + '\n')
for i in range(0, len(names)):
    w.write(names[i] + ' ')
    w.write(str(weights[i]) + ' ')
    w.write(str(coes[i]) + '\n')
w.close()
