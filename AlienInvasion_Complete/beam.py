import pygame


class Beam(pygame.sprite.Sprite):
    """Manages beams fired from aliens"""
    def __init__(self, ai_settings, screen, alien):
        """super().__init__()
        self.screen = screen

        # Initialize beam image and related variables
        self.image = pygame.image.load('images/alien_beam_resized.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        # Y position and speed factor
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.beam_speed_factor"""

        """Create a bullet object at the given alien's current position."""
        super().__init__()
        self.screen = screen
        # Create bullet at (0, 0) then set to correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom


        # Store bullet's position as a decimal value
        self.y = float(self.rect.y)
        self.color = ai_settings.beam_color
        self.speed_factor = ai_settings.beam_speed_factor

    def update(self):
        """Move the beam down the screen"""
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
