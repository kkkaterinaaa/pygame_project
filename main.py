import pygame
import os
import sys
from pygame.sprite import Sprite
from pygame.sprite import Group
from time import sleep
import pygame.font


pygame.init()
size = width, height = 1200, 595
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50
background_position = [0, 0]


class Values():
    def __init__(self):
        self.number_balls = 3
        self.drop_speed = 10
        self.slingshots_left = 2
        self.speedup = 1.1
        self.score_boost = 1.5
        self.speeds()

    def speeds(self):
        self.ball_speed = 10
        self.bird_speed = 2
        self.slingshot_speed = 5
        self.bird_direction = 1
        self.points = 30

    def speeding(self):
        self.ball_speed *= self.speedup
        self.bird_speed *= self.speedup
        self.slingshot_speed *= self.speedup
        self.points = int(self.points * self.score_boost)


class Stats():
    def __init__(self, values):
        self.values = values
        self.reset_stats()
        self.action_active = False
        self.pause = False

    def reset_stats(self):
        self.slingshots_left = self.values.slingshots_left
        self.score = 0
        self.level = 1


class Result():
    def __init__(self, values, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.values = values
        self.stats = stats
        self.text_color = (40, 40, 40)
        self.font = pygame.font.SysFont('serif', 45)
        self.showing()
        self.show_level()
        self.show_lifes()

    def showing(self):
        round_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(round_score)
        self.score_image = (self.font.render(score_str, True, self.text_color,
                            (155, 45, 48)))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.hearts.draw(self.screen)

    def show_level(self):
        self.level_image = (self.font.render(str(self.stats.level), True,
                            self.text_color, (155, 45, 48)))
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_lifes(self):
        self.hearts = Group()
        for number in range(self.stats.slingshots_left + 1):
            heart = Heart(self.values, self.screen)
            heart.rect.x = 10 + number * heart.rect.width
            heart.rect.y = 10
            self.hearts.add(heart)


class Heart(Sprite):
    def __init__(self, values, screen):
        super(Heart, self).__init__()
        self.values = values
        self.screen = screen
        self.image = load_image("heart.png", -1)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()


class Play():
    def __init__(self, values, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 60
        self.button_color = (155, 45, 48)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('serif', 45)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.creation_msg(msg)

    def creation_msg(self, msg):
        self.msg_image = (self.font.render(msg, True, self.text_color,
                          self.button_color))
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()


def start_screen():
    intro_text = ["Проект выполнили: Зайцева Екатерина, Барабанова Анастасия", "",
                  "Правила игры:",
                  "В этой игре Вам необходимо попасть в птиц из рогатки с помощью мячей",
                  "Для выстрела используйте пробел, а для перемещения рогатки клавиши вправо и влево",
                  "При нажатии на клавишу 'P'  игра останавливается, при повторном нажатии возобновляется",
                  "При попадании в птиц Вы получаете баллы, которые выводятся в правом верхнем углу",
                  "Под результатом расположен уровень, который увеличивается при уничтожении всех птиц",
                  "С каждым разом птицы, рогатка и мячи ускоряются, усложняя игру",
                  "В левом верхнем углу находятся жизни",
                  "Их количество сокращается при столкновении птиц с землёй или рогаткой",
                  "Когда последняя жизнь исчезла, игра заканчивается"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    pygame.mixer.music.load('data/fon.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.display.set_caption('Bad birds')
    font = pygame.font.SysFont('serif', 25)
    text_coord = 20

    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 33, 55))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or
                  event.type == pygame.MOUSEBUTTONDOWN):
                return
        pygame.display.flip()
        clock.tick(FPS)


class Slingshot(Sprite):
    def __init__(self, values, screen):
        super(Slingshot, self).__init__()
        self.values = values
        self.screen = screen
        self.image = load_image("slingshot_1.png", -1)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.going_right = False
        self.going_left = False

    def center_slingshot(self):
        self.center = self.screen_rect.centerx

    def update(self):
        if self.going_right and self.rect.right < self.screen_rect.right:
            self.center += self.values.slingshot_speed
        if self.going_left and self.rect.left > 0:
            self.center -= self.values.slingshot_speed
        self.rect.centerx = self.center

    def showing(self):
        self.screen.blit(self.image, self.rect)


class Ball(Sprite):
    def __init__(self, values, screen, slingshot):
        super(Ball, self).__init__()
        self.screen = screen
        self.image = load_image('ball2.png', -1)
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.centerx = slingshot.rect.centerx
        self.rect.top = slingshot.rect.top
        self.y = float(self.rect.y)
        self.speed = values.ball_speed

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def showing(self):
        self.screen.blit(self.image, self.rect)


class Bird(Sprite):
    def __init__(self, values, screen):
        super(Bird, self).__init__()
        self.values = values
        self.screen = screen
        self.frames = []
        self.cut_sheet(load_image("bird.png", -1), 5, 3)
        self.cur_frame = 0
        self.image = load_image('bird1.png', -1)
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)

    def edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += self.values.bird_speed * self.values.bird_direction
        self.rect.x = self.x
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.values.bird_direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def showing(self):
        self.screen.blit(self.image, self.rect)

    def cut_sheet(self, sheet, columns, rows):
        rect = (pygame.Rect(0, 0, sheet.get_width() // columns,
                sheet.get_height() // rows))
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.width * i, rect.height * j)
                self.frames.append((sheet.subsurface(pygame.Rect
                                    (frame_location, rect.size))))
        self.frames.pop(-1)


def create_birds(values, screen, slingshot, birds):
    bird = Bird(values, screen)
    bird_width = bird.rect.width
    bird_height = bird.rect.height
    free_area_x = width - 1.5 * bird_width
    number_birds_x = int(free_area_x / (1.5 * bird_width))
    slingshot_height = slingshot.rect.height
    free_area_y = height - 3 * bird_height - slingshot_height
    number_rows = int(free_area_y / (1.5 * bird_height))

    for row_number in range(number_rows):
        for number in range(number_birds_x):
            bird = Bird(values, screen)
            bird.x = bird_width + 1.5 * bird_width * number
            bird.rect.y = (bird.rect.height + 1.5 * bird.rect.height *
                           row_number)
            bird.rect.x = bird.x
            birds.add(bird)


def new_birds(values, stats, screen, slingshot, birds, balls):
    birds_edges(values, birds)
    birds.update()
    if pygame.sprite.spritecollideany(slingshot, birds):
        slingshot_bump(values, stats, screen, result, slingshot, birds, balls)
    bottom_bump(values, stats, screen, result, slingshot, birds, balls)


def birds_edges(values, birds):
    for bird in birds.sprites():
        if bird.edges():
            change_birds(values, birds)
            break


def change_birds(values, birds):
    for bird in birds.sprites():
        bird.rect.y += values.drop_speed
    values.bird_direction *= -1


start_screen()
values = Values()
stats = Stats(values)
result = Result(values, screen, stats)
button = Play(values, screen, "Let's go!")
slingshot = Slingshot(values, screen)
bird = Bird(values, screen)
balls = Group()
birds = Group()
create_birds(values, screen, slingshot, birds)
running = True


def new_screen(values, screen, stats, result, slingshot, birds, balls, button):
    screen.fill((0, 0, 0))
    screen.blit(load_image('fon.jpg'), background_position)
    for ball in balls.sprites():
        ball.showing()
    slingshot.showing()
    birds.draw(screen)
    result.show_score()
    if not stats.action_active and not stats.pause:
        button.draw()
    pygame.display.flip()


def new_balls(values, screen, stats, result, slingshot, birds, balls):
    balls.update()
    for ball in balls.copy():
        if ball.rect.bottom <= 0:
            balls.remove(ball)
    bumps = pygame.sprite.groupcollide(balls, birds, True, True)
    if bumps:
        for birds in bumps.values():
            stats.score += values.points * len(birds)
            result.showing()
    if len(birds) == 0:
        balls.empty()
        values.speeding()
        stats.level += 1
        pygame.mixer.init()
        sound = pygame.mixer.Sound('data/level.wav')
        sound.set_volume(5)
        sound.play()
        result.show_level()
        create_birds(values, screen, slingshot, birds)


def slingshot_bump(values, stats, screen, result, slingshot, birds, balls):
    if stats.slingshots_left > 0:
        stats.slingshots_left -= 1
        result.show_lifes()
        birds.empty()
        balls.empty()
        create_birds(values, screen, slingshot, birds)
        slingshot.center_slingshot()
        sleep(0.5)
    else:
        result.hearts.empty()
        stats.action_active = False
        pygame.mouse.set_visible(True)


def bottom_bump(values, stats, screen, result, slingshot, birds, balls):
    screen_rect = screen.get_rect()
    for bird in birds.sprites():
        if bird.rect.bottom >= screen_rect.bottom:
            slingshot_bump((values, stats, screen, result, slingshot,
                           birds, balls))
            break


def moving(values, screen, stats, result, button, slingshot, birds, balls):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                slingshot.going_right = True
            elif event.key == pygame.K_LEFT:
                slingshot.going_left = True
            elif event.key == pygame.K_SPACE:
                if len(balls) < values.number_balls:
                    pygame.mixer.init()
                    shoot = pygame.mixer.Sound('data/shoot.wav')
                    shoot.play()
                    new_ball = Ball(values, screen, slingshot)
                    balls.add(new_ball)
            elif event.key == pygame.K_p and stats.action_active:
                stats.action_active = False
                stats.pause = True
                pygame.mixer.music.stop()

            elif event.key == pygame.K_p and not stats.action_active:
                stats.action_active = True
                stats.pause = False
                pygame.mixer.music.play(loops=-1)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                slingshot.going_right = False
            elif event.key == pygame.K_LEFT:
                slingshot.going_left = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            push_button(values, screen, stats, result, button, slingshot,
                        birds, balls, mouse_x, mouse_y)


def push_button(values, screen, stats, result, button, slingshot, birds,
                 balls, mouse_x, mouse_y):
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.action_active:
        values.speeds()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.action_active = True
        result.showing()
        result.show_level()
        result.show_lifes()
        birds.empty()
        balls.empty()
        create_birds(values, screen, slingshot, birds)
        slingshot.center_slingshot()


while running:
    moving(values, screen, stats, result, button, slingshot, birds, balls)
    if stats.action_active:
        slingshot.update()
        new_balls(values, screen, stats, result, slingshot, birds, balls)
        new_birds(values, stats, screen, slingshot, birds, balls)
    new_screen(values, screen, stats, result, slingshot, birds, balls, button)
    clock.tick(FPS)
pygame.quit()
