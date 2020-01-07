#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer


def init_state(init_type, height, width):
    if init_type == 1:
        # 中央の１ピクセルのみ１、後は０
        state = np.zeros((height, width), dtype=np.int8)
        state[height // 2, width // 2] = 1
    elif init_type == 2:
        np.random.seed(0)
        state = np.random.randint(2, size=(height, width))
    return state


def _get_circular_matrix(state, height, width, weights):
    offset = len(weights) - 1
    height2 = height + 2 * offset
    width2 = width + 2 * offset

    circ_state = np.zeros((height2, width2), dtype=np.int8)
    circ_state[offset:-offset, offset:-offset] = state
    circ_state[:offset, offset:-offset] = state[-offset:]
    circ_state[-offset:, offset:-offset] = state[:offset]
    circ_state[offset:-offset, :offset] = state[:, -offset:]
    circ_state[offset:-offset, -offset:] = state[:, :offset]
    return circ_state, offset


def update_state(state, weights):
    height, width = state.shape
    next_state = state.copy()
    circ_state, offset = _get_circular_matrix(state, height, width, weights)
    for i in range(height):
        for j in range(width):
            neighbor_cell_sum = 0
            sum_core = 0
            for k in range(len(weights)):
                h1 = i - k + offset
                h2 = i + k + 1 + offset
                w1 = j - k + offset
                w2 = j + k + 1 + offset
                sum_all = np.sum(circ_state[h1:h2, w1:w2])
                neighbor_cell_sum += weights[k] * (sum_all - sum_core)
                sum_core = sum_all

            if neighbor_cell_sum > 0:
                next_state[i, j] = 1
            elif neighbor_cell_sum < 0:
                next_state[i, j] = 0
            else:
                pass
    return next_state


def main(weights, height, width, init_type=1, step_size=100):
    state = init_state(init_type, height, width)
    visualizer = MatrixVisualizer()
    for i in range(step_size):
        print(i)
        state = update_state(state, weights)
        visualizer.update(1 - state)
    input('enter to finish')


if __name__ == '__main__':
    weights_list = [[1., 1., -0.4, -0.4],
                    [1., 1., -0.3, -0.3],
                    [1., 1., -0.2, -0.2],
                    [1., 1., -0.3, -0.1]]
    height, width = 100, 100
    step_size = 10
    init_type = 2

    for weights in weights_list:
        main(weights, height, width, init_type, step_size)
