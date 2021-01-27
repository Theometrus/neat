import random
import sys

import pygame as pg
from pygame import gfxdraw

from classes.Helpers.XORFitnessEvaluator import XORFitnessEvaluator
from classes.Puppeteers.Population import Population
from config.settings import *


def main():
    xor = XORFitnessEvaluator()
    pop = Population(xor)
    gen = 0

    timeout = 500
    xor_inputs = [[1, 1], [0, 0], [1, 0], [0, 1]]
    while timeout > 0:
        xor = XORFitnessEvaluator()
        outs = {}
        pop.fitness_evaluator = xor
        random.shuffle(xor_inputs)
        inputs = [item for sublist in xor_inputs for item in sublist]
        ctr = 0
        for i in range(4):
            pop.propagate([inputs[ctr], inputs[ctr + 1]])
            ctr += 2

        for i in pop.networks:
            outs[i] = i.outputs

            xor.calculate(i, outs, inputs)

        pop.evolve()
        gen += 1
        print("GENERATION " + str(gen))
        print(inputs)
        print('----------------')
        total = 0.0
        for s in pop.species:
            print(str(len(s.members)))
            print("************")
        # mean_score /= 1000
        for n, v in xor.networks.items():
            total += v
        total /= len(xor.networks)
        print("MEAN SCORE: " + str(total))
        print("GENERATION " + str(gen))
        print("================================")

        if total >= 14.0:
            break
        # time.sleep(1)
        timeout -= 1

    xor = XORFitnessEvaluator()
    outs = {}
    pop.fitness_evaluator = xor
    pop.propagate([0, 1])
    pop.propagate([1, 1])
    pop.propagate([1, 0])
    pop.propagate([0, 0])
    for i in pop.networks:
        outs[i] = i.outputs
        xor.calculate(i, outs, [1, 0, 0, 0, 1, 1, 0, 1])
    avg_0 = 0.0
    avg_1 = 0.0
    avg_2 = 0.0
    avg_3 = 0.0
    nets = sorted(pop.networks, key=lambda x: x.fitness)

    avg_nodes = 0
    avg_conns = 0
    best_fitness = 0.0
    best_fitness_node = None

    for i in nets:
        avg_nodes += len(i.genome.nodes)
        avg_conns += len(i.genome.connections)
        avg_0 += i.outputs[0]
        avg_1 += i.outputs[1]
        avg_2 += i.outputs[2]
        avg_3 += i.outputs[3]
        if i.fitness > best_fitness:
            best_fitness = i.fitness
            best_fitness_node = i
    avg_0 /= len(pop.networks)
    avg_1 /= len(pop.networks)
    avg_2 /= len(pop.networks)
    avg_3 /= len(pop.networks)
    avg_nodes /= 150
    avg_conns /= 150
    print([avg_0, avg_1, avg_2, avg_3])
    print("Average nodes: {}, average conns: {}".format(avg_nodes, avg_conns))
    print(len(best_fitness_node.genome.nodes))

    # pg.init()
    # pg.display.set_caption("NEAT")
    # screen = pg.display.set_mode(RESOLUTION)
    # bg_color = BG_COLOR
    #
    # running = True
    # while running:
    #     for ev in pg.event.get():
    #         if ev.type == pg.QUIT:
    #             running = False
    #
    #     screen.fill(bg_color)
    #
    #     for j in best_fitness_node.genome.connections:
    #         color = (0, 0, 0) if not j.is_enabled else (0, 150, 0)
    #         if j.is_enabled:
    #             pg.draw.line(color=color, width=3, start_pos=(j.from_node.x * 700 + 27, j.from_node.y * 250 + 90),
    #                          end_pos=(j.to_node.x * 700 - 8, j.to_node.y * 250 + 90), surface=screen)
    #
    #     for j in best_fitness_node.genome.nodes:
    #         gfxdraw.aacircle(screen, round(j.x * 700 + 10), round(j.y * 250 + 90), 17, (0, 0, 0))
    #         gfxdraw.filled_circle(screen, round(j.x * 700 + 10), round(j.y * 250 + 90), 17, (0, 0, 200))
    #         font = pg.font.SysFont('comicsans', 20)
    #         text = font.render(str(j.innovation_number), 1, (0, 0, 0))
    #         screen.blit(text,
    #                     ((j.x * 700 + 5),
    #                      j.y * 250 + 85))
    #
    #     pg.display.update()
    #     pg.time.delay(20)
    #
    # pg.quit()
    # sys.exit()

if __name__ == '__main__':
    main()
