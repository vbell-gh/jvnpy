from collections import namedtuple
from typing import Optional

from jvnpy.agents import Agent
from jvnpy.state import State


class Rewards:
    Scores = namedtuple("Score", ["player", "opponent"])

    def __init__(
        self, both_1=(3, 3), both_0=(1, 1), player_0_opponent_1=(0, 5)
    ) -> None:
        self.rewards = {
            (1, 1): Rewards.Scores(player=both_1[0], opponent=both_1[1]),
            (0, 0): Rewards.Scores(player=both_0[0], opponent=both_0[1]),
            (1, 0): Rewards.Scores(
                player=player_0_opponent_1[0], opponent=player_0_opponent_1[1]
            ),
            (0, 1): Rewards.Scores(
                player=player_0_opponent_1[1], opponent=player_0_opponent_1[0]
            ),
        }

    def get_rewards(self):
        return self.rewards


class Game:
    def __init__(
        self,
        player: Agent,
        opponent: Agent,
        state: State,
        rewards: Optional[
            Rewards
        ] = None,  # If rewards is None, we will use the default rewards
    ) -> None:
        self.rewards = rewards
        self.player = player
        self.opponent = opponent
        self.state = state

        if rewards is None:
            self.rewards = Rewards().get_rewards()  # Use the default rewards
        else:
            self.rewards = rewards.get_rewards()  # Use the custom rewards class

    def forward(self):
        # Pass the state to the agents
        player_action = self.player.act(self.state, role="player")
        opponent_action = self.opponent.act(self.state, role="opponent")

        # Check if the combination of actions is valid
        if (player_action, opponent_action) not in self.rewards:
            raise ValueError("Invalid actions")

        # Update the scores and decisions to the state
        self.state.player_scores.append(
            self.rewards[(player_action, opponent_action)].player
        )
        self.state.opponent_scores.append(
            self.rewards[(player_action, opponent_action)].opponent
        )

        self.state.player_decisions.append(player_action)
        self.state.opponent_decisions.append(opponent_action)
        return self.state

    def play_n_rounds(self, n: int):
        try:
            for _ in range(n):
                self.state = self.forward()
        except ValueError as e:
            print("Error: ", e)
        return self.state
