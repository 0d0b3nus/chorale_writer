import os

import bidict
import numpy as np

class MarkovChain(object):

    def __init__(self, training_data, order=1):
        self.history_tuples = bidict.bidict()
        self.states = bidict.bidict()
        self.transition_matrix = None
        self.__train(training_data, order)

    def __train(self, training_data, order):
        width = self.__get_width(training_data)
        height = self.__get_height(training_data, order)
        frequency_matrix = np.matrix([[0] * width] * height, dtype='uint64')

        num_states = 0
        num_histories = 0
        window_start = 0
        window_end = order + 1
        while window_end < len(training_data):
            history = tuple(training_data[window_start:window_end])
            next_state = training_data[window_end]
            # Find which row corresponds to history
            if history not in self.history_tuples.inv:
                self.history_tuples[num_histories] = history
                i = num_histories
                num_histories += 1
            else:
                i = self.history_tuples.inv[history]

            # Find which column corresponds to next state
            if next_state not in self.states.inv:
                self.states[num_states] = next_state
                j = num_states
                num_states += 1
            else:
                j = self.states.inv[next_state]

            frequency_matrix[i, j] += 1
            window_start += 1
            window_end += 1
        transitions = frequency_matrix.sum()
        self.transition_matrix = np.matrix(frequency_matrix,
                                           dtype='float64') / transitions
        print(self.transition_matrix)

    def __get_width(self, training_data):
        states = set()

        for state in training_data:
            states.add(state)
        return len(states)

    def __get_height(self, training_data, order):
        histories = set()

        window_start = 0
        window_end = order + 1
        while window_end < len(training_data):
            history = tuple(training_data[window_start:window_end])
            histories.add(history)
            window_start += 1
            window_end += 1
        return len(histories)

    def generate_sequence(self, start_state=None, end_state=None, num_states=20):
        sequence = []
        history = self.__generate_starting_state()
        sequence += list(history)
        states = len(history)

        if end_state is not None:
            new_state = None
            while new_state != end_state:
                tm = self.__transition_matrix
                current_dist = np.matrix([0] * tm.shape[0])
                current_dist[self.history_tuples.inv[history]] = 1
        pass

    def __generate_starting_state(self, start_state=None):
        starting_dist = np.matrix([0] * self.transition_matrix.shape[0])
        if start_state is not None:
            starting_states = [history in self.history_tuples.values()
                               if history[0] == start_state]
        else:
            starting_states = self.history_tuples.values()

S = MarkovChain([1, 2, 3, 4, 5, 4, 5, 3, 2, 1, 2, 3], 3)
