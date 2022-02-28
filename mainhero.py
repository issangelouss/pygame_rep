import pygame
import sprites


class MainHeroStanding(pygame.sprite.Sprite):
    # класс с неподвижным гг
    def __init__(self, x, y, hp):
        super().__init__(sprites.all_sprites)
        self.image = pygame.image.load('data/main_hero/mainhero_stand.png')
        self.rect = self.image.get_rect()
        self.hp = hp
        self.rect = self.rect.move(x, y)

    def die(self):
        self.kill()
        if self.hp != 0:
            return self.rect.x, self.rect.y, self.hp


class MainHeroWalking(sprites.AnimatedSprite):
    # класс с идущим гг
    def __init__(self, x, y, hp):
        super().__init__(pygame.image.load('data/main_hero/sprite_sheet_mov.png'), 3, 1)
        self.rect = self.image.get_rect()
        self.hp = hp
        self.rect = self.rect.move(x, y)

    def moving_right(self):
        self.rect.x += 10
        if self.rect.x > 525:
            self.rect.x = 525

    def moving_left(self):
        self.rect.x -= 10
        if self.rect.x < 0:
            self.rect.x = 0

    def moving_up(self):
        self.rect.y -= 10
        if self.rect.y < 90:
            self.rect.y = 90

    def moving_down(self):
        self.rect.y += 10
        if self.rect.y > 270:
            self.rect.y = 270

    def update(self):
        super().update()

    def die(self):
        self.kill()
        return MainHeroStanding(self.rect.x, self.rect.y, self.hp)


class MainHeroBeating(sprites.AnimatedSprite):
    # класс с атакующим гг
    def __init__(self, x, y, hp):
        super().__init__(pygame.image.load('data/main_hero/sprite_sheet_kick.png'), 3, 1)
        self.rect = self.image.get_rect()
        self.hp = hp
        self.rect = self.rect.move(x, y)

    def die(self):
        self.kill()
        return MainHeroStanding(self.rect.x, self.rect.y, self.hp)


class MainHeroBlock(pygame.sprite.Sprite):
    # класс с блоком гг
    def __init__(self, x, y, hp):
        super().__init__(sprites.all_sprites)
        self.image = pygame.image.load('data/main_hero/mainhero_block.png')
        self.rect = self.image.get_rect()
        self.hp = hp
        self.rect = self.rect.move(x, y)

    def die(self):
        self.kill()
        return MainHeroStanding(self.rect.x, self.rect.y, self.hp)
