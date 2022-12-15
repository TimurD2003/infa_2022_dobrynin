import pygame
from pygame.draw import *
from random import randint, uniform

pygame.init()

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)         #инициализация шрифта для надписи очков

FPS = 60                                                #число обновлений кадров в секунду

SCR_SIZE = (1200, 800)                                  #размеры окна в формате (ширина, высота)
screen = pygame.display.set_mode(SCR_SIZE)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]      #набор цветов для шаров

score = 0                                               # начальное значение очков игрока

FIG = ["circle", "square"]                              #массив с названиями типов фигур
figs = []                                               #массив для данных о фигурах
figs_number = 7                                         #число фигур, которые одновременно появляются на экране


def dist(dot1, dot2):
    '''
    Считает расстояние между 2 точками на плоскости.
    dot1 - кортеж с координатами точки 1,
    dot2 - кортеж с координатами точки 2.
    '''
    dist = (dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2
    dist = dist**0.5
    return dist


def bound(x, min_ ,max_):
    '''
    Ограничивает значение некоторой вещественной переменной
    по модулю в пределах min_>0 и max_>0.
    '''
    if abs(x) < min_:
        return min_*x/abs(x)
    if abs(x) > max_:
        return max_*x/abs(x)
    return x


def show_score():
    '''
    Выводит очки игрока в верхний левый угол экрана.
    '''
    global score
    text_surface = font.render(f'Score:{score}', True, (0, 0, 0))
    screen.blit(text_surface, (50, 20))


def new_fig():
    '''
    Создает словарь fig_prop с данными о фигуре: шаре радиуса r или квадрате стороной r
    цвета color, с центром в точке center = [x, y] и скоростью по осям speed = [dx, dy].
    Цвет, размер, тип фигуры, скорость и координаты центра выбираются случайно.
    '''
    r = randint(20,100)
    fig_prop = {
                "figure": FIG[randint(0, 1)],
                "radius": r,
                "center": [randint(r, SCR_SIZE[i] - r) for i in range(2)],
                "speed": [randint(3,12) for i in range(2)],
                "color": COLORS[randint(0, 5)]
                }

    return fig_prop


def create_square(fig_dict):
    '''
    Принимает словарь, созданный с помощью функции new_fig,
    в котором fig_dict["figure"] == "square".
    По данным из словаря создаёт объект square типа pygame.draw.rect
    с центром в точке fig_dict["center"] и со стороной fig_dict["radius"].
    '''
    r = fig_dict["radius"]
    square = pygame.Rect([[fig_dict["center"][j] - r//2 for j in range(2)],[r, r]])

    return square


def speed(fig, r, center, speed):
    '''
    Осуществляет изменение положения фигуры.
    Принимает на вход размер фигуры (int),
    её координаты и скорость по осям (2 списка из 2 элементов).
    Возвращает новые координаты и новую скорость
    в виде 2 списков из 2 элементов.
    Если фигура - квадрат, то скорость также случайным образом меняется.
    Для всех типов фигур реализован отскок от стен.
    '''
    if fig == "square": speed = [bound(speed[i]*uniform(0.5, 1.5),5,15) for i in range(2)]
    
    for i in range(2):
        if (center[i] + speed[i] > SCR_SIZE[i]-r) or (center[i] + speed[i] < r):
            speed[i] *= -1

        center[i] += speed[i]

    return center, speed


def generate_figs():
    '''
    Обрабатывает массив с данными фигур, тем самым меняя их положение на экране.
    При первом запуске заполняет пустой массив figs
    с помощью функции new_fig(), при последующих запусках
    изменяет положение каждого объекта с помощью функции speed().
    '''
    global figs, figs_number, screen

    for i in range(figs_number):

        if (not figs) or (len(figs) < figs_number):
            figs.append(new_fig())
        else:
            figs[i]["center"], figs[i]["speed"] = speed(figs[i]["figure"], figs[i]["radius"],
                                             figs[i]["center"], figs[i]["speed"])

        if figs[i]["figure"] == "circle":
            circle(screen, figs[i]["color"],
                   figs[i]["center"], figs[i]["radius"])
        else:
            square = create_square(figs[i])
            rect(screen, figs[i]["color"], square)


def click(event):
    '''
    Обрабатывает нажатие левой кнопки мыши.
    В данной версии - увеличивает очки игрока при нажатии на шар,
    а затем генерирует новый шар.
    '''
    global score, figs, figs_number
    for i in range(figs_number):
        f = figs[i]["figure"]
        if f == "circle":
            if dist(event.pos, figs[i]["center"]) < figs[i]["radius"]:
                score += 1
                figs[i] = new_fig()
        else:
            square = create_square(figs[i])
            if square.collidepoint(event.pos):
                score += 5
                figs[i] = new_fig()


screen.fill(WHITE)                                  #заполняет стартовый экран белым цветом
pygame.display.update()

clock = pygame.time.Clock()
finished = False

while not finished:
    generate_figs()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)

    show_score()
    pygame.display.update()
    screen.fill(WHITE)                              #освобождает экран для следующего шага

pygame.quit()
