from enum import Enum
import arcade


# La classe des types d'attaques.
class AttackType(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

# La classe des animations d'attaque.
class AttackAnimation(arcade.Sprite):

    ATTACK_SCALE = 0.5
    ANIMATION_SPEED = 5.0
    ANIMATION_UPDATE_TIME = 1 / ANIMATION_SPEED

    def __init__(self, attackType):

        # Initialiser le sprite.
        super().__init__()

        self.timeSinceLastSwap = 0
        self.attackType = attackType

        # On charge les textures appropriees dependant de attackType.
        if self.attackType == AttackType.ROCK:
            self.textures = [
                arcade.load_texture("assets/srock.png"),
                arcade.load_texture("assets/srock-attack.png"),
            ]
        elif self.attackType == AttackType.PAPER:
            self.textures = [
                arcade.load_texture("assets/spaper.png"),
                arcade.load_texture("assets/spaper-attack.png"),
            ]
        else:
            self.textures = [
                arcade.load_texture("assets/scissors.png"),
                arcade.load_texture("assets/scissors-close.png"),
            ]
        
        # On specifie quelque trucs.
        self.scale = self.ATTACK_SCALE
        self.currentTexture = 0
        self.set_texture(self.currentTexture)

    def on_update(self, deltaTime: float = 1 / 60):

        # Changer la texture, mais attendre un peu avant de ce faire.
        self.timeSinceLastSwap += deltaTime

        if self.timeSinceLastSwap > self.ANIMATION_UPDATE_TIME:

            self.timeSinceLastSwap = 0
            self.currentTexture += 1

            if self.currentTexture < len(self.textures):
                self.set_texture(self.currentTexture)
            else:
                self.currentTexture = 0
                self.set_texture(self.currentTexture)
                
                # C'est fini, l'animation.
                return False
        
        # On continue d'animer.
        return True
    
    

