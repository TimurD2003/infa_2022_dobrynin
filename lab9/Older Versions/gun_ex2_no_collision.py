import math
from random import choice, randint

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

pygame.font.init()
ARIAL = pygame.font.SysFont("arial", 18)

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        '''
        Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        '''
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        '''
        Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        '''

        self.x += self.vx
        self.y -= self.vy

        if self.y - self.vy >= (HEIGHT - 50) - self.r:
            self.y = (HEIGHT - 50) - self.r - 0.1  # слагаемое -0.1 для компенсации флуктуаций при остановке
            self.vy *= -0.5
            self.vx *= 0.5
        else:
            self.vy -= 1

        if self.x + self.vx >= WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx *= -1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r, 1
        )

    def hittest(self, obj):
        '''
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        '''
        x, y, r = obj.x, obj.y, obj.r
        return (x - self.x) ** 2 + (y - self.y) ** 2 < (r + self.r) ** 2


class Gun:

    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 0
        self.color = GREY

    def fire2_start(self, event):
        '''
        Запускает переход в режим прицеливания.
        '''
        self.f2_on = 1

    def fire2_end(self, event):
        '''
        Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        '''
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        '''Прицеливание. Зависит от положения мыши.'''
        if event:
            self.an = math.atan2((event.pos[1] - 450), (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        '''
        Рисует пушку на экране.
        Длина пушки пропорциональна силе выстрела,
        а цвет меняется во время прицеливания.
        '''
        gun_len = 10 + self.f2_power // 2
        x_end = 20 + gun_len * math.cos(self.an)
        y_end = 450 + gun_len * math.sin(self.an)
        pygame.draw.line(self.screen, self.color, (20, 450), (x_end, y_end), 10)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:

    def __init__(self, screen):
        self.x = randint(600, 750)
        self.y = randint(300, 500)
        self.r = randint(10, 50)
        self.color = RED
        self.screen = screen
        self.points = 0
        self.live = 1

    def new_target(self):
        '''Инициализация новой цели.'''
        self.x = randint(600, 750)
        self.y = randint(300, 500)
        self.r = randint(10, 50)
        self.live = 1

    def hit(self, points=1):
        '''Попадание шарика в цель.'''
        self.points += points
        self.live = 0

    def draw(self):
        '''Рисует цель на экране, если она не поражена'''
        if self.live:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )
            pygame.draw.circle(
                self.screen,
                BLACK,
                (self.x, self.y),
                self.r, 1
            )


def target_coll(target1, target2):
    x1, y1, r1 = target1.x, target1.y, target1.r
    x2, y2, r2 = target2.x, target2.y, target2.r

    while (x1-x2)**2 + (y1-y2)**2 <= (r1+r2)**2:
        target2.new_target()
        x2, y2, r2 = target2.x, target2.y, target2.r

    return target1, target2


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
target1, target2 = target_coll(target1, target2)
finished = False

while not finished:
    screen.fill(WHITE)
    cnt = ARIAL.render(f"{target1.points + target2.points}", True, BLACK)
    screen.blit(cnt, (50, 50))
    gun.draw()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.hit()
        if b.hittest(target2) and target2.live:
            target2.hit()
        if not (target1.live or target2.live):
            target1.new_target()
            target2.new_target()
            target1, target2 = target_coll(target1, target2)
            text = ARIAL.render(f"Вы уничтожили цели за {bullet} выстрелов", True, BLACK)
            bullet = 0
            balls = []
            for i in range(100):
                screen.fill(WHITE)
                screen.blit(text, (300, 300))
                gun.draw()

                b.draw()

                pygame.display.update()
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finished = True
                    elif event.type == pygame.MOUSEMOTION:
                        gun.targetting(event)
                b.move()
    gun.power_up()

pygame.quit()
