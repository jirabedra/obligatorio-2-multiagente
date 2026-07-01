import numpy as np
from numpy import ndarray
from base.game import AlternatingGame, AgentID, ObsType
from base.agent import Agent

class Node():

    def __init__(self, game: AlternatingGame, obs: ObsType) -> None:
        self.game = game
        self.agent = game.agent_selection
        self.obs = obs
        self.num_actions = self.game.num_actions(self.agent)
        self.legal_actions = self.game.available_actions()
        self.action_mask = np.zeros(self.num_actions)
        self.action_mask[self.legal_actions] = 1
        self.cum_regrets = np.zeros(self.num_actions)
        self.curr_policy = self.uniform_legal_policy()
        self.sum_policy = self.curr_policy.copy()
        self.learned_policy = self.curr_policy.copy()
        self.niter = 1

    def uniform_legal_policy(self):
        policy = np.zeros(self.num_actions)
        policy[self.legal_actions] = 1 / len(self.legal_actions)
        return policy

    def regret_matching(self):
        # TODO
        positive_regrets = np.maximum(self.cum_regrets, 0) * self.action_mask
        normalizer = positive_regrets.sum()

        if normalizer > 0:
            self.curr_policy = positive_regrets / normalizer
        else:
            self.curr_policy = self.uniform_legal_policy()

        policy_sum = self.sum_policy.sum()
        if policy_sum > 0:
            self.learned_policy = self.sum_policy / policy_sum
        else:
            self.learned_policy = self.curr_policy.copy()
    
    def update(self, action_values, state_value, probability) -> None:
        # update 
        # ...
        agent_idx = self.game.agent_name_mapping[self.agent]
        counterfactual_probability = np.prod(np.delete(probability, agent_idx))

        self.cum_regrets += counterfactual_probability * (action_values - state_value) * self.action_mask
        self.sum_policy += probability[agent_idx] * self.curr_policy
        self.niter += 1

        # regret matching policy
        self.regret_matching()  

    def policy(self):
        return self.learned_policy

class CounterFactualRegret(Agent):

    def __init__(self, game: AlternatingGame, agent: AgentID) -> None:
        super().__init__(game, agent)
        self.node_dict: dict[ObsType, Node] = {}
        self.warn_on_missing_node = False

    def action(self):
        try:
            node = self.node_dict[self.game.observe(self.agent)]
            a = np.argmax(np.random.multinomial(1, node.policy(), size=1))
            return a
        except:
            #raise ValueError('Train agent before calling action()')
            if self.warn_on_missing_node:
                print('Node does not exist. Playing random.')
            return np.random.choice(self.game.available_actions())
    
    def train(self, niter=1000):
        for _ in range(niter):
            _ = self.cfr()

    def cfr(self):
        game = self.game.clone()
        state_values: dict[AgentID, float] = dict()
        for agent in self.game.agents:
            game.reset()
            probability = np.ones(game.num_agents)
            state_values[agent] = self.cfr_rec(game=game, agent=agent, probability=probability)

        return state_values 

    def cfr_rec(self, game: AlternatingGame, agent: AgentID, probability: ndarray):
        # TODO
        if game.terminated():
            return game.reward(agent)

        curr_agent = game.agent_selection
        curr_agent_idx = game.agent_name_mapping[curr_agent]
        obs = game.observe(curr_agent)

        if obs not in self.node_dict:
            self.node_dict[obs] = Node(game=game, obs=obs)

        node = self.node_dict[obs]
        policy = node.curr_policy.copy()
        action_values = np.zeros(node.num_actions)

        for action in game.available_actions():
            next_game = game.clone()
            next_game.step(action)

            next_probability = probability.copy()
            next_probability[curr_agent_idx] *= policy[action]

            action_values[action] = self.cfr_rec(
                game=next_game,
                agent=agent,
                probability=next_probability,
            )

        state_value = np.dot(policy, action_values)

        if curr_agent == agent:
            node.update(
                action_values=action_values,
                state_value=state_value,
                probability=probability,
            )

        return state_value
        
