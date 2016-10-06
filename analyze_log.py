import pprint
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame, scatter_matrix

EVAL_SUCCESS_AFTER_N_TRIALS = 90

line = True
curr_reached, curr_failed = 0,0
latest = 90 #only regard trials starting with this one
curr_alpha, curr_alphadecay, curr_gamma, curr_epsilon, curr_epsilondecay, curr_negrew = 0,0,0,0,0,0
results_list=[]
alpha_list=[]
alphadecay_list=[]
gamma_list=[]
epsilon_list=[]
epsilondecay_list=[]
reached_list=[]
failed_list=[]
cumulrew_list=[]

f = open('log','r')
while line:
    line = f.readline()
    if 'Alpha' in line:
        curr_alpha = float(line.split()[1])
        curr_alphadecay = float(line.split()[3])
        curr_gamma = float(line.split()[5])
        curr_epsilon = float(line.split()[7])
        curr_epsilondecay = float(line.split()[9])
        curr_cumulrew = float(line.split()[11])
        #print line
    
    if 'Simulator.run(): Trial' in line:
        trial_nr = int(line.split()[-1])
        leave = False
        while not leave: 
            in_trial_line = f.readline()
            if 'Negative_reward' in in_trial_line:
                if trial_nr >= 90:
                    curr_negrew += 1
            if 'reached' in in_trial_line:
                if trial_nr >= EVAL_SUCCESS_AFTER_N_TRIALS:
                    curr_reached += 1
                leave = True
            if 'aborted' in in_trial_line:
                if trial_nr >= EVAL_SUCCESS_AFTER_N_TRIALS:
                    curr_failed += 1
                leave = True
                
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
        cumulrew_list.append(curr_cumulrew)
        curr_alpha, curr_alphadecay, curr_gamma, curr_epsilon, curr_epsilondecay, curr_reached, curr_failed, curr_cumulrew = 0,0,0,0,0,0,0,0

#print "total: ",curr_reached, curr_failed

results = DataFrame({'alpha': alpha_list, \
                     'decay_alpha': alphadecay_list, \
                     'gamma': gamma_list, \
                     'epsilon': epsilon_list, \
                     'decay_epsilon': epsilondecay_list, \
                     'reached': reached_list, \
                     'xfailed': failed_list, \
                     'ycumulrew': cumulrew_list})
#results['reached'] /= 100.0 * (100-EVAL_SUCCESS_AFTER_N_TRIALS)
#results['xfailed'] /= 100.0 * (100-EVAL_SUCCESS_AFTER_N_TRIALS)

results['reached'] /= 1000.0
results = results.sort_values(by='reached')
results.to_csv('results_df.txt')
print results
print
print results[results.alpha==0.3][results.decay_alpha==0.3][results.gamma==0.3][results.epsilon==0.05]
print

for parval in ['alpha', 'decay_alpha', 'gamma', 'epsilon', 'decay_epsilon' ]:
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