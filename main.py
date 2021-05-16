import random
import pygame
import tkinter as tk
from tkinter import messagebox

# game field
width = 500
rows = 20


class SnakePixel(object):
    # class which creates wall-, snake and snack pixel and the eyes of the snake
    global rows
    global width

    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.dirtx = 1
        self.dirty = 0
        self.color = color

    def move(self, dirtx, dirty):
        self.dirtx = dirtx
        self.dirty = dirty
        self.pos = (self.pos[0] + self.dirtx, self.pos[1] + self.dirty)

    def draw(self, surface, eyes=False):
        dis = width // rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        # draw the eyes of the snake
        if eyes:
            centre = dis // 2
            radius = 3
            left_eye = (i * dis + centre - radius, j * dis + 8)
            right_eye = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), left_eye, radius)
            pygame.draw.circle(surface, (0, 0, 0), right_eye, radius)


class Snake(object):
    # class which makes the snake movable
    global rows

    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = SnakePixel(pos)
        self.body.append(self.head)
        self.dirtx = 0
        self.dirty = 1

    def move(self):
        global rows

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            # gameplay with arrows
            if keys[pygame.K_LEFT]:
                self.dirtx = -1
                self.dirty = 0
                self.turns[self.head.pos[:]] = [self.dirtx, self.dirty]

            elif keys[pygame.K_RIGHT]:
                self.dirtx = 1
                self.dirty = 0
                self.turns[self.head.pos[:]] = [self.dirtx, self.dirty]

            elif keys[pygame.K_UP]:
                self.dirtx = 0
                self.dirty = -1
                self.turns[self.head.pos[:]] = [self.dirtx, self.dirty]

            elif keys[pygame.K_DOWN]:
                self.dirtx = 0
                self.dirty = 1
                self.turns[self.head.pos[:]] = [self.dirtx, self.dirty]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirtx == -1 and c.pos[0] <= 0:
                    c.pos = (rows - 1, c.pos[1])
                elif c.dirtx == 1 and c.pos[0] >= rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirty == 1 and c.pos[1] >= rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirty == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], rows - 1)
                else:
                    c.move(c.dirtx, c.dirty)

    def reset_game(self, pos):
        # restart if you lose
        self.head = SnakePixel(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirtx = 0
        self.dirty = 1

    def add_pixel(self):
        # grows up the snake
        snake_tail = self.body[-1]
        dx, dy = snake_tail.dirtx, snake_tail.dirty

        # add a pixel tail to the snake, depend of the direction of the snake
        if dx == 1 and dy == 0:
            self.body.append(SnakePixel((snake_tail.pos[0] - 1, snake_tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(SnakePixel((snake_tail.pos[0] + 1, snake_tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(SnakePixel((snake_tail.pos[0], snake_tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(SnakePixel((snake_tail.pos[0], snake_tail.pos[1] + 1)))

        self.body[-1].dirtx = dx
        self.body[-1].dirty = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                # snake head get eyes
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, r, surface):
    # draw the grid

    field_size = w // r

    x = 0
    y = 0

    for l in range(r):
        x = x + field_size
        y = y + field_size

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def draw_wall(cor, surface):
    for i in range(len(cor)):
        SnakePixel(cor[i], color=(151, 255, 255)).draw(surface)


def redraw_window(surface):
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    if wall:
        draw_wall(cords, surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def free_field(r, item):

    # calculate which fields are free
    positions = item.body

    while True:
        x = random.randrange(r)
        y = random.randrange(r)
        # check snake position
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            if wall:
                # check wall collision
                if collision_wall(x, y):
                    continue
                else:
                    break
            else:
                break

    return x, y


def random_wall(r, item):
    # generate matrix for wall fields
    positions = item.body
    wall_cords = []
    for i in range(10):
        cord = []
        while True:
            x = random.randrange(r)
            y = random.randrange(r)
            # check snake position
            if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
                continue
            else:
                cord.append(x)
                cord.append(y)
                break
        wall_cords.append(cord)
    return wall_cords


def end_message(subject, content):
    # message if you lose
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    msg = messagebox.askokcancel(subject, content)
    root.destroy()
    return msg


def first_question(subject, content):
    # message for the beast mode
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    msg = messagebox.askyesnocancel(subject, content)
    root.destroy()
    return msg


def collision_wall(x, y):
    # check if there is a wall
    for i in range(len(cords)):
        if int(x) == int(cords[i][0]) and int(y) == int(cords[i][1]):
            return True


def final():
    pygame.display.set_caption('My first snake game - YOU LOOSE')
    msg_return = end_message('Game over', 'Your score: ' + str(len(s.body)) + "\nPlay again?")
    if msg_return:
        pygame.display.set_caption('My first snake game')

    return msg_return


def main():
    # main part, controls the game
    global rows, width, s, snack, wall, cords

    speed = 10
    wall = False
    start_pos = 10
    question = first_question('difficulty', 'Heavy mode on?')

    # quit game
    if question is None:
        print("quit game")
    else:

        win = pygame.display.set_mode((width, width))
        pygame.display.set_caption('My first snake game')
        s = Snake((255, 0, 0), (10, 10))

        # if you choose beast mode
        if question:
            speed = 15
            wall = True
            cords = random_wall(rows, s)
            draw_wall(cords, win)

        snack = SnakePixel(free_field(rows, s), color=(0, 255, 0))
        clock = pygame.time.Clock()

        while True:
            pygame.time.delay(50)
            clock.tick(speed)
            s.move()

            # snake found snack
            if s.body[0].pos == snack.pos:
                s.add_pixel()
                snack = SnakePixel(free_field(rows, s), color=(0, 255, 0))

            # snake found wall
            if wall:
                if collision_wall(s.body[0].pos[0], s.body[0].pos[1]):
                    msg = final()
                    if msg:
                        # restart game
                        s.reset_game((start_pos, start_pos))
                    else:
                        # quit game
                        pygame.quit()
                        exit()

            # snake found snake
            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                    msg = final()
                    if msg:
                        # restart game
                        s.reset_game((start_pos, start_pos))
                        break
                    else:
                        # quit game
                        pygame.quit()
                        exit()
                        break
            redraw_window(win)
        pass


main()
