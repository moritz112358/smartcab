import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import pprint

alpha = 0.15 # initial value for alpha
gamma = 0.4
epsilon = 1.0  # initial value for epsilon (i.e. at trial 0)
Q_init = 0.0 #Alternative: optimistic initilization to e.g. 5.0
Q_hat = {}
prev_action = None
cycle_count = 0
decay_alpha = 0.3 # curr_alpha = alpha / (cycle_count)**decay_alpha ... --> set to 0 for no decay
decay_epsilon = 0.7
neg_reward_counter = 0

action_list = [None, 'forward', 'left', 'right']

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""
    
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        
        # construct states as a list of tuples
        states = []
        for next_wp in ['left', 'forward', 'right']:
            for in_light in ['red', 'green']:
                for in_oncoming in [None, 'left', 'forward', 'right']:
                    for in_left in [None, 'left', 'forward', 'right']:
                        states.append((next_wp, in_light, in_oncoming, in_left))
        
        # Initialize Q_hat as a dict from tuples to values
        global Q_hat, Q_init
        for s in states:
            for a in action_list:
                Q_hat[(s,a)] = Q_init
        
        #pprint.pprint(states)
        #print
        #pprint.pprint(Q_hat)
        
        # Random seed
        random.seed(442)
        
    def reset(self, destination=None):
        global cycle_count, prev_action, neg_reward_counter
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        # decay alpha, epsilon
        cycle_count = 0
        prev_action = None
        neg_reward_counter = 0

    def update(self, t):
        global alpha, gamma, cycle_count, Q_hat, prev_action, epsilon, neg_reward_counter
        
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        
        # note previous state (==state before state update)
        if self.state:
            prev_state = self.state
        else: 
            prev_state = ('forward', 'red', None, None)
            print "ONLY AT BEGINNING!"
        
        self.state = (self.next_waypoint, inputs['light'], inputs['oncoming'], inputs['left'])
        
        # TODO: Select action according to your policy
        # decay epsilon
        if cycle_count > 0:
            curr_epsilon = epsilon / ((cycle_count)**decay_epsilon)
        else:
            curr_epsilon = epsilon
        
        # initialize action to random action, then check if there is any action that has higher Q-value and if so, select that action --> determine max a' of Q_hat(self.state',a')
        action = action_list[random.randint(0,3)] 
        if random.random() > curr_epsilon: 
            for a in action_list:
                if Q_hat[(self.state, a)] > Q_hat[(self.state, action)]:
                    action = a
        
        # Execute action and get reward
        reward = self.env.act(self, action)
        
        # count negative rewards
        if reward < 0:
            neg_reward_counter += 1
        
        # TODO: Learn policy based on state, action, reward
        # calculate alpha decay
        if cycle_count > 0:
            curr_alpha = alpha / ((cycle_count)**decay_alpha)
        else:
            curr_alpha = alpha
        # update Q_hat according to Q-learning update rule. Note that s'=self.state and s=prev_state
        # likewise, a=prev_action and a'=action (as determined above) as the action, that maximises Q for current state
        Q_hat[(prev_state, prev_action)] = (1 - curr_alpha) * Q_hat[(prev_state, prev_action)] + curr_alpha * (reward + gamma * Q_hat[(self.state,action)])
        
        # update cycle_count for decaying alpha, epsilon
        cycle_count += 1
        
        # store previous action
        prev_action = action
        
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""
    
    #MY CODE:
    global alpha, gamma, epsilon, decay_alpha, decay_epsilon
    for alpha in [0.1, 0.15, 0.2, 0.3]:
        for decay_alpha in [0.3, 0.4]:
            for gamma in [0.3, 0.4]:
                for epsilon in [0.03, 0.05]:
                    for decay_epsilon in [0.3, 0.4, 0.5 ]:
                        for multiple_runs in range(10):
                            # Set up environment and agent
                            e = Environment()  # create environment (also adds some dummy traffic)
                            a = e.create_agent(LearningAgent)  # create agent
                            e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track #!!!
                            # NOTE: You can set enforce_deadline=False while debugging to allow longer trials
                            
                            # Now simulate it
                            sim = Simulator(e, update_delay=0.0, display=False)  # create simulator (uses pygame when display=True, if available)
                            # NOTE: To speed up simulation, reduce update_delay and/or set display=False
                            
                            sim.run(n_trials=100)  # run for a specified number of trials
                            # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
                            
                            #MY CODE:
                            #global Q_hat
                            #pprint.pprint(Q_hat)
                            print "Alpha:", alpha, "Alphadecay:", decay_alpha, " Gamma:", gamma, " Epsilon:",epsilon, "Epsilondecy:", decay_epsilon, "NegRewards:", neg_reward_counter
                        print "NEW SET OF HYPER-PARAMETERS"
                        

if __name__ == '__main__':
    run()
