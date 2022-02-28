from sprites import *
from mainhero import *
from enemy import *

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)

f = open('data/settings.txt', mode='r')
background = f.read(1)
high_score = int(f.read(2))
f.close()
f = open('data/settings.txt', mode='w')
f.close()
select = show_result = running = show = False


class Button:
    # реализация кнопок
    def __init__(self, w, h):
        self.width = w
        self.height = h

    def draw(self, x, y, message, action, font_size=30, num_bckgr=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, '#926eae', (x, y, self.width, self.height))
            if click[0] == 1:
                if action == choose_bckgr:
                    # т.к. доп.аргумент num_bckgr
                    choose_bckgr(num_bckgr)
                else:
                    action()
        else:
            # если курсор на кнопке, она подсвечивается. в обратном случае нет
            pygame.draw.rect(screen, '#876c99', (x, y, self.width, self.height))

        print_text(message, x + 10, y + 10, font_size)


def print_text(message, x, y, font_size=30):
    font_type = pygame.font.Font('data/Current-Regular.otf', font_size)
    text = font_type.render(message, True, (0, 0, 0))
    screen.blit(text, (x, y))


def back_from_select():
    # выход из окна выбора уровня
    global select
    select = False


def back_from_results():
    # выход из окна с результатами
    global show_result
    show_result = False


def play_again():
    # запуск игрового цикла для игры снова
    global show_result
    show_result = False
    game_cycle()


def quit_game():
    # выход из игры
    global show
    show = False


def choose_bckgr(num_bckgr):
    # выбор фона
    global background
    background = num_bckgr


def show_menu():
    # функция для показа главного меню
    global show
    menu_background = pygame.image.load('data/backgrounds/menu_background.png')
    start_btn = Button(150, 50)
    select_lvl_btn = Button(250, 50)
    quit_btn = Button(150, 50)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False

        screen.blit(menu_background, (0, 0))
        pygame.draw.rect(screen, '#876c99', (100, 50, 500, 100))
        print_text("GROM 'EM UP!", 110, 60, font_size=60)
        start_btn.draw(270, 200, 'PLAY', game_cycle)
        select_lvl_btn.draw(220, 270, 'SELECT LEVEL', select_level)
        quit_btn.draw(270, 340, 'QUIT', quit_game)

        pygame.display.flip()


def select_level():
    # функция для показа окна выбора уровня
    global background, select
    select_lvl_background = pygame.image.load('data/backgrounds/menu_background.png')
    back_btn = Button(50, 50)
    backgr_1_btn = Button(250, 40)
    backgr_2_btn = Button(250, 40)
    backgr_3_btn = Button(250, 40)
    backgr_4_btn = Button(250, 40)

    select = True
    while select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                select = False

        screen.blit(select_lvl_background, (0, 0))
        back_btn.draw(5, 5, 'B', back_from_select)
        print(background)
        # выбранный фон обводится в желтый прямоугольник
        if background == '1':
            pygame.draw.rect(screen, '#ffd800', (68, 18, 254, 183))
        elif background == '2':
            pygame.draw.rect(screen, '#ffd800', (378, 18, 254, 183))
        elif background == '3':
            pygame.draw.rect(screen, '#ffd800', (68, 257, 254, 183))
        elif background == '4':
            pygame.draw.rect(screen, '#ffd800', (378, 257, 254, 183))
        screen.blit(pygame.transform.scale(pygame.image.load('data/backgrounds/background_1.png'), (250, 179)), (70, 20))
        backgr_1_btn.draw(70, 201, 'ABANDONED SHOP', choose_bckgr, font_size=20, num_bckgr='1')
        screen.blit(pygame.transform.scale(pygame.image.load('data/backgrounds/background_2.png'), (250, 179)), (380, 20))
        backgr_2_btn.draw(380, 201, 'NIGHT CLUB', choose_bckgr, font_size=20, num_bckgr='2')
        screen.blit(pygame.transform.scale(pygame.image.load('data/backgrounds/background_3.png'), (250, 179)), (70, 259))
        backgr_3_btn.draw(70, 440, 'GRAFFITI WALL', choose_bckgr, font_size=20, num_bckgr='3')
        screen.blit(pygame.transform.scale(pygame.image.load('data/backgrounds/background_4.png'), (250, 179)), (380, 259))
        backgr_4_btn.draw(380, 440, 'CITY STREET', choose_bckgr, font_size=20, num_bckgr='4')

        pygame.display.flip()


def results(score):
    # функция для показа окна с результатами
    global high_score, show_result, running
    menu_btn = Button(300, 50)
    play_again_btn = Button(300, 50)
    running = False

    show_result = True
    while show_result:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_result = False
        pygame.draw.rect(screen, '#876c99', (0, 0, 700, 500))
        if score > high_score:
            # перезапись рекорда
            high_score = score
        print_text(f'YOUR RESULT: {score}', 300, 175)
        print_text(f'HIGHSCORE: {high_score}', 300, 225)
        menu_btn.draw(320, 275, 'BACK TO MENU', back_from_results)
        play_again_btn.draw(320, 325, 'PLAY AGAIN', play_again)

        pygame.display.flip()


def game_cycle():
    # функция для показа окна с игрой
    global background, running
    main_hero = MainHeroStanding(200, 200, 3)
    enemy = EnemyStanding(1000, 200, 3, 'h')
    potion = False
    beat = score = 0
    running = True
    r_flag = l_flag = u_flag = d_flag = False
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if main_hero.__class__.__name__ == 'MainHeroStanding':
                    x, y, hp = main_hero.die()
                    main_hero = MainHeroWalking(x, y, hp)
                if event.key == pygame.K_d:
                    r_flag = True
                elif event.key == pygame.K_a:
                    l_flag = True
                elif event.key == pygame.K_w:
                    u_flag = True
                elif event.key == pygame.K_s:
                    d_flag = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_hero.__class__.__name__ == 'MainHeroStanding':
                    x, y, hp = main_hero.die()
                    if event.button == 1:
                        main_hero = MainHeroBeating(x, y, hp)
                        if enemy.rect.colliderect(main_hero.rect):
                            # удар по врагу
                            if enemy.hp == 1:
                                score += 100
                            enemy.hp -= 1
                            enemy.rect.x += 100
                    if event.button == 3:
                        main_hero = MainHeroBlock(x, y, hp)
            if event.type == pygame.MOUSEBUTTONUP:
                if main_hero.__class__.__name__ != 'MainHeroStanding':
                    main_hero = main_hero.die()
            if event.type == pygame.KEYUP:
                if main_hero.__class__.__name__ in ['MainHeroWalking', 'MainHeroBeating']:
                    main_hero = main_hero.die()
                    if event.key in [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a]:
                        r_flag = l_flag = u_flag = d_flag = False
        # гг идет даже при зажатии клавиши благодаря флагам
        if r_flag:
            main_hero.moving_right()
        elif l_flag:
            main_hero.moving_left()
        elif u_flag:
            main_hero.moving_up()
        elif d_flag:
            main_hero.moving_down()

        if not enemy.rect.colliderect(main_hero.rect):
            # враг не останавливается пока не дойдет до гг
            beat = 0
            if enemy.__class__.__name__ in ['EnemyStanding', 'EnemyBeating']:
                if enemy.hp != 0:
                    x, y, hp, l = enemy.die()
                    enemy = EnemyWalking(x, y, hp, l)
                else:
                    enemy = enemy.die()
            else:
                enemy.moving()
        else:
            # подойдя к врагу, враг бьет только один раз, чтобы выиграть было реально
            if beat == 0:
                if enemy.hp != 0:
                    x, y, hp, l = enemy.die()
                    enemy = EnemyBeating(x, y, hp, l)
                    beat = 1
                else:
                    enemy = enemy.die()
            if enemy.__class__.__name__ == 'EnemyBeating':
                if enemy.cur_frame == 1 and main_hero.__class__.__name__ != 'MainHeroBlock':
                    main_hero.rect.x -= 50
                    if main_hero.__class__.__name__ != 'MainHeroBlock':
                        main_hero.hp -= 1
                if enemy.cur_frame == 2:
                    if enemy.hp != 0:
                        x, y, hp, l = enemy.die()
                        enemy = EnemyStanding(x, y, hp, l)
                    else:
                        enemy = enemy.die()

        if enemy.hp == 0:
            enemy = enemy.die()

        if main_hero.hp == 1 and not potion:
            # когда у гг остается 1 хп, появляется лекарство
            potion = Potion()

        if potion:
            # при столкновении с лекарством гг получает 1 хп
            if potion.rect.colliderect(main_hero.rect):
                potion.kill()
                main_hero.hp += 1
                potion = False

        screen.fill((255, 255, 255))
        if background == '1':
            screen.blit(pygame.image.load('data/backgrounds/background_1.png'), (0, 0))
        elif background == '2':
            screen.blit(pygame.image.load('data/backgrounds/background_2.png'), (0, 0))
        elif background == '3':
            screen.blit(pygame.image.load('data/backgrounds/background_3.png'), (0, 0))
        elif background == '4':
            screen.blit(pygame.image.load('data/backgrounds/background_4.png'), (0, 0))
        for i in range(main_hero.hp):
            screen.blit(pygame.image.load('data/other_sprites/heart.png'), (10 + 40 * i, 10))
        for i in range(enemy.hp):
            screen.blit(pygame.image.load('data/other_sprites/heart.png'), (560 + 40 * i, 10))
        all_sprites.update()
        screen.blit(enemy.image, enemy.rect)
        screen.blit(main_hero.image, main_hero.rect)
        if potion:
            screen.blit(potion.image, potion.rect)
        print(score)
        clock.tick(10)
        pygame.display.flip()
        if main_hero.hp == 0:
            results(score)


show_menu()
#запись новых результатов
f = open('data/settings.txt', 'w')
f.write(background)
f.write('\n')
f.write(str(high_score))
pygame.quit()
