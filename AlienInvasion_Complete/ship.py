import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize ship and set starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load Ship image and set rect attribute
        self.images = None
        self.image = None
        self.image_index = None
        self.death_index = None
        self.last_frame = None
        self.death_frames = None
        self.rect = None

        # sound
        self.ship_death_sound = pygame.mixer.Sound('sound/AlienBoom.wav')
        self.ship_shoot = pygame.mixer.Sound('sound/pewpew.wav')
        self.ship_death_sound.set_volume(0.5)
        self.ship_shoot.set_volume(0.5)
        self.channel = ai_settings.ship_channel

        # Moving status flags
        self.moving_right = False
        self.moving_left = False

        # Load ship image and set rect attributes
        self.ship_images = [
            pygame.image.load('images/SpaceShip/MericaShip00.png'),
            pygame.image.load('images/SpaceShip/MericaShip01.png'),
            pygame.image.load('images/SpaceShip/MericaShip02.png'),
            pygame.image.load('images/SpaceShip/MericaShip03.png'),
            pygame.image.load('images/SpaceShip/MericaShip04.png'),
            pygame.image.load('images/SpaceShip/MericaShip05.png'),
            pygame.image.load('images/SpaceShip/MericaShip06.png'),
            pygame.image.load('images/SpaceShip/MericaShip07.png'),
            pygame.image.load('images/SpaceShip/MericaShip08.png'),
            pygame.image.load('images/SpaceShip/MericaShip09.png'),
            pygame.image.load('images/SpaceShip/MericaShip10.png'),
            pygame.image.load('images/SpaceShip/MericaShip11.png')

        ]

        self.death_images = [
            pygame.image.load('images/Boom/Boom_0.png'),
            pygame.image.load('images/Boom/Boom_1.png'),
            pygame.image.load('images/Boom/Boom_2.png'),
            pygame.image.load('images/Boom/Boom_3.png'),
            pygame.image.load('images/Boom/Boom_4.png'),
            pygame.image.load('images/Boom/Boom_5.png'),
            pygame.image.load('images/Boom/Boom_6.png'),
            pygame.image.load('images/Boom/Boom_7.png'),
            pygame.image.load('images/Boom/Boom_8.png')
        ]

        self.image_index = 0
        self.image = self.ship_images[self.image_index]
        self.screen_rect = screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.last_frame = pygame.time.get_ticks()

        # Store center as decimal
        self.center = float(self.rect.centerx)
        self.dead = False

    def fire_weapon(self):
        """Play the audio for the ship firing its weapon"""
        self.channel.play(self.ship_shoot)

    def update(self):
        """Update ship's position based on moving state"""
        # Move right/left based on moving status flags, unless the ship is at the edge of the screen
        time_test = pygame.time.get_ticks()

        """if not self.dead:
            self.last_frame = time_test
            self.image_index = (self.image_index + 1) % len(self.ship_images)  # Loop over frames
            self.image = self.ship_images[self.image_index]"""

        if not self.dead:
            if abs(self.last_frame - time_test) > 20:
                self.last_frame = time_test
                self.image_index = (self.image_index + 1) % len(self.ship_images)   # Loop over frames
                self.image = self.ship_images[self.image_index]

        if not self.dead:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor

            self.rect.centerx = self.center
        else:
            time_test = pygame.time.get_ticks()
            if abs(time_test - self.last_frame) > 100:
                self.death_index += 1
                if self.death_index < len(self.death_images):
                    self.image = self.death_images[self.death_index]
                    self.last_frame = time_test
                else:
                    self.dead = False
                    self.image = self.ship_images[self.image_index]

    def center_ship(self):
        """Center the ship on the screen"""
        self.centerx = self.screen_rect.centerx

    def death(self):
        """Switch ship to death image briefly and pause"""
        self.dead = True
        self.death_index = 0
        self.image = self.death_images[self.death_index]
        self.last_frame = pygame.time.get_ticks()
        self.channel.play(self.ship_death_sound)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
