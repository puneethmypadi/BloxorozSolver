# -*- coding: utf-8 -*-
# @Time    : 21/11/2020
# @Author  : Puneeth Mypadi
# @Email   : puneeth.mypadi@gmail.com
# @File    : bloxorozsolver.py

# import statements
import numpy as np
import sys
from ast import literal_eval
from queue import SimpleQueue
import copy

# 2-D array denoting the play arena
canvas = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
          [0, 0, 0, 0, 0, 0, 1, 1, 1, 0], ]


# DiePosition denotes the position of the playing piece.
class DiePosition:

    # Contains 2 points with 2D coordinate systems. Both the points coincide when the playing piece stands upright
    def __init__(self, a, b):
        self.a = a
        self.b = b

    # Having eq method for easy equality comparisons

    def __eq__(self, other):
        return (self.a == other.a).all() and (self.b == other.b).all()

    # hashgen for the class to be used for indexing in a set/dictionary
    def __hash__(self):
        return hash((self.a[0], self.a[1], self.b[0], self.b[1]))

    # gives next positions which can be occupied by the play-piece in the next iteration
    def next_positions(self):
        return np.array([self.up(), self.down(), self.left(), self.right()])

    # Die position for Upward movement of the die
    def up(self):
        if (self.a == self.b).all():
            return DiePosition(np.add(self.a, [-2, 0]), np.add(self.b, [-1, 0]))
        elif self.a[0] == self.b[0]:
            return DiePosition(np.add(self.a, [-1, 0]), np.add(self.b, [-1, 0]))
        elif self.a[1] == self.b[1]:
            return DiePosition(np.add(self.a, [-1, 0]), np.add(self.b, [-2, 0]))

    # Die position for downward movement of the die
    def down(self):
        if (self.a == self.b).all():
            return DiePosition(np.add(self.a, [1, 0]), np.add(self.b, [2, 0]))
        elif self.a[0] == self.b[0]:
            return DiePosition(np.add(self.a, [1, 0]), np.add(self.b, [1, 0]))
        elif self.a[1] == self.b[1]:
            return DiePosition(np.add(self.a, [2, 0]), np.add(self.b, [1, 0]))

    # Die position for leftward movement of the die
    def left(self):
        if (self.a == self.b).all():
            return DiePosition(np.add(self.a, [0, -2]), np.add(self.b, [0, -1]))
        elif self.a[0] == self.b[0]:
            return DiePosition(np.add(self.a, [0, -1]), np.add(self.b, [0, -2]))
        elif self.a[1] == self.b[1]:
            return DiePosition(np.add(self.a, [0, -1]), np.add(self.b, [0, -1]))

    # Die position for Rightward movement of the die
    def right(self):
        if (self.a == self.b).all():
            return DiePosition(np.add(self.a, [0, 1]), np.add(self.b, [0, 2]))
        elif self.a[0] == self.b[0]:
            return DiePosition(np.add(self.a, [0, 2]), np.add(self.b, [0, 1]))
        elif self.a[1] == self.b[1]:
            return DiePosition(np.add(self.a, [0, 1]), np.add(self.b, [0, 1]))

    # Printable string
    def __str__(self):
        return "a={} b={}".format(self.a, self.b)


# Checks if the state falls out of the boundary/positive quadrant or the state of the DiePosition is illegal
def falls_out_of_boundary(state):
    # if the indexes aren't in the first quadrant
    if state.a[0] < 0 or state.a[1] < 0 or state.b[0] < 0 or state.b[1] < 0:
        return True
    # if the coordinates overshoot the canvas' dimensions
    if len(canvas) <= state.a[0] or len(canvas) <= state.b[0] or len(canvas[0]) <= state.a[1] or len(canvas[0]) <= \
            state.b[1]:
        return True
    # if the die coordinates aren't side by side
    if np.linalg.norm(state.a - state.b, 1) > 1:
        return True
    # if the coordinates correspond to 0 entries in the canvasS
    if canvas[state.a[0]][state.a[1]] == 0 or canvas[state.b[0]][state.b[1]] == 0:
        return True
    return False


# Removes all impossible states in the iterable
def remove_impossible_states(states):
    i = 0
    kept_states = []
    for state in states:
        if not falls_out_of_boundary(state):
            kept_states = kept_states.append(state)
        i = i + 1
    return np.array(kept_states)


# Check if the current state is goal
def is_goal(state):
    # check if both the coordinates of the die correspond to the 9 of the canvas
    return canvas[state.a[0]][state.a[1]] == 9 and canvas[state.b[0]][state.b[1]] == 9


# Returns numpy array representation of commandline argument
def return_np_array_from_str_rep(representation):
    return np.array(literal_eval(representation))


# resolves commandline arguments and gets starting positions, if arguments are illegal, it falls back to default
# starting position of [1,1]
def get_start_pos():
    default_start = DiePosition(np.array([1, 1]), np.array([1, 1]))
    if len(sys.argv) == 1:
        return default_start
    if len(sys.argv) == 2 and not falls_out_of_boundary(
            DiePosition(return_np_array_from_str_rep(sys.argv[1]), return_np_array_from_str_rep(sys.argv[1]))):
        return DiePosition(return_np_array_from_str_rep(sys.argv[1]), return_np_array_from_str_rep(sys.argv[1]));
    if len(sys.argv) == 3 and not falls_out_of_boundary(
            DiePosition(return_np_array_from_str_rep(sys.argv[1]), return_np_array_from_str_rep(sys.argv[2]))):
        default_start = DiePosition(return_np_array_from_str_rep(sys.argv[1]),
                                    return_np_array_from_str_rep(sys.argv[2]))
        if (default_start.a > default_start.b).any():
            default_start.a, default_start.b = default_start.b, default_start.a
    return default_start


'''performs depth limited search on the node
    append current node to the path stack
    if depth is greater than 0 and there are no children, return with a no children flag along with none and pop the  stack,
    else find next legal steps, and do a recursive with one less than the given depth on each child
    if there is a node which is a goal return it along with the path stack
    '''


def dls(node, depth, stack):
    # if max depth is reached, check if the current node is the goal and return the path and the node, else return
    # with a None value
    if depth == 0:
        if is_goal(node):
            return node, True, stack
        else:
            return None, True, stack
    elif depth > 0:
        any_remaining = False
        children = remove_impossible_states(node.next_positions())
        for child in children:
            stack.append(child)
            found, remaining, stack = dls(child, depth - 1, stack)
            if found is not None:
                return found, True, stack
            if remaining:
                stack.pop();
                any_remaining = True

        return None, any_remaining, stack


'''Perform dls iteratively over a maximum of 1000 d'''


def iterative_deepening_dfs(root):
    for depth in range(0, 1000):
        print(depth)
        found, remaining, stack = dls(root, depth, [root])
        if found is not None:
            return found, True, stack
        elif not remaining:
            return None, False, stack


# Driver for the code

# Get the starting position from cmdline
start_pos = get_start_pos()

# print the inferred starting position
print('starting position is {}'.format(start_pos))

# perform iidfs
locations, remaining, steps = iterative_deepening_dfs(start_pos)

# print each step in Die's way
for item in steps:
    array_copy = copy.deepcopy(canvas)
    array_copy[item.a[0]][item.a[1]] = 'X'
    array_copy[item.b[0]][item.b[1]] = 'X'
    for row in array_copy:
        print(row)
    print('\n\n')
