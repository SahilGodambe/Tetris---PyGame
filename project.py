import pygame
from copy import deepcopy
from random import choice, randrange

W, H = 11, 20
TILE = 35
GAME_RES = W * TILE, H * TILE
RES = 700, 750
FPS = 60

scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

def get_color():
    return (randrange(30, 256), randrange(30, 256), randrange(30, 256))

def check_borders(figure, field):
    for i in range(4):
        if figure[i].x < 0 or figure[i].x >= W or figure[i].y >= H:
            return False
        elif figure[i].y >= 0 and field[figure[i].y][figure[i].x]:
            return False
    return True

def get_record(filename='record'):
    try:
        with open(filename) as f:
            return int(f.readline())
    except FileNotFoundError:
        with open(filename, 'w') as f:
            f.write('0')
        return 0

def set_record(record, score, filename='record'):
    rec = max(int(record), score)
    with open(filename, 'w') as f:
        f.write(str(rec))

def main():
    pygame.init()
    sc = pygame.display.set_mode(RES)
    game_sc = pygame.Surface(GAME_RES)
    clock = pygame.time.Clock()

    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
    figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 1, TILE - 1)
    field = [[0 for _ in range(W)] for _ in range(H)]

    bg = pygame.image.load('img/bg.jpg').convert()
    game_bg = pygame.image.load('img/bg2.jpg').convert()
    main_font = pygame.font.Font('font/font.ttf', 65)
    font = pygame.font.Font('font/font.ttf', 45)

    title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
    title_score = font.render('score:', True, pygame.Color('green'))
    title_record = font.render('record:', True, pygame.Color('purple'))

    def draw_start_screen():
        sc.blit(bg, (0, 0))
        title = main_font.render("TETRIS", True, pygame.Color("orange"))
        prompt = font.render("Press any key to Start", True, pygame.Color("white"))
        sc.blit(title, (RES[0] // 2 - title.get_width() // 2, 300))
        sc.blit(prompt, (RES[0] // 2 - prompt.get_width() // 2, 400))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    return

    def draw_game_over(score):
        sc.blit(bg, (0, 0))
        over = main_font.render("GAME OVER", True, pygame.Color("red"))
        final_score = font.render(f"Score: {score}", True, pygame.Color("white"))
        prompt = font.render("Press any key to Restart", True, pygame.Color("yellow"))
        sc.blit(over, (RES[0] // 2 - over.get_width() // 2, 300))
        sc.blit(final_score, (RES[0] // 2 - final_score.get_width() // 2, 400))
        sc.blit(prompt, (RES[0] // 2 - prompt.get_width() // 2, 500))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    return

    fall_speed = 500
    last_fall_time = pygame.time.get_ticks()
    draw_start_screen()

    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    color, next_color = get_color(), get_color()
    score, anim_speed, lines = 0, 60, 0

    while True:
        record = get_record()
        dx, rotate = 0, False
        sc.blit(bg, (0, 0))
        sc.blit(game_sc, (20, 20))
        game_sc.blit(game_bg, (0, 0))

        for i in range(lines):
            pygame.time.wait(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    fall_speed = 50
                elif event.key == pygame.K_UP:
                    rotate = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    fall_speed = 500

        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
        if not check_borders(figure, field):
            figure = deepcopy(figure_old)

        current_time = pygame.time.get_ticks()
        if current_time - last_fall_time > fall_speed:
            last_fall_time = current_time
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
            if not check_borders(figure, field):
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()

        center = figure[0]
        if rotate:
            figure_old = deepcopy(figure)
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
            if not check_borders(figure, field):
                figure = deepcopy(figure_old)

        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1

        score += scores[lines]

        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, color, figure_rect)

        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)

        PREVIEW_X, PREVIEW_Y = 480, 180
        for i in range(4):
            figure_rect.x = PREVIEW_X + (next_figure[i].x - W // 2 + 1) * TILE
            figure_rect.y = PREVIEW_Y + (next_figure[i].y + 1) * TILE
            pygame.draw.rect(sc, next_color, figure_rect)

        sc.blit(title_tetris, (440, 50))
        sc.blit(title_score, (480, 500))
        sc.blit(font.render(str(score), True, pygame.Color('white')), (495, 550))
        sc.blit(title_record, (470, 600))
        sc.blit(font.render(str(record), True, pygame.Color('gold')), (495, 640))

        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                draw_game_over(score)
                field = [[0 for _ in range(W)] for _ in range(H)]
                figure = deepcopy(choice(figures))
                next_figure = deepcopy(choice(figures))
                color, next_color = get_color(), get_color()
                score = 0
                fall_speed = 500
                last_fall_time = pygame.time.get_ticks()
                draw_start_screen()
                break

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
