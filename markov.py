import os

import bidict
import numpy as np

import nltk

class Start(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __repr__(self):
        return "Start()"


class End(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __repr__(self):
        return "End()"


class ObjectIndexedArray(object):

    def __init__(self, row_indices, column_indices, dtype=np.float_):
        self._row_indices_dict = bidict.bidict()
        for i, object_index in enumerate(set(row_indices)):
            self._row_indices_dict[object_index] = i

        self._column_indices_dict = bidict.bidict()
        for j, object_index in enumerate(set(column_indices)):
            self._column_indices_dict[object_index] = j

        self._height = len(self._row_indices_dict)
        self._width = len(self._column_indices_dict)
        self._array = np.zeros((self._height, self._width), dtype=dtype)

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def debug(self):
        for i in range(0, self.height):
            print(self._row_indices_dict.inv[i])
        for j in range(0, self.width):
            print(self._column_indices_dict.inv[j])
        print(self._array)

    def _translate_indices(self, index):
        row_index_object, column_index_object = index
        i = self._row_indices_dict[row_index_object]
        j = self._column_indices_dict[column_index_object]
        return (i, j)

    def __matmul__(self, other):
        return self._array @ other

    def __rmatmul__(self, other):
        return other @ self._array

    def __getitem__(self, index):
        i, j = self._translate_indices(index)
        return self._array[i, j]

    def __setitem__(self, index, value):
        i, j = self._translate_indices(index)
        self._array[i, j] = value

    def get_row_index(self, i):
        return self._row_indices_dict.inv[i]

    def get_column_index(self, j):
        return self._column_indices_dict.inv[j]

    def get_row_number(self, row_index):
        return self._row_indices_dict[row_index]

    def get_column_number(self, column_index):
        return self._column_indices_dict[column_index]

    def sum(self):
        return self._array.sum()

    def normalize(self):
        for i in range(0, self._array.shape[0]):
            vector_sum = self._array[i].sum()
            self._array[i] /= vector_sum


class MarkovChain(object):
    """ MarkovChain([[1, 2, 3, 2, 5], [2, 4, 5, 6, 6]])
    """

    def __init__(self, training_data, order=1):
        self.order = order
        self.transition_array = None
        self.__train(training_data, order)

    def __train(self, training_data, order):
        column_indices = set()
        row_indices = set()

        tagged_data = []
        for sample in training_data:
            sample = [Start()] * order + sample + [End()]
            tagged_data.append(sample)
            window_start = 0
            window_end = order
            while window_end < len(sample):
                row_index = tuple(sample[window_start:window_end])
                row_indices.add(row_index)

                column_index = sample[window_end]
                column_indices.add(column_index)
                window_start += 1
                window_end += 1

        self.transition_array = ObjectIndexedArray(tuple(row_indices),
                                                   tuple(column_indices))

        for sample in tagged_data:
            window_start = 0
            window_end = order
            while window_end < len(sample):
                row_index = tuple(sample[window_start:window_end])
                column_index = sample[window_end]
                self.transition_array[row_index, column_index] = +1
                window_start += 1
                window_end += 1
        self.transition_array.normalize()

    def generate_sequence(self):
        sequence = [Start()] * self.order
        history = tuple(sequence)
        next_state = None

        while next_state is not End():
            next_state = self.__get_next(history)
            sequence.append(next_state)
            history = tuple(sequence[-self.order:])
        print(sequence)

    def __get_next(self, history):
        i = self.transition_array.get_row_number(history)
        state_vector = np.zeros((1, self.transition_array.height))
        state_vector[0, i] = 1
        distribution = state_vector @ self.transition_array._array
        j = np.random.choice(range(0, self.transition_array.width),
                p=distribution[0])
        return self.transition_array.get_column_index(j)

S = MarkovChain([[1, 1, 2, 1, 3, 3, 5, 6, 4, 1, 1, 4]], 2)
S.generate_sequence()

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
with open("pg11.txt") as fp:
    data = fp.read()
s = tokenizer.tokenize(data)
f = [x.replace('.', '').replace(',', '').replace('\n', ' ').lower().split(' ') for x in s]

S = MarkovChain(f, 2)
S.generate_sequence()
