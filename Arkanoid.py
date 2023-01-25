import pygame
import random
import os
import sys


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_sound(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        sys.exit()
    return fullname


def load_level(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    file = open(fullname, 'r')
    lvlmap = file.readlines()
    return list(map(lambda x: x.rstrip('\n'), lvlmap))


def generate_level(lvlmap):
    global state_count
    lvlmap = lvlmap
    x = 15
    y = 15
    for string in lvlmap:
        for el in string:
            if el == 'B':
                state_count += 1
                Breakable_box(x, y)
            elif el == 'U':
                Unbreakable_box(x, y)
            elif el == 'N':
                pass
            x += 20
        x = 15
        y += 20


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(main)
        self.image = pygame.Surface((100, 15))
        self.image.fill((253, 106, 2))
        self.rect = self.image.get_rect()
        self.speed = 15
        self.rect.x = 300
        self.rect.y = 600

    def move_left(self):
        if self.rect.x >= 0:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.x <= 600:
            self.rect.x += self.speed


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(balls)
        self.radius = radius
        self.effect = pygame.mixer.Sound(load_sound('ballsound.mp3'))
        self.x = x
        self.y = y
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.choice([-5, 5])
        self.vy = -5

    def update(self):
        global counter
        self.rect = self.rect.move(self.vx, self.vy)
        self.x += self.vx
        self.y += self.vy
        if self.y > 650:
            balls.remove(self)
            all_sprites.remove(self)
        if pygame.sprite.spritecollideany(self, horizontal_borders) and pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
            self.vy = - self.vy
        elif pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        elif pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        elif pygame.sprite.spritecollideany(self, main) and self.y <= 600:
            self.effect.play()
            self.vy = -self.vy
        elif pygame.sprite.spritecollideany(self, breakable_boxes):
            counter += 1
            self.vy = -self.vy

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def speed(self):
        if self.vx < 0:
            self.vx -= 1
        else:
            self.vx += 1
        if self.vy < 0:
            self.vy -= 1
        else:
            self.vy += 1

    def unspeed(self):
        if self.vx < 0 and self.vx < -3:
            self.vx += 1
        elif self.vx > 0 and self.vx > 3:
            self.vx -= 1
        if self.vy < 0 and self.vy < -3:
            self.vy += 1
        elif self.vy > 0 and self.vy > 3:
            self.vy -= 1


class Easterball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.x = x
        self.y = y
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.choice([-3, 3])
        self.vy = -3

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        self.x += self.vx
        self.y += self.vy
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Breakable_box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(breakable_boxes)
        self.image = pygame.Surface((15, 15))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.sprite.spritecollideany(self, balls):
            self.remove(all_sprites)
            self.remove(breakable_boxes)
            choice = random.randint(1, 20)
            if choice == 3 and len(bonuses.sprites()) < 5:
                bonus = random.choice([1, 2, 3, 4])
                if bonus == 2:
                    Two_balls_bonus(self.rect.x, self.rect.y)
                elif bonus == 3:
                    Three_balls_bonus(self.rect.x, self.rect.y)
                elif bonus == 1:
                    Speed_bonus(self.rect.x, self.rect.y)
                elif bonus == 4:
                    Unspeed_bonus(self.rect.x, self.rect.y)


class Unbreakable_box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(unbreakable_boxes)
        self.image = pygame.Surface((15, 15))
        self.image.fill((80, 80, 80))
        self.rect = self.image.get_rect()
        self.count = 0
        self.rect.x = x
        self.rect.y = y
        Border(x, y, x + 15, y)
        Border(x, y + 15, x + 15, y + 15)
        Border(x, y, x, y + 15)
        Border(x + 15, y, x + 15, y + 15)


class Two_balls_bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(bonuses)
        self.image = load_image('twoball.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 4
        if self.rect.y > 650:
            self.remove(all_sprites)
            self.remove(bonuses)
        if pygame.sprite.spritecollideany(self, main):
            if len(balls.sprites()) < 60:
                x = 350
                for _ in range(2):
                    Ball(6, x, 580)
                    x += 15
            all_sprites.remove(self)
            bonuses.remove(self)


class Three_balls_bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(bonuses)
        self.image = load_image('threeball.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 4
        if self.rect.y > 650:
            self.remove(all_sprites)
            self.remove(bonuses)
        if pygame.sprite.spritecollideany(self, main):
            if len(balls.sprites()) < 60:
                x = 350
                for _ in range(3):
                    Ball(6, x, 580)
                    x += 15
            all_sprites.remove(self)
            bonuses.remove(self)


class Speed_bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(bonuses)
        self.image = load_image('speed.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 4
        if self.rect.y > 650:
            self.remove(all_sprites)
            self.remove(bonuses)
        if pygame.sprite.spritecollideany(self, main):
            for el in balls:
                el.speed()
            all_sprites.remove(self)
            bonuses.remove(self)


class Unspeed_bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(bonuses)
        self.image = load_image('unspeed.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 4
        if self.rect.y > 650:
            self.remove(all_sprites)
            self.remove(bonuses)
        if pygame.sprite.spritecollideany(self, main):
            for el in balls:
                el.unspeed()
            all_sprites.remove(self)
            bonuses.remove(self)


def restart():
    global balls
    global all_sprites
    for el in balls:
        if el.get_y() > 500:
            return
    for el in balls:
        all_sprites.remove(el)
    balls = pygame.sprite.Group()
    Ball(6, 350, 580)


def base():
    global state_count
    global counter
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            platform.move_left()

        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            platform.move_right()
        all_sprites.draw(screen)
        all_sprites.update()
        if not balls or not breakable_boxes:
            if round(counter/state_count*100, 2) >= 60:
                open_lvl = " level" + str(int(level_name[5]) + 1) + ".txt"
                if open_lvl[6] != "6" and open_lvl not in completed_lvls:
                    with open("data/completed_levels.txt", "a") as cl:
                        cl.write(open_lvl)
            screen.fill((0, 0, 0))
            return
        clock.tick(fps)
        pygame.display.flip()


def start_page():
    global level_name
    fon = pygame.transform.scale(load_image('startfon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    text = font.render('ARKANOID', False, (48, 213, 200))
    screen.blit(text, (180, 30))
    font = pygame.font.Font(None, 45)
    text_2 = font.render('Выберите уровень', False, (255, 255, 255))
    screen.blit(text_2, (190, 120))
    font = pygame.font.Font(None, 30)
    text_3 = font.render("Вы не прошли предыдущий уровень",
                         False, (255, 255, 255))
    frstimg = pygame.transform.scale(load_image('level1img.png'), (100, 100))
    screen.blit(frstimg, (70, 250))
    scndimg = pygame.transform.scale(load_image('level2img.png'), (100, 100))
    screen.blit(scndimg, (290, 250))
    thrdimg = pygame.transform.scale(load_image('level3img.png'), (100, 100))
    screen.blit(thrdimg, (510, 250))
    frthimg = pygame.transform.scale(load_image('level4img.png'), (100, 100))
    screen.blit(frthimg, (180, 450))
    ffthimg = pygame.transform.scale(load_image('level5img.png'), (100, 100))
    screen.blit(ffthimg, (400, 450))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 70 <= event.pos[0] <= 150 and 250 <= event.pos[1] <= 350:
                    if 'level1.txt' in completed_lvls:
                        level_name = 'level1.txt'
                        return
                    else:
                        screen.blit(text_3, (160, 650))
                        clock.tick(10)
                if 290 <= event.pos[0] <= 370 and 250 <= event.pos[1] <= 350:
                    if 'level2.txt' in completed_lvls:
                        level_name = 'level2.txt'
                        return
                    else:
                        screen.blit(text_3, (160, 650))
                if 510 <= event.pos[0] <= 590 and 250 <= event.pos[1] <= 350:
                    if 'level3.txt' in completed_lvls:
                        level_name = 'level3.txt'
                        return
                    else:
                        screen.blit(text_3, (160, 650))
                        clock.tick(10)
                if 180 <= event.pos[0] <= 280 and 450 <= event.pos[1] <= 550:
                    if 'level4.txt' in completed_lvls:
                        level_name = 'level4.txt'
                        return
                    else:
                        screen.blit(text_3, (160, 650))
                        clock.tick(10)
                if 400 <= event.pos[0] <= 500 and 450 <= event.pos[1] <= 550:
                    if 'level5.txt' in completed_lvls:
                        level_name = 'level5.txt'
                        return
                    else:
                        screen.blit(text_3, (160, 650))
                        clock.tick(10)
        pygame.display.flip()
        clock.tick(fps)


def game_over():
    global last_e_e
    fon = pygame.transform.scale(load_image('startfon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    text = font.render('GAME OVER', False, (48, 213, 200))
    screen.blit(text, (180, 30))
    font = pygame.font.Font(None, 35)
    text_2 = font.render(
        'Нажмите любую кнопку или перезапустите программу', False, (255, 255, 255))
    text_3 = font.render(
        f'Вы прошли {round(counter/state_count*100, 2)}% уровня', False, (255, 255, 255))
    font = pygame.font.Font(None, 32)
    text_4 = font.render("Следующий уровень открыт", False, (255, 255, 255))
    text_5 = font.render(
        "Пройдите 60% уровня и более, чтобы открыть следующий", False, (255, 255, 255))
    b1 = Border(3, 3, 697, 3)
    b2 = Border(3, 697, 697, 697)
    b3 = Border(3, 3, 3, 697)
    b4 = Border(697, 3, 697, 697)
    ball = Easterball(6, 350, 580)
    last_e_e.add((b1, b2, b3, b4, ball))
    while True:
        screen.blit(fon, (0, 0))
        screen.blit(text, (180, 30))
        screen.blit(text_2, (25, 650))
        screen.blit(text_3, (200, 150))
        if round(counter/state_count*100, 2) >= 60:
            screen.blit(text_4, (190, 200))
        else:
            screen.blit(text_5, (25, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        last_e_e.draw(screen)
        last_e_e.update()
        clock.tick(fps)
        pygame.display.flip()


def tutorial():
    font = pygame.font.Font(None, 27)
    first_string = [i for i in "A/D KEYLEFT/KEYRIGHT для управления".upper()]
    second_string = [i for i in "R ПРИ ПРОБЛЕМАХ С ШАРОМ"]
    third_string = [i for i in "Пройдите 60% уровня и более, чтобы открыть следующий"]
    screen.fill((0, 0, 0))
    skip = font.render("SPACEBAR для продолжения", False, (255, 255, 255))
    screen.blit(skip, (420, 650))
    x = 90
    y = 250
    for el in first_string:
        letter = font.render(el, False, (255, 255, 255))
        screen.blit(letter, (x, y))
        x += 15
        pygame.display.flip()
        clock.tick(35)
    y = 300
    x = 170
    for el in second_string:
        letter = font.render(el, False, (255, 255, 255))
        screen.blit(letter, (x, y))
        x += 15
        pygame.display.flip()
        clock.tick(35)
    x = 15
    y = 350
    font = pygame.font.Font(None, 26)
    for el in third_string:
        letter = font.render(el, False, (255, 255, 255))
        screen.blit(letter, (x, y))
        x += 13
        pygame.display.flip()
        clock.tick(35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('Arkanoid')
    pygame.mixer.music.load(load_sound('fon_music.mp3'))
    pygame.mixer.music.play(-1)
    while True:
        size = width, height = 700, 700
        screen = pygame.display.set_mode(size)
        all_sprites = pygame.sprite.Group()
        main = pygame.sprite.Group()
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()
        breakable_boxes = pygame.sprite.Group()
        unbreakable_boxes = pygame.sprite.Group()
        bonuses = pygame.sprite.Group()
        balls = pygame.sprite.Group()
        last_e_e = pygame.sprite.Group()
        state_count = 0
        counter = 0
        with open("data/completed_levels.txt") as cl:
            completed_lvls = [i for i in cl.readline().split()]
        Border(5, 5, width - 5, 5)
        Border(5, height - 5, width - 5, height - 5)
        Border(5, 5, 5, height - 5)
        Border(width - 5, 5, width - 5, height - 5)
        fps = 60
        level_name = 'None'
        clock = pygame.time.Clock()
        platform = Platform()
        Ball(6, 350, 580)
        start_page()
        tutorial()
        level_map = load_level(level_name)
        generate_level(level_map)
        base()
        game_over()
