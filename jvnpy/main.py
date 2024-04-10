from collections import namedtuple
from typing import Optional

from jvnpy.agents import Agent
from jvnpy.state import State


class Rewards:
    """ The Class Rewards is used to define the rewards for the game.
        The rewards can be customized

    Returns:
        Scores, which is a named tuple with the player and opponent rewards based
    """
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
    """
    Represents a game between two agents.

    Args:
        player (Agent): The player agent.
        opponent (Agent): The opponent agent.
        state (State): The initial state of the game.
        rewards (Optional[Rewards]): The rewards class for the game. If None, default rewards will be used.

    Attributes:
        rewards (Rewards): The rewards class for the game.
        player (Agent): The player agent.
        opponent (Agent): The opponent agent.
        state (State): The current state of the game.

    Methods:
        forward(): Advances the game by one step, returns the state.
        play_n_rounds(n: int): Plays the game for n rounds, returns the state.

    """

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
        """
        Advances the game by one step.

        Returns:
            State: The state of the game.

        Raises:
            ValueError: If the combination of player and opponent actions is invalid.
        """
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
        """
        Plays the game for n rounds.

        Args:
            n (int): The number of rounds to play.

        Returns:
            State: The state of the game.

        """
        try:
            for _ in range(n):
                self.state = self.forward()
        except ValueError as e:
            print("Error: ", e)
        return self.state
