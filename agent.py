import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

alpha = 1.0
gamma = 0.5
states = []
Q_hat = {}
cycle_count = 0

action_list = [None, 'forward', 'left', 'right']

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        
        # construct states as a list of tuples
        for next_wp in ['left', 'forward', 'right']:
            for left_allowed in [True, False]:
                for forward_allowed in [True, False]:
                    for right_allowed in [True, False]:
                        states.append((next_wp, left_allowed, forward_allowed, right_allowed))
        
        # Initialize Q_hat as a dict from tuples to values, all values initialized as 0
        for s in states:
            for a in action_list:
                Q_hat[(s,a)] = 0
        
        print "States: ",states
        print
        print "Q_hat: ",Q_hat
        
        # Random seed
        random.seed(442)
        
    def reset(self, destination=None):
        global alpha
        global cycle_count
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        cycle_count = 1
        alpha = 1.0 / cycle_count

    def update(self, t):
        global alpha
        global cycle_count
        
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
        
        left_allowed = (inputs['light']=='green') & (inputs['oncoming'] in ['left', None])
        forward_allowed = inputs['light']=='green'
        right_allowed = (inputs['light']=='green') | (inputs['left'] in [None, 'left', 'right'])
        self.state = (self.next_waypoint, left_allowed, forward_allowed, right_allowed)
        
        # TODO: Select action according to your policy
        # == determine max a' of Q_hat(self.state',a')
        # initialize action to random action, then check if there is any action that has higher Q-value and if so, make it the action to do
        action = action_list[random.randint(0,3)] 
        s_prime = self.state
        for a in action_list:
            if Q_hat[(self.state, a)] > Q_hat[(self.state, action)]:
                action = a
        
        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        
        # update Q_hat according to Q-learning update rule. Note that s'=self.state and s=prev_state
        Q_hat[(prev_state, action)] = (1-alpha) * Q_hat[(prev_state, action)] + alpha * (reward + gamma * Q_hat[(self.state,action)])
               
        # update alpha
        cycle_count += 1
        alpha = 1.0 / cycle_count

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""
    
    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # specify agent to track #!!!
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.0, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
