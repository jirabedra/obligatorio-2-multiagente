from __future__ import annotations

from math import log, sqrt

import numpy as np

from base.agent import Agent
from base.game import ActionType, AgentID, AlternatingGame, ObsType


class ISMCTSNode:
    def __init__(
        self,
        parent: ISMCTSNode | None,
        agent: AgentID,
        obs: ObsType | None,
        num_agents: int,
        action: ActionType | None = None,
    ) -> None:
        self.parent = parent
        self.agent = agent
        self.obs = obs
        self.action = action
        self.children: dict[ActionType, ISMCTSNode] = {}
        self.visits = 0
        self.cum_rewards = np.zeros(num_agents)


class InformationSetMCTS(Agent):
    def __init__(
        self,
        game: AlternatingGame,
        agent: AgentID,
        simulations: int = 100,
        rollouts: int = 1,
        exploration: float = sqrt(2),
    ) -> None:
        super().__init__(game=game, agent=agent)
        self.simulations = simulations
        self.rollouts = rollouts
        self.exploration = exploration

    def action(self) -> ActionType:
        action, _ = self.ismcts()
        if action is None:
            return np.random.choice(self.game.available_actions())
        return action

    def ismcts(self) -> tuple[ActionType | None, float]:
        root = ISMCTSNode(
            parent=None,
            agent=self.game.agent_selection,
            obs=self.game.observe(self.game.agent_selection),
            num_agents=len(self.game.agents),
        )

        for _ in range(self.simulations):
            game = self.determinization()

            # selection
            node, game = self.select_node(root, game)

            # expansion
            node, game = self.expand_node(node, game)

            # rollout
            rewards = self.rollout(game)

            # backpropagation
            self.backprop(node, rewards)

        return self.action_selection(root)

    def determinization(self) -> AlternatingGame:
        if hasattr(self.game, "random_change"):
            return self.game.random_change(self.agent)
        return self.game.clone()

    def select_node(
        self,
        node: ISMCTSNode,
        game: AlternatingGame,
    ) -> tuple[ISMCTSNode, AlternatingGame]:
        curr_node = node
        curr_game = game

        while not curr_game.game_over():
            actions = curr_game.available_actions()
            untried_actions = self.untried_actions(curr_node, actions)
            if untried_actions:
                return curr_node, curr_game

            action = max(actions, key=lambda action: self.ucb(curr_node, curr_node.children[action]))
            curr_game = curr_game.clone()
            curr_game.step(action)
            curr_node = curr_node.children[action]

        return curr_node, curr_game

    def expand_node(
        self,
        node: ISMCTSNode,
        game: AlternatingGame,
    ) -> tuple[ISMCTSNode, AlternatingGame]:
        if game.game_over():
            return node, game

        actions = game.available_actions()
        untried_actions = self.untried_actions(node, actions)
        if not untried_actions:
            return node, game

        action = np.random.choice(untried_actions)
        next_game = game.clone()
        next_game.step(action)
        child = ISMCTSNode(
            parent=node,
            agent=next_game.agent_selection,
            obs=None if next_game.game_over() else next_game.observe(next_game.agent_selection),
            num_agents=len(self.game.agents),
            action=action,
        )
        node.children[action] = child
        return child, next_game

    def untried_actions(self, node: ISMCTSNode, actions: list[ActionType]) -> list[ActionType]:
        untried_actions = [action for action in actions if action not in node.children]
        return untried_actions

    def ucb(self, parent: ISMCTSNode, child: ISMCTSNode) -> float:
        if child.visits == 0:
            return float("inf")
        agent_idx = self.game.agent_name_mapping[parent.agent]
        exploitation = child.cum_rewards[agent_idx] / child.visits
        exploration = self.exploration * sqrt(log(max(parent.visits, 1)) / child.visits)
        return exploitation + exploration

    def rollout(self, game: AlternatingGame) -> np.ndarray:
        total_rewards = np.zeros(len(self.game.agents))
        for _ in range(self.rollouts):
            rollout_game = game.clone()
            while not rollout_game.game_over():
                actions = rollout_game.available_actions()
                action = np.random.choice(actions)
                rollout_game.step(action)
            total_rewards += np.array([rollout_game.reward(agent) for agent in rollout_game.agents])
        return total_rewards / self.rollouts

    def backprop(self, node: ISMCTSNode, rewards: np.ndarray) -> None:
        curr_node = node
        while curr_node is not None:
            curr_node.visits += 1
            curr_node.cum_rewards += rewards
            curr_node = curr_node.parent

    def action_selection(self, root: ISMCTSNode) -> tuple[ActionType | None, float]:
        if not root.children:
            return None, 0.0
        child = max(root.children.values(), key=lambda node: node.visits)
        agent_idx = self.game.agent_name_mapping[self.agent]
        return child.action, child.cum_rewards[agent_idx] / child.visits
