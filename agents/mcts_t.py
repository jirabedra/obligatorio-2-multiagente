from base.game import AlternatingGame, AgentID, ActionType
from base.agent import Agent
from math import log, sqrt
import numpy as np
from typing import Callable

class MCTSNode:
    def __init__(self, parent: 'MCTSNode', game: AlternatingGame, action: ActionType):
        self.parent = parent
        self.game = game
        self.action = action
        self.children = []
        self.explored_children = 0
        self.visits = 0
        self.value = 0
        self.cum_rewards = np.zeros(len(game.agents))
        self.agent = self.game.agent_selection

def ucb(node, C=sqrt(2)) -> float:
    if node.visits == 0:
        return float('inf')
    agent = node.parent.agent if node.parent is not None else node.agent
    agent_idx = node.game.agent_name_mapping[agent]
    parent_visits = max(node.parent.visits, 1)
    return node.cum_rewards[agent_idx] / node.visits + C * sqrt(log(parent_visits)/node.visits)

def uct(node: MCTSNode, agent: AgentID) -> MCTSNode:
    child = max(node.children, key=ucb)
    return child

class MonteCarloTreeSearch(Agent):
    def __init__(self, game: AlternatingGame, agent: AgentID, simulations: int=100, rollouts: int=10, selection: Callable[[MCTSNode, AgentID], MCTSNode]=uct) -> None:
        """
        Parameters:
            game: alternating game associated with the agent
            agent: agent id of the agent in the game
            simulations: number of MCTS simulations (default: 100)
            rollouts: number of MC rollouts (default: 10)
            selection: tree search policy (default: uct)
        """
        super().__init__(game=game, agent=agent)
        self.simulations = simulations
        self.rollouts = rollouts
        self.selection = selection
        
    def action(self) -> ActionType:
        a, _ = self.mcts()
        return a

    def mcts(self) -> (ActionType, float):

        root = MCTSNode(parent=None, game=self.game.clone(), action=None)

        for i in range(self.simulations):

            node = root

            #print(i)
            #node.game.render()

            # selection
            #print('selection')
            node = self.select_node(node=node)

            # expansion
            #print('expansion')
            num_children = len(node.children)
            self.expand_node(node)
            if len(node.children) > num_children:
                node = node.children[-1]

            # rollout
            #print('rollout')
            rewards = self.rollout(node)

            #update values / Backprop
            #print('backprop')
            self.backprop(node, rewards)

        #print('root childs')
        #for child in root.children:
        #    print(child.action, child.cum_rewards / child.visits)

        action, value = self.action_selection(root)

        return action, value

    def backprop(self, node, rewards):
        # TODO
        # cumulate rewards and visits from node to root navigating backwards through parent
        agent_idx = node.game.agent_name_mapping[self.agent]
        curr_node = node
        while curr_node is not None:
            curr_node.visits += 1
            curr_node.cum_rewards += rewards
            curr_node.value = curr_node.cum_rewards[agent_idx] / curr_node.visits
            curr_node = curr_node.parent

    def rollout(self, node):
        rewards = np.zeros(len(self.game.agents))
        # TODO
        # implement rollout policy
        # for i in range(self.rollouts): 
        #     play random game and record average rewards
        for _ in range(self.rollouts):
            game = node.game.clone()
            while not game.game_over():
                actions = game.available_actions()
                if not actions:
                    break
                action = actions[np.random.randint(len(actions))]
                game.step(action)
            rewards += np.array([game.rewards[agent] for agent in game.agents])
        rewards /= self.rollouts
        return rewards

    def select_node(self, node: MCTSNode) -> MCTSNode:
        curr_node = node
        while not curr_node.game.game_over():
            actions = curr_node.game.available_actions()
            if len(curr_node.children) < len(actions):
                # TODO
                # set curr_node to an unvisited child
                return curr_node
            else:
                # TODO
                # set curr_node to a child using the selection function
                if not curr_node.children:
                    return curr_node
                curr_node = self.selection(curr_node, curr_node.agent)
        return curr_node

    def expand_node(self, node) -> None:
        # TODO
        # if the game is not terminated: 
        #    play an available action in node
        #    create a new child node and add it to node children
        if node.game.game_over():
            return

        actions = node.game.available_actions()
        tried_actions = {child.action for child in node.children}
        untried_actions = [action for action in actions if action not in tried_actions]

        if not untried_actions:
            return

        action = untried_actions[np.random.randint(len(untried_actions))]
        child_game = node.game.clone()
        child_game.step(action)
        child = MCTSNode(parent=node, game=child_game, action=action)
        node.children.append(child)
        node.explored_children = len(node.children)

    def action_selection(self, node: MCTSNode) -> (ActionType, float):
        action: ActionType = None
        value: float = 0
        # TODO
        # hint: return action of child with max value 
        # other alternatives could be considered
        if node.children:
            child = max(node.children, key=lambda child: child.value)
            action = child.action
            value = child.value
        return action, value    