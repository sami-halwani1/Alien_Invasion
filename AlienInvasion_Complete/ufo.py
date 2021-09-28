import pygame
from pygame.sysfont import SysFont
from random import choice


class Ufo(pygame.sprite.Sprite):
    """Represents a UFO meant to move across the screen at random intervals"""
    def __init__(self, ai_settings, screen, sound=True):
        super().__init__()
        # screen, settings, score values
        self.screen = screen
        self.ai_settings = ai_settings
        self.possible_scores = ai_settings.ufo_point_values
        self.ufo_images = None
        self.image = None
        self.image_index = None
        self.death_index = None
        self.last_frame = None
        self.death_frames = None
        self.rect = None
        self.score = None

        self.score_image = None
        self.font = SysFont(None, 32, italic=True)
        self.prep_score()

        # sound
        self.entrance_sound = pygame.mixer.Sound('sound/ufoAppeared.wav')
        self.death_sound = pygame.mixer.Sound('sound/Gottem.wav')
        self.entrance_sound.set_volume(0.6)
        self.channel = ai_settings.ufo_channel



        # death flag
        self.dead = False


        # images, score text
        self.ufo_images = [
            pygame.image.load('images/Fish/Fish_0.png'),
            pygame.image.load('images/Fish/Fish_0.png'),
            pygame.image.load('images/Fish/Fish_1.png'),
            pygame.image.load('images/Fish/Fish_1.png'),
            pygame.image.load('images/Fish/Fish_2.png'),
            pygame.image.load('images/Fish/Fish_2.png'),
            pygame.image.load('images/Fish/Fish_3.png'),
            pygame.image.load('images/Fish/Fish_3.png'),
            pygame.image.load('images/Fish/Fish_4.png'),
            pygame.image.load('images/Fish/Fish_4.png'),
            pygame.image.load('images/Fish/Fish_5.png'),
            pygame.image.load('images/Fish/Fish_6.png'),
            pygame.image.load('images/Fish/Fish_6.png')

        ]
        # death frames
        self.death_frames = [
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
        self.death_frames.append(self.score_image)
        self.image_index = 0
        self.image = self.ufo_images[self.image_index]
        self.rect = self.image.get_rect()
        self.last_frame = pygame.time.get_ticks()

        # initial position, speed/direction
        self.speed = ai_settings.ufo_speed * (choice([-1, 1]))
        self.rect.x = 0 if self.speed > 0 else ai_settings.screen_width
        self.rect.y = ai_settings.screen_height * 0.1

        self.last_frame = 0
        self.wait_interval = 0

        if sound:
            self.channel.play(self.entrance_sound, loops=-1)

    def kill(self):
        self.channel.stop()
        super().kill()

    def begin_death(self):
        self.channel.stop()
        self.channel.play(self.death_sound)
        self.dead = True
        self.death_index = 0
        self.image = self.death_frames[self.death_index]
        self.last_frame = 0

    def get_score(self):
        """Get a random score from the UFO's possible score values"""
        self.score = choice(self.possible_scores)
        return self.score

    def prep_score(self):
        score_str = str(self.get_score())
        self.score_image = self.font.render(score_str, True, (255, 0, 0), self.ai_settings.bg_color)

    def update(self):
        time_test = pygame.time.get_ticks()

        if not self.dead:
            if abs(self.last_frame - time_test) > 50:
                self.last_frame = time_test
                self.image_index = (self.image_index + 1) % len(self.ufo_images)   # Loop over frames
                self.image = self.ufo_images[self.image_index]

        if not self.dead:
            self.rect.x += self.speed
            if self.speed > 0 and self.rect.left > self.ai_settings.screen_width:
                self.kill()
            elif self.rect.right < 0:
                self.kill()

        else:
            if abs(self.last_frame - time_test) > 100:   # At least 100 millisecond delay between frames
                self.last_frame = time_test     # Delay should ensure animation is perceivable at high fps
                self.death_index += 1
                if self.death_index >= len(self.death_frames):
                    self.kill()
                else:
                    self.image = self.death_frames[self.death_index]
                    self.wait_interval += 100

    def blitme(self):
        self.screen.blit(self.image, self.rect)
