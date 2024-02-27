import pygame
import math
import random as rnd
import time
from itertools import cycle

WIDTH, HEIGHT = 1200, 800  # Размеры игрового окна
WIDTH_ZONE, HEIGHT_ZONE = 3000, 3000  # Размеры игрового поля
FPS = 60  # Количество кадров в секунду

# Инициализирование pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Шрифт текста
type_font = 'Verdana.ttf'
font = pygame.font.SysFont(type_font, 24, True)
big_font = pygame.font.SysFont(type_font, 28, True)


class Painter:
    # Класс, который объединяет все объекты и отрисовывает их

    def __init__(self):
        self.paints = []  # Список объектов

    def add(self, can_paint):
        # Добавляет объект

        self.paints.append(can_paint)

    def paint(self):
        # Отрисовывает все объекты

        for d in self.paints:
            d.draw()


class Game:
    # Класс игры

    def __init__(self):
        self.is_running = False
        self.pause_menu = False

    @classmethod
    def get_distance(cls, bac1, bac2):
        # Возвращает дистанцию между двумя точками
        dist_x = abs(bac1[0] - bac2[0])
        dist_y = abs(bac1[1] - bac2[1])
        return (dist_x ** 2 + dist_y ** 2) ** 0.5

    @classmethod
    def drawtext(cls, message, pos, color=(255, 255, 255)):
        # Выводит текст заданного цвета
        screen.blit(font.render(message, True, color), pos)

    def start(self):
        # Запускает игру
        global camera, game
        self.is_running = True
        painter = Painter()
        painter.add(grid)
        painter.add(cells)
        painter.add(bacterium)
        while self.is_running:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        pygame.quit()
                        quit()
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
                    quit()
                if bacterium.mass > WIDTH_ZONE - 100 or bacterium.mass <= 1:
                    bacterium.mass = WIDTH_ZONE
                    self.is_running = False
                    pygame.quit()
                    quit()

            bacterium.move()
            bacterium.collision_check(cells.cell_list)
            if camera is not None:
                camera.update(bacterium)

            screen.fill((9, 10, 21))
            painter.paint()

            pygame.display.flip()


class CanPaint:
    # Класс объектов которые отрисовываются на экране

    def __init__(self, surface, cam):
        self.surface = surface
        self.camera = cam


class Camera:
    # Класс камеры

    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = WIDTH, HEIGHT
        self.zoom = 0.5

    def centre(self, bacterium_or_position):
        # Центрирует камеру по игроку
        if isinstance(bacterium_or_position, Player):
            x, y = bacterium_or_position.x, bacterium_or_position.y
            self.x = (WIDTH / 2) - (x * self.zoom)
            self.y = (HEIGHT / 2) - (y * self.zoom)
        elif bacterium_or_position is tuple:
            self.x, self.y = bacterium_or_position

    def update(self, target):
        # Обновляет зум камеры, зависящий от набранной массы игрока
        self.zoom = 100 / target.mass + 0.3
        self.centre(bacterium)


class Grid(CanPaint):
    # Класс сетки игры

    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.color_grid = "#00bfff"

    def draw(self):
        # Рисование сетки на экране
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0, WIDTH_ZONE + 1, 50):
            pygame.draw.line(self.surface, self.color_grid, (x, y + i * zoom), (WIDTH_ZONE * zoom + x, i * zoom + y), 3)
            pygame.draw.line(self.surface, self.color_grid, (x + i * zoom, y), (i * zoom + x, WIDTH_ZONE * zoom + y), 3)


class Player(CanPaint):
    # Класс игрока

    FONT_COLOR = "#deeece"  # Цвет имени и массы игрового персонажа

    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.x, self.y = rnd.randint(300, WIDTH_ZONE - 300), rnd.randint(300, WIDTH_ZONE - 300)
        self.mass, self.speed = 20, 4
        self.outline_size = 3 + self.mass / 2
        self.color = "#00c77b"
        self.outline_color = "#007a3f"
        self.poison = False

    def collision_check(self, foods):
        # Проверяет все клетки, если игрок может съесть клетку, то удаляет её и у клетки вызывает метод действия.
        for food in foods:
            if Game().get_distance([food.x, food.y], [self.x, self.y]) <= self.mass / 2:
                food(self)
                foods.remove(food)
                cells.new_cell(rnd.choice([1, 0, 1]))

    def move(self):
        # Движение игрока
        self.outline_size = 3 + self.mass / 2
        go_x, go_y = pygame.mouse.get_pos()
        rotation = math.atan2(go_y - float(HEIGHT) / 2, go_x - float(WIDTH) / 2)
        rotation *= 180 / math.pi
        normalized = (90 - abs(rotation)) / 90
        vx = self.speed * normalized
        if rotation < 0:
            vy = -self.speed + abs(vx)
        else:
            vy = self.speed - abs(vx)

        if self.x + vx - self.outline_size < 0:
            self.x = self.outline_size
        elif self.x + vx + self.outline_size > WIDTH_ZONE:
            self.x = WIDTH_ZONE - self.outline_size
        else:
            self.x += vx

        if self.y + vy - self.outline_size < 0:
            self.y = self.outline_size
        elif self.y + vy + self.outline_size > HEIGHT_ZONE:
            self.y = HEIGHT_ZONE - self.outline_size
        else:
            self.y += vy

    def draw(self):
        # Рисует игрока
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))

        pygame.draw.circle(self.surface, self.outline_color, center, int((self.mass / 2 + 3) * zoom))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass / 2 * zoom))


class CellList(CanPaint):
    # Класс группы всех клеток

    def __init__(self, surface, cam, num):
        super().__init__(surface, cam)
        self.cell_list = []
        for _ in range(num):
            cell = self.choice_color()
            self.cell_list.append(cell)

    def new_cell(self, num=1):
        # Добавляет новую клетку
        for _ in range(num):
            self.cell_list.append(rnd.choice(
                [
                    GreenCell,
                    RedCell,
                    PurpleCell,
                    WhiteCell,
                    RainbowCell,
                    PinkCell
                ])(self.surface, self.camera))

    def draw(self):
        # Рисует все клетки
        for cell in self.cell_list:
            cell.draw()

    @staticmethod
    def choice_color():
        # С разной вероятностью возвращает один из классов клетки

        chance = rnd.randint(1, 100)

        if chance <= 70:
            return GreenCell(screen, camera)
        elif 71 <= chance <= 85:
            return RedCell(screen, camera)
        elif 86 <= chance <= 90:
            return PinkCell(screen, camera)
        elif 91 <= chance <= 95:
            return WhiteCell(screen, camera)
        elif 96 <= chance <= 100:
            return RainbowCell(screen, camera)


class Cell(CanPaint):
    # Класс обычной клетки без функции

    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.mass = 10
        self.x, self.y = rnd.randint(11, WIDTH_ZONE - 11), rnd.randint(11, WIDTH_ZONE - 11)
        colors_cells = [
            [242, 242, 101],
            [141, 6, 191],
            [141, 66, 212],
            [232, 22, 88],
            [242, 232, 33],
            [212, 55, 121],
            [22, 212, 11],
            [22, 232, 55],
            [202, 101, 252],
            [242, 151, 33]
        ]
        self.color = rnd.choice(colors_cells)
        self.do = rnd.choice([1, 2, 3])

    def draw(self):
        # Рисует клетку на поле
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        place_spawn = (int(self.x * zoom + x), int(self.y * zoom + y))
        pygame.draw.circle(self.surface, self.color, place_spawn, int(self.mass * zoom))

    def __call__(self, player):
        # Затычка для функции
        pass


class GreenCell(Cell):
    # Класс зелёной клетки, которая увеличивает массу на 1

    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.color = (0, 255, 0)

    def __call__(self, player: Player):
        # Увеличивает массу на 1
        bacterium.mass += 1


class RedCell(Cell):
    # Класс красной клетки, которая уменьшает массу на 15

    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.color = (255, 0, 0)

    def __call__(self, player: Player):
        # Уменьшает массу на 15
        bacterium.mass -= 15


class PurpleCell(Cell):
    # Класс фиолетовой клетки, которая останавливает время на 2 секунды

    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.color = (139, 0, 255)

    def __call__(self, player: Player):
        # Останавливает игру
        time.sleep(2)


class WhiteCell(Cell):
    # Класс белой клетки, которая лопает игрока

    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.color = (255, 255, 255)

    def __call__(self, player: Player):
        # Изменяет массу на 1 из-за чего игра заканчивается
        bacterium.mass = 1


class RainbowCell(Cell):
    # Класс переливающейся клетки, которая увеличивает массу на 20

    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        colors = [
            [242, 242, 101], [242, 242, 101], [242, 242, 101], [242, 242, 101], [242, 242, 101], [242, 242, 101],
            [141, 6, 191], [141, 6, 191], [141, 6, 191], [141, 6, 191], [141, 6, 191], [141, 6, 191],
            [141, 66, 212], [141, 66, 212], [141, 66, 212], [141, 66, 212], [141, 66, 212], [141, 66, 212],
            [232, 22, 88], [232, 22, 88], [232, 22, 88], [232, 22, 88], [232, 22, 88], [232, 22, 88],
            [242, 232, 33], [242, 232, 33], [242, 232, 33], [242, 232, 33], [242, 232, 33], [242, 232, 33],
            [212, 55, 121], [212, 55, 121], [212, 55, 121], [212, 55, 121], [212, 55, 121], [212, 55, 121],
            [22, 212, 11], [22, 212, 11], [22, 212, 11], [22, 212, 11], [22, 212, 11], [22, 212, 11],
            [22, 232, 55], [22, 232, 55], [22, 232, 55], [22, 232, 55], [22, 232, 55], [22, 232, 55],
            [202, 101, 252], [202, 101, 252], [202, 101, 252], [202, 101, 252], [202, 101, 252], [202, 101, 252],
            [242, 151, 33], [242, 151, 33], [242, 151, 33], [242, 151, 33], [242, 151, 33], [242, 151, 33],
        ]
        self.colors = cycle(colors)
        self.color = next(self.colors)

    def draw(self):
        # Рисует клетку на поле
        super().draw()
        self.color = next(self.colors)

    def __call__(self, player: Player):
        # Увеличивает массу на 20
        bacterium.mass += 20


class PinkCell(Cell):
    # Класс зелёной клетки, которая имеет функцию одной из других клеток

    def __init__(self, surface, cam):
        super().__init__(surface, cam)
        self.color = (255, 155, 170)
        self.do = CellList.choice_color()

    def __call__(self, player: Player):
        # Выполняет функцию клетки
        self.do(player)


if __name__ == '__main__':
    camera = Camera()
    grid = Grid(screen, camera)
    cells = CellList(screen, camera, 700)
    bacterium = Player(screen, camera)
    game = Game()
    game.start()
