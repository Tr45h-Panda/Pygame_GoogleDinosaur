import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 400))  
    pygame.display.set_caption("Dino Game")

    # Create and run the game
    game = Game(screen)
    while True:  # Loop to allow seamless replay
        game.run()  # Run the game
        game.reset()  # Reset the game after it ends

if __name__ == "__main__":
    main()