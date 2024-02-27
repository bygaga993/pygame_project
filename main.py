import pygame
import math
import random as rnd

WIDTH, HEIGHT = 1200, 800  # Размеры игрового окна
WIDTH_ZONE, HEIGHT_ZONE = 1200, 800  # Размеры игрового поля
FPS = 60  # Количествo кадров в секунду

# Инициализирование pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


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

    def start(self):
        # Запускает игру

        global camera
        self.is_running = True
        painter = Painter()
        painter.add(grid)
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

            bacterium.move()

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


if __name__ == '__main__':
    camera = Camera()
    grid = Grid(screen, camera)
    bacterium = Player(screen, camera)
    game = Game()
    game.start()
