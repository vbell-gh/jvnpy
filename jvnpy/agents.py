from abc import ABC, abstractmethod
import random

from jvnpy.state import State


class Agent(ABC):
    @abstractmethod
    def act(self, state: State) -> int:
        pass


class RandomAgent(Agent):
    def act(self, state):
        return random.randint(0, 1)


class PositiveAgent(Agent):
    def act(self, state):
        return 1


class NegativeAgent(Agent):
    def act(self, state):
        return 0


class OccasionalNegativeAgent(Agent):
    def act(self, state):
        return random.choices([0, 1], weights=[0.1, 0.9])[0]


class OccasionalPositiveAgent(Agent):
    def act(self, state):
        return random.choices([0, 1], weights=[0.9, 0.1])[0]


class TitForTatAgent(Agent):
    def act(self, state):
        if len(state.opponent_decisions) == 0:
            return 1
        return state.opponent_decisions[-1]
