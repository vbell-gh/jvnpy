from matplotlib import pyplot as plt
import numpy as np


class State:
    def __init__(self) -> None:
        self.player_decisions = []
        self.opponent_decisions = []
        self.player_scores = []
        self.opponent_scores = []

    def plot_results(self):
        """
        Plots the game state.
        """
        plt.plot(np.cumsum(self.player_scores), label="Player")
        plt.plot(np.cumsum(self.opponent_scores), label="Opponent")
        plt.style.use("ggplot")
        plt.legend()
        plt.show()
