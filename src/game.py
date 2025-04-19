import pygame
from ground import Ground
from obstacle import Obstacle
from score import Score
from cloud import Cloud
import random
from pterodactyl import Pterodactyl
from leaderboard import Leaderboard

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = None
        self.dinosaur = None
        self.ground = None
        self.obstacles = []
        self.clouds = []  # List to store clouds
        self.cloud_spawn_cooldown = 0  # Cooldown for spawning clouds
        self.game_over = False
        self.reset_button_sprite = None
        self.game_speed = 7  # Initial game speed
        self.leaderboard = Leaderboard()  # Add a leaderboard instance
        self.starting_animation_played = False  # Track if the starting animation has been played

    def start(self):
        """Initialize the game and show the starting animation."""
        self.running = True
        self.game_over = False
        self.game_speed = 7  # Reset game speed
        self.score = Score("assets/sprite.png", {
            0: (954, 2, 18, 21),
            1: (976, 2, 18, 21),
            2: (994, 2, 18, 21),
            3: (1014, 2, 18, 21),
            4: (1034, 2, 18, 21),
            5: (1054, 2, 18, 21),
            6: (1074, 2, 18, 21),
            7: (1094, 2, 18, 21),
            8: (1114, 2, 18, 21),
            9: (1134, 2, 18, 21),
        })
        from dinosaur import Dinosaur
        self.dinosaur = Dinosaur(50, 300, 44, 47, "assets/sprite.png")
        self.ground = Ground(374, "assets/sprite.png", (0, 100, 1200, 29), 800)
        self.obstacles = []
        self.clouds = []  # Reset clouds
        self.cloud_spawn_cooldown = 0  # Reset cloud cooldown
        self.obstacle_cooldown = 0
        self.score_update_counter = 0

        # Load the reset button sprite
        self.reset_button_sprite = pygame.image.load("assets/sprite.png").subsurface((2, 2, 72, 64))
        self.game_over_sprite = pygame.image.load("assets/sprite.png").subsurface((954, 29, 380, 21))

        # Show the starting animation only if it hasn't been played yet
        if not self.starting_animation_played:
            self.show_starting_animation()
            self.starting_animation_played = True

    def show_starting_animation(self):
        """Show the starting animation with the dino standing on the ground."""
        clock = pygame.time.Clock()
        waiting = True

        while waiting:
            self.screen.fill(WHITE)

            # Draw the ground and the dino standing still
            if self.ground:
                self.ground.draw(self.screen)
            if self.dinosaur:
                self.dinosaur.draw(self.screen)

            # Display "Press UP or SPACE to Start" text
            font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)
            start_text = font.render("Press UP or SPACE to Start", True, BLACK)
            start_text_rect = start_text.get_rect(center=(self.screen.get_width() // 2, 200))
            self.screen.blit(start_text, start_text_rect)

            pygame.display.flip()

            # Wait for the player to press the jump key
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.dinosaur.jump()  # Make the dino jump
                        waiting = False  # Exit the waiting loop

            clock.tick(60)  # Limit the frame rate

        # Wait for the dino to land before starting the game
        while self.dinosaur.is_jumping:
            self.dinosaur.update()
            self.render()
            pygame.display.flip()
            clock.tick(60)

        # Ensure the dino is fully landed before starting the game
        self.dinosaur.is_jumping = False

    def spawn_obstacle(self):
        """Spawn a new obstacle or Pterodactyl at a dynamic interval."""
        if self.obstacle_cooldown == 0 and random.randint(1, 100) > 90:  # Adjust spawn probability
            if random.randint(1, 3) == 1:  # 1 in 3 chance to spawn a Pterodactyl
                # Define the Pterodactyl's animation frames and exact y levels
                pterodactyl_coords = [(260, 2, 92, 79), (352, 2, 92, 79)]  # Example sprite coordinates
                pterodactyl_y_levels = [320, 250, 200]  # Exact heights for the Pterodactyl
                pterodactyl = Pterodactyl(
                    x=self.screen.get_width(),
                    y_levels=pterodactyl_y_levels,
                    sprite_sheet_path="assets/sprite.png",
                    sprite_coords=pterodactyl_coords,
                    speed=self.game_speed  # Match the game speed
                )
                self.obstacles.append(pterodactyl)
            else:
                # Spawn a regular obstacle
                obstacle = Obstacle.spawn_obstacle(self.screen.get_height())
                if obstacle:
                    self.obstacles.append(obstacle)

            # Set cooldown for the next obstacle spawn
            self.obstacle_cooldown = max(40, int(100 / self.game_speed))  # Adjust cooldown based on game speed
        if self.obstacle_cooldown > 0:
            self.obstacle_cooldown -= 1

    def spawn_cloud(self):
        """Spawn a new cloud at a random height and distance."""
        if self.cloud_spawn_cooldown == 0:
            # Define the sprite coordinates for the cloud (x, y, width, height)
            cloud_coords = (166, 2, 92, 27)  # Example coordinates for a cloud sprite

            # Randomize the x and y positions
            cloud_x = self.screen.get_width() + random.randint(50, 200)  # Random offset for x
            cloud_y = random.randint(30, 220)  # Random height for the cloud

            # Create and add the cloud
            cloud = Cloud(cloud_x, cloud_y, "assets/sprite.png", cloud_coords, speed=random.uniform(0.5, 1.5))
            self.clouds.append(cloud)

            # Set a random cooldown for the next cloud spawn
            self.cloud_spawn_cooldown = random.randint(150, 500)  # Random cooldown
        else:
            self.cloud_spawn_cooldown -= 1

    def update_clouds(self):
        """Update the position of clouds and remove off-screen clouds."""
        for cloud in self.clouds[:]:
            cloud.update()
            if cloud.is_off_screen():
                self.clouds.remove(cloud)

    def check_collisions(self):
        """Check for collisions between the dinosaur and obstacles using masks."""
        # Create a mask for the dinosaur
        dino_mask = pygame.mask.from_surface(self.dinosaur.current_sprite)

        for obstacle in self.obstacles:
            # Create a mask for the obstacle
            obstacle_mask = pygame.mask.from_surface(obstacle.sprite)

            # Calculate the offset between the dinosaur and the obstacle
            offset = (obstacle.x - self.dinosaur.x, obstacle.y - self.dinosaur.y)

            # Check for overlap between the masks
            if dino_mask.overlap(obstacle_mask, offset):
                self.running = False  # Stop the game loop
                self.game_over = True  # Set game over state
                self.dinosaur.set_dead()  # Switch to the dead sprite
                break

    def update(self):
        # Update the dinosaur
        if self.dinosaur:
            self.dinosaur.update()

        # Update the ground
        if self.ground:
            self.ground.speed = self.game_speed  # Adjust ground speed
            self.ground.update()

        # Increment the score at a rate tied to the game speed
        self.score_update_counter += self.game_speed / 40  # Faster increment as speed increases
        if self.score_update_counter >= 1:
            self.score.increment()
            self.score_update_counter = 0

        # Update obstacles
        self.spawn_obstacle()
        for obstacle in self.obstacles[:]:
            # Pass the game speed to both obstacles and Pterodactyls
            obstacle.update(self.game_speed)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)

        # Gradually increase the game speed
        self.game_speed += 0.001  # Adjust this value to control how quickly the speed increases

        # Update clouds
        self.spawn_cloud()
        self.update_clouds()

        # Check for collisions
        self.check_collisions()

    def render(self):
        self.screen.fill(WHITE)

        # Draw clouds
        for cloud in self.clouds:
            cloud.draw(self.screen)

        # Draw the ground, dinosaur, obstacles, and score
        if self.ground:
            self.ground.draw(self.screen)
        if self.dinosaur:
            self.dinosaur.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

            # Debug: Draw the mask for the obstacle
            obstacle_mask = pygame.mask.from_surface(obstacle.sprite)
            #obstacle_surface = obstacle_mask.to_surface(setcolor=(255, 0, 0, 100), unsetcolor=(0, 0, 0, 0))
            #self.screen.blit(obstacle_surface, (obstacle.x, obstacle.y))

        if self.dinosaur:
            # Debug: Draw the mask for the dinosaur
            dino_mask = pygame.mask.from_surface(self.dinosaur.current_sprite)
            #dino_surface = dino_mask.to_surface(setcolor=(0, 255, 0, 100), unsetcolor=(0, 0, 0, 0))
            #self.screen.blit(dino_surface, (self.dinosaur.x, self.dinosaur.y))

        if self.score:
            self.score.draw(self.screen, 700, 20)

        # Draw the reset button and game over sprite if the game is over
        if self.game_over:
            game_over_x = (self.screen.get_width() - self.game_over_sprite.get_width()) // 2
            game_over_y = 150
            reset_button_x = (self.screen.get_width() - self.reset_button_sprite.get_width()) // 2
            reset_button_y = game_over_y + self.game_over_sprite.get_height() + 20
            self.screen.blit(self.game_over_sprite, (game_over_x, game_over_y))
            self.screen.blit(self.reset_button_sprite, (reset_button_x, reset_button_y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    if not self.game_over and self.dinosaur:
                        self.dinosaur.jump()
                    elif self.game_over:
                        # Only reset the game after the leaderboard has been handled
                        if not self.running:  # Ensure the game is not running
                            self.reset()
                elif event.key == pygame.K_DOWN:
                    if not self.game_over and self.dinosaur:
                        self.dinosaur.duck()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    if self.dinosaur:
                        self.dinosaur.release_jump()
                elif event.key == pygame.K_DOWN:
                    if self.dinosaur:
                        self.dinosaur.stop_ducking()

        # Continuous key state checking
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if not self.game_over and self.dinosaur and not self.dinosaur.is_jumping:
                self.dinosaur.duck()

    def reset(self):
        """Reset the game state for a new game."""
        self.start()  # Call the start method to reset the game state

    def handle_leaderboard(self):
        """Handle leaderboard logic after the game ends."""
        font = pygame.font.Font(None, 36)  # Default font for rendering text

        # Check if the score qualifies for the leaderboard
        if self.leaderboard.qualifies_for_leaderboard(self.score.current_score):  # Access the score correctly
            initials = self.get_player_initials("assets/PressStart2P-Regular.ttf")  # Get the player's initials
            self.leaderboard.add_score(initials, self.score.current_score)  # Add the score to the leaderboard

        # Display the leaderboard
        self.display_leaderboard("assets/PressStart2P-Regular.ttf")

    def get_player_initials(self, font_path="assets/PressStart2P-Regular.ttf"):
        """
        Prompt the player to enter their initials with an arcade-style font.
        :param font_path: Path to the arcade-style font file.
        :return: The player's initials as a string.
        """
        initials = ""
        blink = True
        clock = pygame.time.Clock()
        input_active = True

        # Load the arcade-style font
        font = pygame.font.Font(font_path, 36)  # Adjust size as needed

        while input_active:
            self.screen.fill((0, 0, 0))  # Black background for arcade feel

            # Display the first line: "Highscore!"
            highscore_text = font.render("Highscore!", True, (255, 255, 255))
            highscore_rect = highscore_text.get_rect(center=(self.screen.get_width() // 2, 120))
            self.screen.blit(highscore_text, highscore_rect)

            # Display the second line: "Enter Initials:"
            enter_initials_text = font.render("Enter Initials:", True, (255, 255, 255))
            enter_initials_rect = enter_initials_text.get_rect(center=(self.screen.get_width() // 2, 180))
            self.screen.blit(enter_initials_text, enter_initials_rect)

            # Display the initials with blinking for the next available underscore
            padded_initials = initials.ljust(3, "_")  # Pad with underscores to ensure 3 characters
            display_initials = ""
            for i, char in enumerate(padded_initials):
                if i == len(initials) and blink and char == "_":  # Blink only the next available underscore
                    display_initials += " "  # Show a blank space for blinking
                else:
                    display_initials += char

            initials_text = font.render(display_initials, True, (255, 255, 255))
            initials_rect = initials_text.get_rect(center=(self.screen.get_width() // 2, 250))
            self.screen.blit(initials_text, initials_rect)

            pygame.display.flip()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(initials) == 3:
                        input_active = False  # Finish input when Enter is pressed
                    elif event.key == pygame.K_BACKSPACE and len(initials) > 0:
                        initials = initials[:-1]  # Remove the last character
                    elif len(initials) < 3 and event.unicode.isalpha():
                        initials += event.unicode.upper()  # Add the typed character (uppercase)

            # Blink the underscore
            blink = not blink if clock.tick(2) else blink  # Toggle blink every 500ms

        return initials

    def display_leaderboard(self, font_path="assets/PressStart2P-Regular.ttf"):
        """
        Display the leaderboard on the screen using an arcade-style font.
        :param font_path: Path to the arcade-style font file.
        """
        font = pygame.font.Font(font_path, 36)  # Load the arcade-style font
        self.screen.fill((0, 0, 0))  # Black background for arcade feel

        # Display the title: "LEADERBOARD"
        title_text = font.render("LEADERBOARD", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Render the leaderboard entries
        for i, (initials, score) in enumerate(self.leaderboard.scores, start=1):
            entry_text = font.render(f"{i}. {initials} - {score}", True, (255, 255, 255))
            entry_rect = entry_text.get_rect(center=(self.screen.get_width() // 2, 100 + i * 40))
            self.screen.blit(entry_text, entry_rect)

        pygame.display.flip()

        # Wait for the player to press a key to continue
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False  # Exit the leaderboard screen

    def run(self):
        self.start()  # Initialize the game
        while self.running:  # Run the game loop while the game is running
            self.handle_events()  # Handle user input
            if not self.game_over:
                self.update()  # Update game state only if not game over
            self.render()  # Render the game
            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Cap the frame rate at 60 FPS

            if self.game_over:
                self.running = False  # Stop the game loop when the game is over

        # Add a 2-second pause before transitioning to the leaderboard
        pygame.time.wait(2000)

        # Handle leaderboard logic after the game ends
        self.handle_leaderboard()

        # Reset the game after the leaderboard
        self.reset()