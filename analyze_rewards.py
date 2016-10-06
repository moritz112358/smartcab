import pprint
import pandas as pd
#create dict and initialize to zero
rewards_per_trial = {}
for l in range(100):
    rewards_per_trial[l] = 0

    
    
f = open('log_rew','r')

for line in f:
    if 'Simulator.run(): Trial' in line:
        curr_trial = int(line.split()[2])
    if 'Cumul_reward for previous' in line:
        curr_reward = float(line.split()[4])
        rewards_per_trial[curr_trial] = rewards_per_trial[curr_trial] + curr_reward

#pprint.pprint(rewards_per_trial)

df = pd.Series(rewards_per_trial).drop(0)
print df/100.

print df[89:99].mean()/100.

f.close()