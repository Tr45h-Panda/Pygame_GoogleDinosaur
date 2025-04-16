import pygame
import random

class Obstacle:
    def __init__(self, x, y, width, height, sprite_sheet_path, sprite_coords, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

        # Load the sprite sheet and extract the obstacle sprite
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.sprite = self.get_sprite(*sprite_coords)

    def get_sprite(self, x, y, width, height):
        """Extract a sprite from the sprite sheet."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return sprite

    def update(self, game_speed):
        """Move the obstacle to the left based on the game speed."""
        self.x -= game_speed

    def draw(self, screen):
        """Draw the obstacle on the screen."""
        screen.blit(self.sprite, (self.x, self.y))

    def is_off_screen(self):
        """Check if the obstacle has moved off the screen."""
        return self.x + self.width < 0

    @classmethod
    def spawn_obstacle(cls, screen_height):
        """Spawn a new obstacle at the bottom of the screen."""
        # Define obstacle sets with rarity weights
        obstacle_sets = [
            {"sprite_coords": (446, 2, 34, 72), "width": 34, "height": 72, "rarity": 50},  # Common
            {"sprite_coords": (480, 2, 68, 72), "width": 68, "height": 72, "rarity": 30},  # Less common
            {"sprite_coords": (548, 2, 102, 72), "width": 102, "height": 72, "rarity": 10},  # Rare
            {"sprite_coords": (652, 2, 50, 102), "width": 50, "height": 102, "rarity": 20},   # Very rare
            {"sprite_coords": (702, 2, 100, 102), "width": 100, "height": 102, "rarity": 10},   # Ultra rare
            {"sprite_coords": (802, 2, 150, 102), "width": 150, "height": 102, "rarity": 5},   # Legendary
        ]

        # Calculate total rarity weight
        total_rarity = sum(obstacle["rarity"] for obstacle in obstacle_sets)

        # Randomly select an obstacle set based on rarity
        rand = random.randint(1, total_rarity)
        cumulative_rarity = 0
        selected_obstacle = None
        for obstacle in obstacle_sets:
            cumulative_rarity += obstacle["rarity"]
            if rand <= cumulative_rarity:
                selected_obstacle = obstacle
                break

        # Spawn the selected obstacle
        if selected_obstacle:
            return cls(
                x=800,  # Start just off the right edge of the screen
                y=screen_height - selected_obstacle["height"] - 10,  # Align with the bottom of the screen
                width=selected_obstacle["width"],
                height=selected_obstacle["height"],
                sprite_sheet_path="assets/sprite.png",
                sprite_coords=selected_obstacle["sprite_coords"],
                speed=7  # Match ground speed
            )