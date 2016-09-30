import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        
        # Initialize Q_hat
        alpha = 0.5
        gamma = 0.5
        Q_hat = {}
        for next_wp in ['left', 'forward', 'right']:
            for left_allowed in [True, False]:
                for forward_allowed in [True, False]:
                    for right_allowed in [True, False]:
                        #s = [next_wp, left_allowed, forward_allowed, right_allowed]
                        for a in [None, 'forward', 'left', 'right']:
                            Q_hat[(next_wp, left_allowed, forward_allowed, right_allowed,a)] = 0
        
        print Q_hat
        
        # Random seed
        random.seed(442)
        
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        left_allowed = (inputs['light']=='green') & (inputs['oncoming'] in ['left', None])
        forward_allowed = inputs['light']=='green'
        right_allowed = (inputs['light']=='green') | (inputs['left'] in [None, 'left', 'right'])
        self.state = [self.next_waypoint, left_allowed, forward_allowed, right_allowed]
        
        # TODO: Select action according to your policy
        
        # random action (for "Implement basic driving agent")
        action_list = [None, 'forward', 'left', 'right']
        action = action_list[random.randint(0,3)]

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        
        # determine max a' of Q_hat(s',a')
        max_aprime = 0 #max()
        
        Q_hat[self.next_waypoint, left_allowed, forward_allowed, right_allowed] = \
            (1-alpha) * Q_hat[self.next_waypoint, left_allowed, forward_allowed, right_allowed] + \
                alpha * (reward + gamma * max_aprime)

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""
    
    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # specify agent to track #!!!
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=2.0, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
