import pygame

class Score:
    def __init__(self, sprite_sheet_path, digit_coords):
        """
        Initialize the Score tracker.
        :param sprite_sheet_path: Path to the sprite sheet containing the digits.
        :param digit_coords: A dictionary mapping digits (0-9) to their sprite coordinates.
        """
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.digit_sprites = self._load_digit_sprites(digit_coords)
        self.current_score = 0

    def _load_digit_sprites(self, digit_coords):
        """
        Load digit sprites from the sprite sheet.
        :param digit_coords: A dictionary mapping digits (0-9) to their sprite coordinates.
        :return: A dictionary of digit surfaces.
        """
        digit_sprites = {}
        for digit, coords in digit_coords.items():
            x, y, width, height = coords
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
            digit_sprites[digit] = sprite
        return digit_sprites

    def increment(self, amount=1):
        """
        Increment the score by a specified amount.
        :param amount: The amount to increment the score by (default is 1).
        """
        self.current_score += amount

    def reset(self):
        """Reset the score to zero."""
        self.current_score = 0

    def get_score(self):
        """
        Get the current score.
        :return: The current score as an integer.
        """
        return self.current_score

    def draw(self, screen, x, y):
        """
        Draw the score on the screen.
        :param screen: The Pygame screen to draw on.
        :param x: The x-coordinate to start drawing the score.
        :param y: The y-coordinate to start drawing the score.
        """
        score_str = str(self.current_score).zfill(5)  # Pad the score to always show 5 digits
        for i, digit in enumerate(score_str):
            digit_sprite = self.digit_sprites[int(digit)]
            screen.blit(digit_sprite, (x + i * digit_sprite.get_width(), y))