import random
import arcade
#import arcade.gui

from attack_animation import AttackType, AttackAnimation
from game_state import GameState

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45  # The default line height for text.


# La classe principale de l'application. Notez que j'ai fait des modifications a la base. Je n'ai pas utilise les dictionnaires, notamment.
class MyGame(arcade.Window):
   
   PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
   PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
   COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
   COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5
   ATTACK_FRAME_WIDTH = 154 / 2
   ATTACK_FRAME_HEIGHT = 154 / 2

   def __init__(self, width, height, title):
       super().__init__(width, height, title)

       arcade.set_background_color(arcade.color.BLACK_OLIVE)

       self.player = arcade.Sprite("assets/faceBeard.png", 0.2)
       self.computer = arcade.Sprite("assets/compy.png", 1)
       self.players = arcade.SpriteList()
       self.rock = AttackAnimation(AttackType.ROCK)
       self.paper = AttackAnimation(AttackType.PAPER)
       self.scissors = AttackAnimation(AttackType.SCISSORS)
       self.playerScore = 0
       self.computerScore = 0
       self.animate = False
       self.playerChose = False
       self.computerAttackChosen = None
       self.playerAttackChosen = None
       self.playerWonRound = None
       self.drawRound = None
       self.gameState = GameState.NOT_STARTED

   def setup(self):
       """
       Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
       fois si vous recommencer une nouvelle partie.
       """
       # C'est ici que vous allez créer vos listes de sprites et vos sprites.
       # Prenez note que vous devriez attribuer une valeur à tous les attributs créés dans __init__

       self.player.center_x = self.PLAYER_IMAGE_X
       self.player.center_y = self.PLAYER_IMAGE_Y

       self.computer.center_x = self.COMPUTER_IMAGE_X
       self.computer.center_y = self.COMPUTER_IMAGE_Y

       self.players.append(self.player)
       self.players.append(self.computer)


   def validate_victory(self):
       """
       Utilisé pour déterminer qui obtient la victoire (ou s'il y a égalité)
       Rappel: après avoir validé la victoire, il faut changer l'état de jeu
       """

       # Regarder qui gagne. C'est tres laid, et il y a probablement une maniere plus simple de le faire mais bon.
       if self.playerAttackChosen == AttackType.ROCK:
           if self.computerAttackChosen == AttackType.ROCK:
               self.drawRound = True
            
           elif self.computerAttackChosen == AttackType.PAPER:
              self.playerWonRound = False
           
           else:
               self.playerWonRound = True

       elif self.playerAttackChosen == AttackType.PAPER:
           if self.computerAttackChosen == AttackType.PAPER:
               self.drawRound = True
            
           elif self.computerAttackChosen == AttackType.SCISSORS:
              self.playerWonRound = False
           
           else:
               self.playerWonRound = True

       else:
           if self.computerAttackChosen == AttackType.SCISSORS:
               self.drawRound = True
            
           elif self.computerAttackChosen == AttackType.ROCK:
              self.playerWonRound = False
           
           else:
               self.playerWonRound = True
       
       # Changer les scores.
       if not self.drawRound and self.playerWonRound:
           self.playerScore += 1

       elif not self.drawRound and not self.playerWonRound:
           self.computerScore += 1
        
       # Regarder si le score excede trois. Si oui, la partie est finie.
       if max(self.playerScore, self.computerScore) >= 3:
           self.gameState = GameState.GAME_OVER
       
       # Sinon, la ronde est finie.
       else:
           self.gameState = GameState.ROUND_DONE
    
   def draw_possible_attack(self):

       drawAll = self.gameState != GameState.ROUND_DONE and self.gameState != GameState.GAME_OVER

       arcade.draw_rectangle_outline(self.PLAYER_IMAGE_X - self.ATTACK_FRAME_WIDTH - 20, SCREEN_HEIGHT - 450, self.ATTACK_FRAME_WIDTH, self.ATTACK_FRAME_HEIGHT, arcade.color.AMARANTH_PURPLE)
       arcade.draw_rectangle_outline(self.PLAYER_IMAGE_X, SCREEN_HEIGHT - 450, self.ATTACK_FRAME_WIDTH, self.ATTACK_FRAME_HEIGHT, arcade.color.AMARANTH_PURPLE)
       arcade.draw_rectangle_outline(self.PLAYER_IMAGE_X + self.ATTACK_FRAME_WIDTH + 20, SCREEN_HEIGHT - 450, self.ATTACK_FRAME_WIDTH, self.ATTACK_FRAME_HEIGHT, arcade.color.AMARANTH_PURPLE)

       if drawAll or self.playerAttackChosen == AttackType.ROCK:
            self.rock.center_x = self.PLAYER_IMAGE_X - self.ATTACK_FRAME_WIDTH - 20
            self.rock.center_y = SCREEN_HEIGHT - 450
            self.rock.draw()

       if drawAll or self.playerAttackChosen == AttackType.PAPER:
            self.paper.center_x = self.PLAYER_IMAGE_X
            self.paper.center_y = SCREEN_HEIGHT - 450
            self.paper.draw()

       if drawAll or self.playerAttackChosen == AttackType.SCISSORS:
            self.scissors.center_x = self.PLAYER_IMAGE_X + self.ATTACK_FRAME_WIDTH + 20
            self.scissors.center_y = SCREEN_HEIGHT - 450
            self.scissors.draw()

   def draw_computer_attack(self):

       arcade.draw_rectangle_outline(self.COMPUTER_IMAGE_X, SCREEN_HEIGHT - 450, self.ATTACK_FRAME_WIDTH, self.ATTACK_FRAME_HEIGHT, arcade.color.AMARANTH_PURPLE)

       if self.gameState != GameState.ROUND_DONE and self.gameState != GameState.GAME_OVER:
           return

       if self.computerAttackChosen == AttackType.ROCK:
            self.rock.center_x = self.COMPUTER_IMAGE_X
            self.rock.center_y = SCREEN_HEIGHT - 450
            self.rock.draw()

       elif self.computerAttackChosen == AttackType.PAPER:
            self.paper.center_x = self.COMPUTER_IMAGE_X
            self.paper.center_y = SCREEN_HEIGHT - 450
            self.paper.draw()

       else:
            self.scissors.center_x = self.COMPUTER_IMAGE_X
            self.scissors.center_y = SCREEN_HEIGHT - 450
            self.scissors.draw()


   def draw_scores(self):
       """
       Montrer les scores du joueur et de l'ordinateur
       """

       drawPosition = self.PLAYER_IMAGE_X - SCREEN_WIDTH / 2
       arcade.draw_text("Le pointage du joueur est " + str(self.playerScore),
                        drawPosition,
                        SCREEN_HEIGHT - 550,
                        arcade.color.AERO_BLUE,
                        20,
                        width=SCREEN_WIDTH,
                        align="center")

       drawPosition = self.COMPUTER_IMAGE_X - SCREEN_WIDTH / 2
       arcade.draw_text("Le pointage de l'ordinateur est " + str(self.computerScore),
                        drawPosition,
                        SCREEN_HEIGHT - 550,
                        arcade.color.AERO_BLUE,
                        20,
                        width=SCREEN_WIDTH,
                        align="center")

   def draw_instructions(self):
       message = ""

       if self.gameState == GameState.NOT_STARTED:
           message = "Appuyez sur ESPACE pour commencer."

       elif self.gameState == GameState.ROUND_ACTIVE:
           message = "Appuyez sur une image pour faire une attaque."

       elif self.gameState == GameState.ROUND_DONE:
           if self.drawRound:
               message = "Appuyez sur ESPACE pour passer a la prochaine ronde.\nLa ronde est une nulle."
           elif self.playerWonRound:
               message = "Appuyez sur ESPACE pour passer a la prochaine ronde.\nLe joueur remporte la ronde."
           else:
               message = "Appuyez sur ESPACE pour passer a la prochaine ronde.\nL'ordinateur remporte la ronde."

       else:
           if self.playerScore >= 3:
               message = "Appuyez sur ESPACE pour recommencer.\nLe joueur remporte la partie."
           else:
               message = "Appuyez sur ESPACE pour recommencer.\nL'ordinateur remporte la partie."


       arcade.draw_text(message,
                        0,
                        SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 3,
                        arcade.color.AERO_BLUE,
                        30,
                        width=SCREEN_WIDTH,
                        align="center")


   def on_draw(self):
       """
       C'est la méthode que Arcade invoque à chaque "frame" pour afficher les éléments
       de votre jeu à l'écran.
       """

       # Cette commande permet d'effacer l'écran avant de dessiner. Elle va dessiner l'arrière
       # plan selon la couleur spécifié avec la méthode "set_background_color".
       arcade.start_render()

       # Montrer title.
       arcade.draw_text(SCREEN_TITLE,
                        0,
                        SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                        arcade.color.BLACK_BEAN,
                        60,
                        width=SCREEN_WIDTH,
                        align="center")
        
       # Update de l'animation. On peut faire ce que j'ai fait parce qu'ils ont tous les memes temps d'update.
       if self.animate:
           self.rock.on_update()
           self.paper.on_update()
           self.animate = self.scissors.on_update()

       # Le reste.
       self.draw_instructions()
       self.players.draw()
       self.draw_possible_attack()
       self.draw_computer_attack()
       self.draw_scores()

       #afficher l'attaque de l'ordinateur selon l'état de jeu
       #afficher le résultat de la partie si l'ordinateur a joué (ROUND_DONE)

   def on_update(self, delta_time):

       if self.gameState == GameState.ROUND_ACTIVE and self.playerChose:

           # Choisir au hasard un choix pour l'ordi.
           self.computerAttackChosen = random.choice(list(AttackType))

           # Regarder qui gagne la ronde et tout ca.
           self.validate_victory()

    # Quand on appuie sur une cle.
   def on_key_press(self, key, key_modifiers):

       if key == arcade.key.SPACE:
           
           if self.gameState == GameState.ROUND_DONE:
               self.reset_round()
           
           if self.gameState == GameState.GAME_OVER:
               self.reset_round()
               self.playerScore = 0
               self.computerScore = 0

           self.gameState = GameState.ROUND_ACTIVE

   def reset_round(self):

       self.playerAttackChosen = None
       self.computerAttackChosen = None
       self.playerChose = False
       self.playerWonRound = None
       self.drawRound = None

   def on_mouse_press(self, x, y, button, key_modifiers):
       """
       Méthode invoquée lorsque l'usager clique un bouton de la souris.
       Paramètres:
           - x, y: coordonnées où le bouton a été cliqué
           - button: le bouton de la souris appuyé
           - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
       """

       if self.gameState != GameState.ROUND_ACTIVE:
           return

       # Test de collision pour le type d'attaque (self.player_attack_type).
       if self.rock.collides_with_point((x, y)):
           self.playerAttackChosen = AttackType.ROCK
           self.playerChose = True
           self.animate = True
        
       elif self.paper.collides_with_point((x, y)):
           self.playerAttackChosen = AttackType.PAPER
           self.playerChose = True
           self.animate = True
    
       elif self.scissors.collides_with_point((x, y)):
           self.playerAttackChosen = AttackType.SCISSORS
           self.playerChose = True
           self.animate = True
    


def main():
   """ Main method """
   game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
   game.setup()
   arcade.run()


if __name__ == "__main__":
   main()
