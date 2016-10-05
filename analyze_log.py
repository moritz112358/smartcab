import pprint
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame, scatter_matrix

line = True
curr_reached, curr_failed = 0,0
latest = 90 #only regard trials starting with this one
curr_alpha, curr_alphadecay, curr_gamma, curr_epsilon, curr_epsilondecay = 0,0,0,0,0
results_list=[]
alpha_list=[]
alphadecay_list=[]
gamma_list=[]
epsilon_list=[]
epsilondecay_list=[]
reached_list=[]
failed_list=[]

f = open('log','r')
while line:
    line = f.readline()
    if 'Alpha' in line:
        curr_alpha = float(line.split()[1])
        curr_alphadecay = float(line.split()[3])
        curr_gamma = float(line.split()[5])
        curr_epsilon = float(line.split()[7])
        curr_epsilondecay = float(line.split()[9])
        #print line
    if 'Simulator.run(): Trial' in line:
        trial_nr = int(line.split()[-1])
        f.readline()
        f.readline()
        success_report = f.readline()
        if trial_nr >= 90:
            if 'reached' in success_report:
                #print trial_nr, "REACHED"
                curr_reached += 1
            else:
                #print trial_nr, "failed"
                curr_failed += 1
    if 'HYPER-PARAMETERS' in line:
        #results_list.append([curr_alpha,curr_gamma, curr_epsilon, curr_reached, curr_failed])
        #print curr_alpha, curr_gamma, curr_epsilon, curr_reached
        alpha_list.append(curr_alpha)
        alphadecay_list.append(curr_alphadecay)
        gamma_list.append(curr_gamma)
        epsilon_list.append(curr_epsilon)
        epsilondecay_list.append(curr_epsilondecay)
        reached_list.append(curr_reached)
        failed_list.append(curr_failed)
        curr_alpha, curr_alphadecay, curr_gamma, curr_epsilon, curr_epsilondecay, curr_reached, curr_failed = 0,0,0,0,0,0,0

#print "total: ",curr_reached, curr_failed

results = DataFrame({'alpha': alpha_list, \
                     'alphadecay': alphadecay_list, \
                     'gamma': gamma_list, \
                     'epsilon': epsilon_list, \
                     'epsilondecay': epsilondecay_list, \
                     'reached': reached_list, \
                     'failed': failed_list})
results['reached'] /= 100.0
results['failed'] /= 100.0

results = results.sort_values(by='reached')
results.to_csv('results_df.txt')
print results
print

for parval in ['alpha', 'alphadecay', 'gamma', 'epsilon', 'epsilondecay' ]:
    print "--", parval, "---------------------------------------------------"
    for val in sorted(set(results[parval])):
        print results[results[parval] == val][['reached', parval]].mean()
        print "---------------------------------------------------------------------"
#res_max = results['reached'].max()
#print "Best result:"
#print results[results['reached'] == res_max]

#scatter_matrix(results, diagonal='kde', color='k', alpha=0.3)
#plt.show()


f.close()