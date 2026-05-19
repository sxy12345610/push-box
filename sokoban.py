import pygame
import sys

# 初始化
pygame.init()
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("推箱子")

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# 地图：0空地 1墙 2玩家 3箱子 4目标点
# 简单关卡 5x5
level = [
    [1,1,1,1,1],
    [1,2,0,0,1],
    [1,0,3,0,1],
    [1,0,4,0,1],
    [1,1,1,1,1]
]

player_pos = [1,1]
box_pos = [2,2]
target_pos = [3,2]

def draw():
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 1:
                pygame.draw.rect(screen, BLACK, rect)
            elif tile == 2:
                pygame.draw.circle(screen, BLUE, rect.center, TILE_SIZE//3)
            elif tile == 3:
                pygame.draw.rect(screen, ORANGE, rect.inflate(-10,-10))
            elif tile == 4:
                pygame.draw.circle(screen, RED, rect.center, TILE_SIZE//4)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, (100,100,100), rect, 1)

def move(dx, dy):
    global player_pos, box_pos
    px, py = player_pos
    nx, ny = px+dx, py+dy
    # 检查是否撞墙
    if level[ny][nx] == 1:
        return
    # 检查是否推到箱子
    if level[ny][nx] == 3:
        bx, by = nx+dx, ny+dy
        if level[by][bx] != 1 and level[by][bx] != 3:  # 箱子前方可走
            # 移动箱子
            level[ny][nx] = 0
            level[by][bx] = 3
            box_pos = [bx, by]
            # 移动玩家
            level[py][px] = 0
            level[ny][nx] = 2
            player_pos = [nx, ny]
            # 胜利判定
            if box_pos == target_pos:
                print("You win!")
                pygame.quit()
                sys.exit()
        return
    # 空地或目标点直接走
    if level[ny][nx] == 0 or level[ny][nx] == 4:
        level[py][px] = 0
        level[ny][nx] = 2
        player_pos = [nx, ny]

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: move(-1,0)
            if event.key == pygame.K_RIGHT: move(1,0)
            if event.key == pygame.K_UP: move(0,-1)
            if event.key == pygame.K_DOWN: move(0,1)
    draw()
    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()