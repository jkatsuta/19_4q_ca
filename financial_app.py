#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from alifebook_lib.visualizers import ArrayVisualizer


def init_state(init_type, space_size):
    if init_type == 1:
        # 中央の１ピクセルのみ１、後は０
        state = np.zeros(space_size, dtype=np.int8)
        state[space_size // 2] = 1
    elif init_type == 2:
        np.random.seed(0)
        state = np.random.randint(2, size=space_size)
    next_state = np.empty(space_size, dtype=np.int8)
    return state, next_state


def main(space_size=600, init_type=1, step_size=1000):
    state, next_state = init_state(init_type, space_size)
    visualizer = ArrayVisualizer()

    for _ in range(step_size):
        for i in range(space_size):
            l = state[i - 1]
            r = state[(i+1) % space_size]

            if (l + r) == 1:
                next_state[i] = 1
            else:
                next_state[i] = 0
        state = next_state.copy()
        visualizer.update(1 - state)

    input('enter to finish')


if __name__ == '__main__':
    space_size = 200
    step_size = 1000
    init_type = 2

    main(space_size, init_type, step_size)
