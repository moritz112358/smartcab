import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import pprint

alpha = 0.1
gamma = 0.2
epsilon = 0.05
Q_init = 0.0
Q_hat = {}
cycle_count = 0
prev_action = None

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
            #SIMPLIFIED STATES
            #for wp_allowed in [True, False]:
            #    states.append((next_wp, wp_allowed))
            for left_allowed in [True, False]:
                for forward_allowed in [True, False]:
                    for right_allowed in [True, False]:
                        states.append((next_wp, left_allowed, forward_allowed, right_allowed))
        
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
        global alpha, cycle_count, prev_action
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        # decay learning rate alpha
        cycle_count = 1
        #alpha = 1.0 / cycle_count
        prev_action = None

    def update(self, t):
        global alpha, gamma, cycle_count, Q_hat, prev_action, epsilon
        
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        
        # note previous state (==state before state update)
        if self.state:
            prev_state = self.state
        else: 
            prev_state = ('forward', False, False, False)
            print "ONLY AT BEGINNING!"
        
        left_allowed = (inputs['light']=='green') and (inputs['oncoming'] in ['left', None])
        forward_allowed = inputs['light']=='green'
        right_allowed = (inputs['light']=='green') or (inputs['left'] in [None, 'left', 'right'])
        self.state = (self.next_waypoint, left_allowed, forward_allowed, right_allowed)
        
        #SIMPLIFIED STATES
        #if self.next_waypoint == 'left':
        #    wp_allowed = left_allowed
        #elif self.next_waypoint == 'forward':
        #    wp_allowed = forward_allowed
        #elif self.next_waypoint == 'right':
        #    wp_allowed = right_allowed
        #self.state = (self.next_waypoint, wp_allowed)
        
        # TODO: Select action according to your policy
        # == determine max a' of Q_hat(self.state',a')
        # initialize action to random action, then check if there is any action that has higher Q-value and if so, select that action
        
        action = action_list[random.randint(0,3)] 
        if random.random() > epsilon: #
            for a in action_list:
                if Q_hat[(self.state, a)] > Q_hat[(self.state, action)]:
                    action = a
        
        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        
        # update Q_hat according to Q-learning update rule. Note that s'=self.state and s=prev_state
        Q_hat[(prev_state, prev_action)] = (1-alpha) * Q_hat[(prev_state, prev_action)] + alpha * (reward + gamma * Q_hat[(self.state,action)])
               
        # update alpha
        cycle_count += 1
        #alpha = 1.0 / cycle_count
        
        # store previous action
        prev_action = action
        
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""
    
    #MY CODE:
    global alpha, gamma, epsilon
    for alpha in [0.05,0.1,0.2,0.4]:
        for gamma in [0.05,0.1,0.2,0.4]:
            for epsilon in [0.025,0.05]:
                print "NEW SET OF HYPER-PARAMETERS"
                for multiple_runs in range(100):
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
                    print "Alpha:", alpha, " Gamma:", gamma, " Epsilon:",epsilon


if __name__ == '__main__':
    run()
