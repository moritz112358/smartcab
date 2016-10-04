import pprint
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame, scatter_matrix

line = True
curr_reached, curr_failed = 0,0
latest = 90 #only regard trials starting with this one
curr_alpha, curr_gamma, curr_epsilon = 0,0,0
results_list=[]
alpha_list=[]
gamma_list=[]
epsilon_list=[]
reached_list=[]
failed_list=[]
print "Alpha Gamma Epsilon Success_rate Failure_rate"

f = open('log','r')
while line:
    line = f.readline()
    if 'Alpha' in line:
        curr_alpha = float(line.split()[1])
        curr_gamma = float(line.split()[3])
        curr_epsilon = float(line.split()[5])
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
        gamma_list.append(curr_gamma)
        epsilon_list.append(curr_epsilon)
        reached_list.append(curr_reached)
        failed_list.append(curr_failed)
        curr_alpha, curr_gamma, curr_epsilon, curr_reached, curr_failed = 0,0,0,0,0

#print "total: ",curr_reached, curr_failed

results = DataFrame({'alpha': alpha_list, \
                     'gamma': gamma_list, \
                     'epsilon': epsilon_list, \
                     'reached': reached_list, \
                     'failed': failed_list})
results['reached'] /= 10.0
results['failed'] /= 10.0

print results

#plt.scatter(results['alpha'],results['reached'])
scatter_matrix(results, diagonal='kde', color='k', alpha=0.3)
plt.show()

#fig = plt.figure()
#ax1 = fig.add_subplot(2,2,1)
#ax2 = fig.add_subplot(2,2,2)
#ax3 = fig.add_subplot(2,2,3)
#ax4 = fig.add_subplot(2,2,4)
#
#ax1.scatter(results['alpha'],results['reached'], 'ko--')
#
#plt.plot.show()

f.close()