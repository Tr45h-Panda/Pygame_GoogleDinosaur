import pygame

class Ground:
    def __init__(self, y, sprite_sheet_path, sprite_coords, screen_width):
        self.y = y  # Ground level (visible top of the ground)
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.sprite = self.get_sprite(*sprite_coords)
        self.x1 = 0
        self.x2 = screen_width
        self.screen_width = screen_width
        self.speed = 7  # Speed of the ground scrolling

        # Offset to account for extra textures above the ground level
        self.texture_offset = 12  # Difference between y=104 and y=112

    def get_sprite(self, x, y, width, height):
        """Extract the ground sprite from the sprite sheet."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return sprite

    def update(self):
        """Update the position of the ground to create a scrolling effect."""
        self.x1 -= self.speed
        self.x2 -= self.speed

        # Reset positions when the ground scrolls off-screen
        if self.x1 + self.sprite.get_width() <= 0:
            self.x1 = self.x2 + self.sprite.get_width()
        if self.x2 + self.sprite.get_width() <= 0:
            self.x2 = self.x1 + self.sprite.get_width()

    def draw(self, screen):
        """Draw the ground on the screen."""
        # Draw the ground with the texture offset
        screen.blit(self.sprite, (self.x1, self.y - self.texture_offset))
        screen.blit(self.sprite, (self.x2, self.y - self.texture_offset))

