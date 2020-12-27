from math import dist
from subprocess import Popen
import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Circles Hierarchy')
WIDTH = int(pygame.display.Info().current_w * 0.7)
HEIGHT = int(pygame.display.Info().current_h * 0.7)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 40)


def get_circles():
    text = font.render('Solve!', True, "black", "white")
    text_rect = text.get_rect()
    text_rect.bottom = HEIGHT
    text_rect.centerx = WIDTH // 2
    circles = []
    cur_center = ()
    solve_button = screen.blit(text, text_rect)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                if solve_button.collidepoint(event.pos):
                    return circles
                cur_center = event.pos
            elif event.type == MOUSEBUTTONUP:
                circles += [[cur_center] + [dist(cur_center, event.pos)]]
                cur_center = ()
        screen.fill("white")
        for circle in circles:
            pygame.draw.circle(screen, "black", circle[0], circle[1], 2)
        if cur_center:
            pygame.draw.circle(screen, "black", cur_center, dist(cur_center, pygame.mouse.get_pos()), 2)
        solve_button = screen.blit(text, text_rect)
        pygame.display.update()


circles = get_circles()
Popen()