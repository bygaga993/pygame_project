import pygame

WIDTH, HEIGHT = 1200, 800  # Размеры игрового окна
WIDTH_ZONE, HEIGHT_ZONE = 3000, 3000  # Размеры игрового поля
FPS = 60  # Фиксация количества кадров в секунду

# Инициализирование pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


class Painter:
    # Класс, который объединяет все объекты и отрисовывает их

    def __init__(self):
        self.paints = []  # Cписок объектов

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
        self.is_running = True
        painter = Painter()
        painter.add(grid)
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

            screen.fill((9, 10, 21))
            painter.paint()

            pygame.display.flip()


class Grid:
    # Класс сетки игры

    def __init__(self, surface):
        self.surface = surface
        self.color_grid = "#00bfff"

    def draw(self):
        # Рисование сетки на экране
        for i in range(0, WIDTH_ZONE + 1, 50):
            pygame.draw.line(self.surface, self.color_grid, (0, i), (WIDTH_ZONE, i), 3)
            pygame.draw.line(self.surface, self.color_grid, (i, 0), (i, WIDTH_ZONE), 3)


if __name__ == '__main__':
    grid = Grid(screen)

    game = Game()
    game.start()