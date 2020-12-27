import networkx as nx
import matplotlib.pyplot as plt
import os
from math import dist
from subprocess import Popen, PIPE
import pygame
from pygame.locals import *
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

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
                circles += [[cur_center] + [int(dist(cur_center, event.pos))]]
                cur_center = ()
        screen.fill("white")
        for circle in circles:
            pygame.draw.circle(screen, "black", circle[0], circle[1], 2)
        if cur_center:
            pygame.draw.circle(screen, "black", cur_center, int(dist(cur_center, pygame.mouse.get_pos())), 2)
        solve_button = screen.blit(text, text_rect)
        pygame.display.update()


def raw_data(circles):
    raw_str = str(len(circles)) + '\n'
    for circle in circles:
        raw_str += str(circle[0][0]) + ' ' + str(circle[0][1]) + ' ' + str(circle[1]) + '\n'
    return raw_str


circles = get_circles()
CMAKE_DIR = "cmake-build-release/"
EXEC_NAME = "circles-hierarchy-core"
print(os.popen("cmake -S . -B " + CMAKE_DIR).read())
print(os.popen("make -C " + CMAKE_DIR).read())
plain_tree = Popen(CMAKE_DIR + EXEC_NAME, stdin=PIPE, stdout=PIPE).communicate(raw_data(circles).encode())[0].decode()
g = nx.Graph()
for line in plain_tree.split('\n')[:-1]:
    edge = line.split()
    g.add_edge(edge[0], edge[1])
nx.draw(g, graphviz_layout(g, "dot"))
plt.show()
