import pygame
from random import randint
from abc import ABCMeta, abstractmethod

BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
FOOD_COLOR = (230, 185, 185)
GREEN_COLOR = (0, 255, 0)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class GameObject(object, metaclass=ABCMeta):
    def __init__(self, pos=(0, 0), color=BLACK_COLOR):
        self._pos = pos
        self._color = color

    @abstractmethod
    def draw(self, screen):
        pass

    @property
    def pos(self):
        return self._pos


class Wall(GameObject):
    def __init__(self, pos, width, height, tick, color=BLACK_COLOR):
        super().__init__(pos, color)
        self._width = width
        self._height = height
        self._tick = tick

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def draw(self, screen):
        pygame.draw.rect(screen, self._color,
                         (self._pos[0], self._pos[1], self._width, self._height), self._tick)


class Food(GameObject):
    def __init__(self, pos, size=10, color=RED_COLOR):
        """
        初始化方法
        :param pos: 外切圆坐标
        :param color:
        :param size:
        """
        super().__init__(pos, color)
        self._is_hide = 0
        self._size = size

    def draw(self, screen):
        if self._is_hide % 5 != 0:
            pygame.draw.circle(screen, self._color,
                               (self._pos[0] + self._size // 2, self._pos[1] + self._size // 2),
                               self._size // 2, 0)
        self._is_hide += 1


class SnakeNode(GameObject):
    def __init__(self, pos, size, color=GREEN_COLOR):
        super().__init__(pos, color)
        self._size = size

    def draw(self, screen):
        pygame.draw.rect(screen, self._color,
                         (self._pos[0], self._pos[1], self._size, self._size), 0)
        pygame.draw.rect(screen, BLACK_COLOR,
                         (self._pos[0], self._pos[1], self._size, self._size), 1)

    @property
    def size(self):
        return self._size


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self._snake_dir = LEFT
        self._nodes = []
        self._aline = True
        self._eat_food = False
        for index in range(5):
            node = SnakeNode((290 + index * 20, 250), 20)
            self._nodes.append(node)

    @property
    def aline(self):
        return self._aline

    @property
    def snake_dir(self):
        return self._snake_dir

    @property
    def head(self):
        return self._nodes[0]

    def change_dir(self, new_dir):
        if new_dir != self._snake_dir and (self._snake_dir + new_dir) % 2 != 0:
            self._snake_dir = new_dir

    def draw(self, screen):
        for node in self._nodes:
            node.draw(screen)

    def move(self):
        # if self._aline:
        head = self.head
        snake_dir = self._snake_dir
        x, y, size = head.pos[0], head.pos[1], head.size
        if snake_dir == UP:
            y -= size
        elif snake_dir == RIGHT:
            x += size
        elif snake_dir == DOWN:
            y += size
        else:
            x -= size
        new_head = SnakeNode((x, y), size)
        self._nodes.insert(0, new_head)
        if self._eat_food:
            self._eat_food = False
        else:
            self._nodes.pop()

    def collide(self, wall):
        x, y = wall.pos
        width = wall.width
        height = wall.height
        node_one = self._nodes[0]
        if x > node_one.pos[0] or node_one.pos[0] + node_one.size > x + width \
                or y > node_one.pos[1] or node_one.pos[1] + node_one.size > y + height:
            self._aline = False
        else:
            self._aline = True

    def eat_food(self, food):
        head = self.head
        if head.pos[0] == food.pos[0] and head.pos[1] == food.pos[1]:
            self._eat_food = True
            return True
        return False

    def eat_me(self):
        head = self.head
        for index in range(3, len(self._nodes)):
            if head.pos[0] == self._nodes[index].pos[0] and \
                    head.pos[1] == self._nodes[index].pos[1]:
                self._aline = False

    @property
    def snake_len(self):
        return len(self._nodes)


def main():
    def refresh():
        """刷新游戏窗口"""
        screen.fill((242, 242, 242))
        snake.draw(screen)
        food.draw(screen)
        wall.draw(screen)
        pygame.display.flip()

    def handle_key_event(key_event):
        key = key_event.key
        if key == pygame.K_F2:
            reset_game()
        elif key in (pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a):
            if snake.aline:
                if key == pygame.K_w:
                    new_dir = UP
                elif key == pygame.K_d:
                    new_dir = RIGHT
                elif key == pygame.K_s:
                    new_dir = DOWN
                else:
                    new_dir = LEFT

                snake.change_dir(new_dir)
        pygame.event.clear()

    def create_apple():
        row = randint(0, 29)
        col = randint(0, 29)
        x, y = 10 + 20 * col, 10 + 20 * row
        return Food((10 + 20 * col, 10 + 20 * row), 20)

    def reset_game():
        nonlocal food, snake
        food = create_apple()
        snake = Snake()

    pygame.init()  # 初始化pygame
    wall = Wall((10, 10), 600, 600, 3)
    screen = pygame.display.set_mode([620, 620])  # 设置窗口大小
    screen.fill((242, 242, 242))  # 设置填充的背景
    pygame.display.set_caption('贪吃蛇')
    pygame.display.flip()  # 刷新界面
    clock = pygame.time.Clock()  # 设置时钟
    food = create_apple()
    snake = Snake()
    reset_game()
    is_running = True
    while is_running:

        for event in pygame.event.get():  # 获取事件
            if event.type == pygame.QUIT:  # 判断事件类型是否为退出
                is_running = False
            elif event.type == pygame.KEYDOWN:
                handle_key_event(event)
        if snake.aline:
            refresh()
            snake.move()
            snake.collide(wall)
            snake.eat_me()
            if snake.eat_food(food):
                food = create_apple()
        else:
            show_info(screen, snake)
        clock.tick(5)  # 1 帧数
    pygame.quit()  # 销毁pygame
    pass


def show_info(screen, snake):
    score = snake.snake_len - 5
    my_font = pygame.font.SysFont('宋体', 60)
    game_over = my_font.render('GAME OVER', False, [0, 0, 0])
    score = my_font.render('score:' + str(score), False, [255, 0, 0])
    screen.blit(score, (400, 30))
    screen.blit(game_over, (180, 260))
    pygame.display.flip()


if __name__ == '__main__':
    main()
