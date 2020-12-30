import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
from math import dist
from subprocess import Popen, PIPE
import pygame
from pygame.locals import *
from networkx.drawing.nx_pydot import graphviz_layout

CMAKE_DIR = "cmake-build-release/"
EXEC_NAME = "circles-hierarchy-core"

pygame.init()
pygame.display.set_caption('Circles Hierarchy')
WIDTH = int(pygame.display.Info().current_w * 0.7)
HEIGHT = int(pygame.display.Info().current_h * 0.7)
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def get_circles():
    font = pygame.font.Font(None, 40)
    text = font.render('Solve!', True, "black", "gray")
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


def get_tree(circles):
    print(os.popen("cmake -S . -B " + CMAKE_DIR).read())
    print(os.popen("make -C " + CMAKE_DIR).read())
    plain_tree = Popen(CMAKE_DIR + EXEC_NAME, stdin=PIPE, stdout=PIPE).communicate(raw_data(circles).encode())[
        0].decode()
    g = nx.Graph()
    for i in range(len(circles)):
        g.add_node(i)
    for line in plain_tree.split('\n')[:-1]:
        edge = list(map(int, line.split()))
        g.add_edge(edge[0], edge[1])
    return g


def color_circles(circles, colors):
    screen.fill("white")
    order_of_painting = [i for i in range(len(circles))]
    for i in order_of_painting:
        pygame.draw.circle(screen, colors[i], circles[i][0], circles[i][1])
    pygame.display.update()


circles = get_circles()
circles.sort(key=lambda circle: circle[1], reverse=True)
g = get_tree(circles)
colors = [tuple(np.random.choice(range(256), size=3)) for _ in range(len(circles))]
color_circles(circles, colors)
colors = [(0, 0, 0)] + colors
pos = graphviz_layout(g, "dot")
nx.draw_networkx_nodes(g, pos, node_color=[(color[0] / 256, color[1] / 256, color[2] / 256) for color in colors])
nx.draw_networkx_edges(g, pos)
plt.show()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
