from jvnpy.agents import Agent
from jvnpy.state import State


class Game:
    def __init__(
        self,
        agent_1: Agent,
        agent_2: Agent,
        state: State,
        rewards={
            (0, 0): (3, 3),
            (0, 1): (0, 5),
            (1, 0): (5, 0),
            (1, 1): (1, 1),
        },
    ) -> None:
        self.rewards = rewards
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.state = state

    def forward(self):
        agent_1_action = self.agent_1.act(self.state)
        agent_2_action = self.agent_2.act(self.state)

        self.state.agent_1_decisions.append(agent_1_action)
        self.state.agent_2_decisions.append(agent_2_action)

        if (agent_1_action, agent_2_action) not in self.rewards:
            raise ValueError("Invalid actions")
        self.state.agent_1_score, self.state.agent_2_score = self.rewards[
            (agent_1_action, agent_2_action)
        ]

        return self.state

    def play_n_rounds(self, n: int):
        for _ in range(n):
            self.forward()
        return self.state
