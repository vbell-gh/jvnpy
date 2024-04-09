from abc import ABC, abstractmethod
import random

from jvnpy.state import State


class Agent(ABC):
    @abstractmethod
    def act(self, state: State, role) -> int:
        pass


class RandomAgent(Agent):
    def act(self, state, role: str):
        return random.randint(0, 1)


class PositiveAgent(Agent):
    def act(self, state, role: str):
        return 1


class NegativeAgent(Agent):
    def act(self, state, role: str):
        return 0


class MainlyPositiveAgent(Agent):
    def act(self, state, role: str):
        return random.choices([0, 1], weights=[0.1, 0.9])[0]


class MainlyNegativeAgent(Agent):
    def act(self, state, role: str):
        return random.choices([0, 1], weights=[0.9, 0.1])[0]


class TitForTatAgent(Agent):
    def act(self, state, role: str):
        if len(state.opponent_decisions) == 0:
            return 1
        elif role == "player":
            return state.opponent_decisions[-1]
        elif role == "opponent":
            return state.player_decisions[-1]


class ProbabilityTitForTatAgent(Agent):
    def __init__(self, p=0.1):
        self.p = p

    def act(self, state, role: str):
        if len(state.opponent_decisions) == 0:
            return 1
        elif role == "player":
            if state.opponent_decisions[-1] == 1 and random.random() < self.p:
                return 0
            else:
                return state.opponent_decisions[-1]
        elif role == "opponent":
            if state.player_decisions[-1] == 1 and random.random() < self.p:
                return 0
            else:
                return state.player_decisions[-1]


class VindictiveAgent(Agent):
    def act(self, state, role: str):
        if len(state.opponent_decisions) == 0:
            return 1
        elif role == "player":
            if 0 in state.opponent_decisions:
                return 0
            else:
                return 1
        elif role == "opponent":
            if 0 in state.player_decisions:
                return 0
            else:
                return 1
