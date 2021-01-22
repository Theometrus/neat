import sys

import pygame as pg
from pygame import gfxdraw

from classes.Puppeteers.Population import Population
from config.settings import RESOLUTION, BG_COLOR


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pg.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pg.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2),
                      self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def main():
    pg.init()
    pg.display.set_caption("NEAT")
    screen = pg.display.set_mode(RESOLUTION)
    bg_color = BG_COLOR

    # =========================================== #
    pop = Population(None)

    b1 = Button((255, 255, 255), 10, 10, 130, 40, "Add node")
    b2 = Button((255, 255, 255), 150, 10, 130, 40, "Add link")
    b3 = Button((255, 255, 255), 290, 10, 130, 40, "Toggle connection")
    b4 = Button((255, 255, 255), 430, 10, 130, 40, "Shift weight")
    b5 = Button((255, 255, 255), 570, 10, 130, 40, "Reassign weight")

    # =========================================== #

    running = True
    while running:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False

            # checks if a mouse is clicked
            if ev.type == pg.MOUSEBUTTONDOWN:
                if b1.is_over(mouse):
                    pop.networks[0].genome.mutate_add_node()
                if b2.is_over(mouse):
                    pop.networks[0].genome.mutate_add_link()
                if b3.is_over(mouse):
                    pop.networks[0].genome.mutate_toggle_link()
                if b4.is_over(mouse):
                    print("Shift weight")
                if b5.is_over(mouse):
                    print("Reassign weight")

        screen.fill(bg_color)

        mouse = pg.mouse.get_pos()
        b1.draw(screen, True)
        b2.draw(screen, True)
        b3.draw(screen, True)
        b4.draw(screen, True)
        b5.draw(screen, True)

        for i in pop.networks:
            for j in i.genome.nodes:
                gfxdraw.aacircle(screen, round(j.x * 700 + 10), round(j.y * 60 + 90), 17, (0, 0, 0))
                gfxdraw.filled_circle(screen, round(j.x * 700 + 10), round(j.y * 60 + 90), 17, (0, 0, 200))
                font = pg.font.SysFont('comicsans', 20)
                text = font.render(str(j.innovation_number), 1, (0, 0, 0))
                screen.blit(text,
                            ((j.x * 700 + 5),
                             j.y * 60 + 85))

            for j in i.genome.connections:
                color = (0, 0, 0) if not j.is_enabled else (0, 150, 0)
                if j.is_enabled:
                    pg.draw.line(color=color, width=3, start_pos=(j.from_node.x * 700 + 27, j.from_node.y * 60 + 90),
                                 end_pos=(j.to_node.x * 700 - 8, j.to_node.y * 60 + 90), surface=screen)
        pg.display.update()
        pg.time.delay(20)

    pg.quit()
    sys.exit()


if __name__ == '__main__':
    main()
