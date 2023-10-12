from enum import Enum


# Enum pour l'etat du jeu.
class GameState(Enum):
    ROUND_DONE = 1
    GAME_OVER = 2
    NOT_STARTED = 3
    ROUND_ACTIVE = 4
