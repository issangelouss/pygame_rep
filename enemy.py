import pygame
import sprites


class EnemyStanding(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, letter):
        super().__init__(sprites.all_sprites)
        self.letter = letter
        self.image = pygame.image.load(f'data/enemies/enemy_{letter}.png')
        self.rect = self.image.get_rect()
        self.hp = hp
        self.rect = self.rect.move(x, y)

    def die(self):
        self.kill()
        if self.hp != 0:
            return self.rect.x, self.rect.y, self.hp, self.letter
        else:
            return EnemyStanding(800, 200, 3, sprites.letters[(sprites.letters.index(self.letter) + 1) % 3])


class EnemyWalking(sprites.AnimatedSprite):
    def __init__(self, x, y, hp, letter):
        super().__init__(pygame.image.load(f'data/enemies/sprite_sheet_mov_e{letter}.png'), 4, 1)
        self.letter = letter
        self.rect = self.image.get_rect()
        self.hp = hp
        self.rect = self.rect.move(x, y)

    def moving(self):
        self.rect.x -= 10

    def update(self):
        super().update()

    def die(self):
        self.kill()
        if self.hp != 0:
            return self.rect.x, self.rect.y, self.hp, self.letter
        else:
            return EnemyStanding(800, 200, 3, sprites.letters[(sprites.letters.index(self.letter) + 1) % 3])


class EnemyBeating(sprites.AnimatedSprite):
    def __init__(self, x, y, hp, letter):
        super().__init__(pygame.image.load(f'data/enemies/sprite_sheet_kick_e{letter}.png'), 3, 1)
        self.letter = letter
        self.rect = self.image.get_rect()
        self.hp = hp
        self.rect = self.rect.move(x, y)

    def die(self):
        self.kill()
        if self.hp != 0:
            return self.rect.x, self.rect.y, self.hp, self.letter
        else:
            return EnemyStanding(800, 200, 3, sprites.letters[(sprites.letters.index(self.letter) + 1) % 3])
