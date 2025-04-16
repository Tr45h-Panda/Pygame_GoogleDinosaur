import pygame

class Dinosaur:
    def __init__(self, x, y, width, height, sprite_sheet_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_jumping = False
        self.is_ducking = False  # Track if the dinosaur is ducking
        self.jump_velocity = 0  # Vertical velocity for jumping
        self.jump_key_held = False  # Track if the jump key is being held
        self.max_jump_velocity = -15  # Maximum upward velocity
        self.gravity = 1.2  # Gravity to pull the dinosaur back down
        self.ground_y = y  # Store the ground level (initial y position)

        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

        # Extract the running sprites
        self.running_sprites = [
            self.get_sprite(1514, 0, 86, 96),  # First running frame
            self.get_sprite(1602, 0, 86, 96),  # Second running frame
        ]

        # Extract the jumping sprite
        self.jumping_sprite = self.get_sprite(1338, 0, 86, 96)  # Jumping sprite

        # Extract the ducking sprites
        self.ducking_sprites = [
            self.get_sprite(1866, 36, 118, 60),  # First ducking frame
            self.get_sprite(1984, 36, 118, 60),  # Second ducking frame
        ]

        self.dead_sprite = self.get_sprite(1690, 0, 86, 96)  # Dead sprite
        self.current_sprite = self.running_sprites[0]

        # Animation timer
        self.animation_counter = 0
        self.animation_speed = 5
        self.current_sprite_index = 0

    def get_sprite(self, x, y, width, height):
        """Extract a sprite from the sprite sheet."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return sprite

    def set_dead(self):
        """Switch to the dead sprite."""
        self.current_sprite = self.dead_sprite

    def jump(self):
        """Start the jump."""
        if not self.is_jumping and not self.is_ducking:  # Prevent jumping while ducking
            self.is_jumping = True
            self.jump_velocity = self.max_jump_velocity  # Start with maximum upward velocity
            self.jump_key_held = True  # Start tracking the key hold duration

    def release_jump(self):
        """Stop the jump when the key is released."""
        self.jump_key_held = False

    def duck(self):
        """Start ducking."""
        if not self.is_ducking and not self.is_jumping:  # Prevent repeated adjustments
            self.is_ducking = True
            self.height = 60  # Adjust the height for ducking
            self.y += 36  # Adjust the y position to stay on the ground (96 - 60 = 36)

    def stop_ducking(self):
        """Stop ducking."""
        if self.is_ducking:
            self.is_ducking = False
            self.height = 96  # Reset the height to the original value
            self.y -= 36  # Reset the y position to the original ground level

    def update(self):
        # Handle jumping
        if self.is_jumping:
            if self.jump_key_held and self.jump_velocity < -4:  # Allow higher jumps if key is held
                self.jump_velocity -= 0.6  # Increased for faster upward acceleration while holding
            else:
                self.jump_key_held = False  # Stop modifying velocity if key is released

            # Apply the jump velocity
            self.y += self.jump_velocity

            # Apply gravity
            self.jump_velocity += self.gravity

            # Stop jumping if the dinosaur lands back on the ground
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False  # Reset jumping state immediately
                self.jump_velocity = 0

        # Update the current sprite based on the state
        self.update_sprite()

    def update_sprite(self):
        """Update the current sprite based on the dinosaur's state."""
        if self.is_jumping:
            self.current_sprite = self.jumping_sprite
        elif self.is_ducking:
            # Cycle through ducking sprites
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.current_sprite_index = (self.current_sprite_index + 1) % len(self.ducking_sprites)
            self.current_sprite = self.ducking_sprites[self.current_sprite_index]
        else:
            # Cycle through running sprites
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.current_sprite_index = (self.current_sprite_index + 1) % len(self.running_sprites)
            self.current_sprite = self.running_sprites[self.current_sprite_index]

    def draw(self, screen):
        """Draw the current sprite at the dinosaur's position."""
        screen.blit(self.current_sprite, (self.x, self.y))
