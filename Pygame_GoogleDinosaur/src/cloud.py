import random
import pygame

class Cloud:
    def __init__(self, x, y, sprite_sheet_path, sprite_coords, speed=1):
        """
        Initialize a cloud.
        :param x: Initial x position of the cloud.
        :param y: Initial y position of the cloud.
        :param sprite_sheet_path: Path to the sprite sheet containing the cloud sprite.
        :param sprite_coords: Coordinates of the cloud sprite in the sprite sheet (x, y, width, height).
        :param speed: Speed at which the cloud drifts (default is 1).
        """
        self.x = x
        self.y = y
        self.speed = speed

        # Load the sprite sheet and extract the cloud sprite
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.sprite = self.get_sprite(*sprite_coords)

    def get_sprite(self, x, y, width, height):
        """Extract a sprite from the sprite sheet."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return sprite

    def update(self):
        """Move the cloud to the left."""
        self.x -= self.speed

    def draw(self, screen):
        """Draw the cloud on the screen."""
        screen.blit(self.sprite, (self.x, self.y))

    def is_off_screen(self):
        """Check if the cloud has moved off the screen."""
        return self.x + self.sprite.get_width() < 0
