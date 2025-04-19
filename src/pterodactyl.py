import pygame
import random

class Pterodactyl:
    def __init__(self, x, y_levels, sprite_sheet_path, sprite_coords, speed):
        """
        Initialize the Pterodactyl.
        :param x: Initial x position of the Pterodactyl.
        :param y_levels: List of exact y positions for the Pterodactyl.
        :param sprite_sheet_path: Path to the sprite sheet containing the Pterodactyl sprites.
        :param sprite_coords: List of tuples for the Pterodactyl's animation frames (x, y, width, height).
        :param speed: Speed at which the Pterodactyl moves.
        """
        self.x = x
        self.y = random.choice(y_levels)  # Choose one of the exact y levels
        self.speed = speed

        # Load the sprite sheet and extract the animation frames
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.sprites = [self.get_sprite(*coords) for coords in sprite_coords]
        self.current_sprite_index = 0

        # Animation timer
        self.animation_counter = 0
        self.animation_speed = 40  # Adjust this value for faster/slower wing flapping

    def get_sprite(self, x, y, width, height):
        """Extract a sprite from the sprite sheet."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return sprite

    @property
    def sprite(self):
        """Return the current sprite for collision detection."""
        return self.sprites[self.current_sprite_index]

    def update(self, game_speed):
        """Move the Pterodactyl to the left at the same speed as the obstacles and animate its wings."""
        self.x -= game_speed  # Use the game speed instead of its own speed

        # Animate the wings
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)

    def draw(self, screen):
        """Draw the Pterodactyl on the screen."""
        screen.blit(self.sprite, (self.x, self.y))

    def is_off_screen(self):
        """Check if the Pterodactyl has moved off the screen."""
        return self.x + self.sprites[0].get_width() < 0