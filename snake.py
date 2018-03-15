import pygame
from random import randint
from abc import ABCMeta, abstractmethod

BLACK_COLOR = (0, 0, 0)  # 全局常量，黑色
RED_COLOR = (255, 0, 0)  # 全局常量，红色
FOOD_COLOR = (230, 185, 185)  # 全局常量，食物的颜色
GREEN_COLOR = (0, 255, 0)  # 绿色

UP = 0  # 向上
RIGHT = 1  # 向右
DOWN = 2  # 向下
LEFT = 3  # 向左


class GameObject(object, metaclass=ABCMeta):
    """游戏物品抽象父类"""

    def __init__(self, pos=(0, 0), color=BLACK_COLOR):
        """初始化方法"""
        self._pos = pos  # 在界面中的位置
        self._color = color  # 在界面中的颜色

    @abstractmethod
    def draw(self, screen):
        """
        抽象方法，绘制对象

        :param screen: 在哪个图像表面层绘画
        :return: None
        """
        pass

    @property
    def pos(self):
        """
        装饰器修饰，直接获取对象在界面中的位置

        :return: 元组，(x,y)
        """
        return self._pos


class Wall(GameObject):
    """四周墙的类"""

    def __init__(self, pos, width, height, tick, color=BLACK_COLOR):
        """
        初始化、构造方法

        :param pos: 墙开始画的坐标点
        :param width: 墙的宽度
        :param height: 墙的高度
        :param tick: 墙的厚度
        :param color: 墙的颜色
        """
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
    """食物类"""

    def __init__(self, pos, size=10, color=RED_COLOR):
        """
        初始化方法

        :param pos: 外切圆坐标
        :param color:
        :param size:
        """
        super().__init__(pos, color)
        self._is_hide = 0  # 是否隐藏的计数器，为了食物点不频繁的闪烁
        self._size = size  # 食物点的大小，直径

    def draw(self, screen):
        """
        绘制食物的方法

        :param screen: 在哪个表面绘制
        :return: None
        """
        # 如果不是5的倍数，就消失一次，减少Boolean值的频繁闪烁，数值越大闪烁越快
        if self._is_hide % 5 != 0:
            # 开始在界面进行绘制食物
            pygame.draw.circle(screen, self._color,
                               (self._pos[0] + self._size // 2, self._pos[1] + self._size // 2),
                               self._size // 2, 0)
        self._is_hide += 1  # 计数点自加


class SnakeNode(GameObject):
    """蛇的结点类"""

    def __init__(self, pos, size, color=GREEN_COLOR):
        """
        初始化构造方法

        :param pos: 结点的坐标
        :param size: 结点的大小
        :param color: 结点的颜色
        """
        super().__init__(pos, color)
        self._size = size

    def draw(self, screen):
        """
        绘制结点

        :param screen: 在哪个表面进行绘制
        :return: None
        """
        # 绘制内部绿色的结点
        pygame.draw.rect(screen, self._color,
                         (self._pos[0], self._pos[1], self._size, self._size), 0)
        # 绘制结点的外部边框
        pygame.draw.rect(screen, BLACK_COLOR,
                         (self._pos[0], self._pos[1], self._size, self._size), 1)

    @property
    def size(self):
        """
        装饰器，修饰get_size方法

        :return: 结点的大小
        """
        return self._size


class Snake(GameObject):
    """蛇的类"""

    def __init__(self):
        """
        初始化构造方法

        """
        super().__init__()
        self._snake_dir = LEFT  # 默认的蛇爬行的方向为左
        self._nodes = []  # 蛇的结点容器
        self._aline = True  # 蛇是否存活
        self._eat_food = False  # 是否吃到食物
        for index in range(5):  # 初始化5个结点在列表容器中
            node = SnakeNode((290 + index * 20, 250), 20)
            self._nodes.append(node)

    def is_in_nodes(self, x, y):
        """
        判断刷新出来的苹果是否在蛇的结点上

        :param x:  食物的x坐标
        :param y:  食物的y坐标
        :return: boolean 值，在为True，不在为False
        """
        for node in self._nodes:
            if node.pos[0] == x and node.pos[1] == y:
                return True
        return False

    @property
    def aline(self):
        """
        装饰器，获取对象属性

        :return: aline属性
        """
        return self._aline

    @property
    def snake_dir(self):
        """
        装饰器，获取蛇移动的方向

        :return: snake_dir 属性
        """
        return self._snake_dir

    @property
    def head(self):
        """
        装饰器，获取容器中的第一个结点

        :return: nodes[0] 第一个元素
        """
        return self._nodes[0]

    def change_dir(self, new_dir):
        """
        改变蛇前进的方向

        :param new_dir:  前进的新方向
        :return: None
        """
        # 如果方向和原来方向不同，而且相反，就可以改变，蛇的前进方向
        if new_dir != self._snake_dir and (self._snake_dir + new_dir) % 2 != 0:
            self._snake_dir = new_dir

    def draw(self, screen):
        """
        画出蛇

        :param screen: 在哪个表面画蛇
        :return: None
        """
        # 遍历结点，同时画出结点
        for node in self._nodes:
            node.draw(screen)

    def move(self):
        """
        蛇移动的方法

        :return: None
        """
        # if self._aline:
        head = self.head  # 获取蛇头
        snake_dir = self._snake_dir  # 获取蛇前进的方向
        # 获取蛇头想x,y坐标和头的大小
        x, y, size = head.pos[0], head.pos[1], head.size
        if snake_dir == UP:  # 向上移动
            y -= size  # y坐标减少
        elif snake_dir == RIGHT:  # 向右移动
            x += size  # x坐标增加
        elif snake_dir == DOWN:  # 向下移动
            y += size  # y坐标增加
        else:  # 向左移动
            x -= size  # x坐标减少
        new_head = SnakeNode((x, y), size)  # 新建一个结点对象
        self._nodes.insert(0, new_head)  # 添加到蛇头
        if self._eat_food:  # 如果吃到了食物
            self._eat_food = False  # 重设参数为没吃到，同时不移除最后的一个结点
        else:  # 没吃到食物
            self._nodes.pop()  # 移除最后的一个结点元素

    def collide(self, wall):
        """
        判断是否撞墙

        :param wall: 墙的对象
        :return: None
        """
        x, y = wall.pos  # 获取墙的坐标
        width = wall.width  # 获取墙的宽
        height = wall.height  # 获取墙的高
        node_one = self._nodes[0]  # 获取蛇头对象
        # 如果蛇头的x坐标小于了墙的最左边，或加上自身宽度大于了墙的初始位置加宽度，
        # 或蛇头的y坐标小于了墙最上面，或加上自身宽度大于了墙初始xy位置加高度
        if x > node_one.pos[0] or node_one.pos[0] + node_one.size > x + width \
                or y > node_one.pos[1] or node_one.pos[1] + node_one.size > y + height:
            self._aline = False  # 蛇撞到墙，死了
        else:
            self._aline = True  # 蛇没撞到墙，还或者

    def eat_food(self, food):
        """
        蛇吃食物的行为

        :param food: food对象
        :return: Boolean 是否吃到
        """
        head = self.head  # 获取蛇头结点
        # 如果蛇头的x,y坐标与食物的x,y坐标重合,那么就吃到了食物
        if head.pos[0] == food.pos[0] and head.pos[1] == food.pos[1]:
            self._eat_food = True  # 吃到食物的状态为True
            return True  # 返回True
        return False  # 没吃到食物返回False

    def eat_me(self):
        """
        吃自己判断

        :return: None
        """
        head = self.head  # 获取蛇头结点对象
        # 从蛇的第4个结点开始遍历，因为，蛇只能吃到自己的第四个结点
        for index in range(3, len(self._nodes)):
            # 如果蛇头坐标和蛇身坐标重合，就吃到了自己
            if head.pos[0] == self._nodes[index].pos[0] and \
                    head.pos[1] == self._nodes[index].pos[1]:
                self._aline = False  # 修改当前蛇的存活状态

    @property
    def snake_len(self):
        """
        获取蛇的结点长度

        :return: 蛇的长度
        """
        return len(self._nodes)


def main():
    """游戏主函数"""

    def refresh():
        """刷新游戏窗口"""
        screen.fill((242, 242, 242))
        snake.draw(screen)
        food.draw(screen)
        wall.draw(screen)
        pygame.display.flip()

    def handle_key_event(key_event):
        """游戏按键事件监听"""
        key = key_event.key  # 拿取到所按的按键的值
        if key == pygame.K_F2:  # 如果为F2则重新开始游戏
            reset_game()
        # 如果key为w,a,s,d则为方向控制
        elif key in (pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a):
            if snake.aline:  # 如果蛇还活着则进行操作
                if key == pygame.K_w:  # 按下了W
                    new_dir = UP  # 设置新的方向向上
                elif key == pygame.K_d:  # 按下了D
                    new_dir = RIGHT  # 设置新的方向向右
                elif key == pygame.K_s:  # 按下了S
                    new_dir = DOWN  # 设置新的方向向下
                else:  # 按下了A
                    new_dir = LEFT  # 设置新的方向向左
                snake.change_dir(new_dir)  # 调用蛇的方法，发送消息改变方向
        pygame.event.clear()  # 清除按键事件

    def reset_game():
        """重设游戏的食物和蛇的对象，游戏重开"""
        nonlocal food, snake, game_over  # 设置为嵌套值域，而非当前函数
        food = create_apple(snake)  # 创建新的食物对象
        snake = Snake()  # 创建新的蛇对象
        game_over = False  # 游戏继续

    scores = []  # 分数容器
    pygame.init()  # 初始化pygame
    wall = Wall((10, 10), 600, 600, 3)  # 创建墙的对象
    screen = pygame.display.set_mode([620, 620])  # 设置窗口大小
    screen.fill((242, 242, 242))  # 设置填充的背景
    pygame.display.set_caption('贪吃蛇')  # 设置窗口标题
    pygame.display.flip()  # 刷新界面
    clock = pygame.time.Clock()  # 设置时钟
    snake = Snake()  # 初始化一个蛇对象
    food = create_apple(snake)  # 初始化一个食物对象
    reset_game()  # 重开游戏，刷新界面
    is_running = True  # 游戏运行状态
    game_over = False  # 游戏当前回合状态
    while is_running:
        for event in pygame.event.get():  # 获取事件
            if event.type == pygame.QUIT:  # 判断事件类型是否为退出
                is_running = False
            elif event.type == pygame.KEYDOWN:
                handle_key_event(event)  # 传递按钮点击事件
        if not game_over:  # 本回合是否继续
            if snake.aline:  # 当前蛇是否还存活
                refresh()  # 刷新游戏窗口
                snake.move()  # 蛇开始移动
                snake.collide(wall)  # 判断蛇是否撞墙
                snake.eat_me()  # 判断蛇是否吃到自己
                if snake.eat_food(food):  # 判断蛇是否吃到食物
                    food = create_apple(snake)  # 吃到食物，创建一个新的食物对象
            else:  # 本回合结束
                game_over = True  # 设置本回合结束
                scores.append(snake.snake_len - 5)  # 将分数添加到容器中
                show_info(screen, scores)  # 显示分数
        clock.tick(5)  # 帧数
    pygame.quit()  # 销毁pygame
    pass


def show_info(screen, scores):
    """
    在界面中绘制分数的函数

    :param screen:  绘制的表面
    :param scores:  绘制的分数列表
    :return:  None
    """
    scores.sort(reverse=True)  # 对分数进行排序
    my_font = pygame.font.SysFont('宋体', 60)  # 设置字体格式
    game_over = my_font.render('GAME OVER', False, [0, 0, 0])  # 字体的文本和颜色
    screen.blit(game_over, (180, 260))  # 开始绘制的坐标
    list_len = len(scores) if len(scores) < 5 else 5  # 获取分数容器的大小，最多展示前五
    for index in range(list_len):  # 遍历欠前五的分数
        my_font = pygame.font.SysFont('宋体', 40)  # 设置字体
        # 绘制的文字内容和分数
        score = my_font.render('Number ' + str(index + 1) + ':' + str(scores[index]), False, [255, 0, 0])
        screen.blit(score, (200, 300 + index * 40))  # 绘制的位置
    pygame.display.flip()  # 刷新界面


def create_apple(snake):
    """
    创建苹果在蛇的身体之外

    :param snake:  蛇的对象
    :return: 在蛇身之外的Food坐标
    """
    row = randint(0, 29)  # 随机行号
    col = randint(0, 29)  # 随机列号
    x, y = 10 + 20 * col, 10 + 20 * row  # 换算为对应的坐标点
    if not snake.is_in_nodes(x, y):  # 如果不在蛇身上
        return Food((10 + 20 * col, 10 + 20 * row), 20)  # 返回一个食物对象
    else:
        create_apple(snake)  # 递归调用函数直到有返回值


if __name__ == '__main__':
    main()
