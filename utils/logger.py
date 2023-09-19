"""
A simple torch style logger
(C) Wei YANG 2017
"""
# pylint: disable=W1514
from __future__ import absolute_import
import matplotlib.pyplot as plt
import numpy as np

__all__ = ['Logger', 'LoggerMonitor', 'savefig']


def savefig(fname, dpi=None):
    """Save the figure"""
    dpi = 150 if dpi is None else dpi
    plt.savefig(fname, dpi=dpi)


def plot_overlap(logger, names=None):
    """Plot the overlap"""
    names = logger.names if names is None else names
    numbers = logger.numbers
    for _, name in enumerate(names):
        x = np.arange(len(numbers[name]))
        plt.plot(x, np.asarray(numbers[name]))
    return [logger.title + '(' + name + ')' for name in names]


class Logger:
    """Save training process to log file with simple plot function."""

    def __init__(self, fpath, title=None, resume=False):
        self.file = None
        self.resume = resume
        self.title = '' if title is None else title
        if fpath is not None:
            if resume:
                self.file = open(fpath, 'r')
                name = self.file.readline()
                self.names = name.rstrip().split('\t')
                self.numbers = {}
                for _, name in enumerate(self.names):
                    self.numbers[name] = []

                for numbers in self.file:
                    numbers = numbers.rstrip().split('\t')
                    for i, ele_numbers in enumerate(numbers):
                        self.numbers[self.names[i]].append(ele_numbers)
                self.file.close()
                self.file = open(fpath, 'a')
            else:
                self.file = open(fpath, 'w')

    def set_names(self, names):
        """Set the names"""
        if self.resume:
            pass
        # initialize numbers as empty list
        self.numbers = {}
        self.names = names
        for _, name in enumerate(self.names):
            self.file.write(name)
            self.file.write('\t')
            self.numbers[name] = []
        self.file.write('\n')
        self.file.flush()

    def append(self, numbers):
        """ append"""
        assert len(self.names) == len(numbers), 'Numbers do not match names'
        for index, num in enumerate(numbers):
            # self.file.write("{0:.6f}".format(num))
            self.file.write(f"{num}")
            self.file.write('\t')
            self.numbers[self.names[index]].append(num)
        self.file.write('\n')
        self.file.flush()

    def plot(self, names=None):
        """Plot"""
        names = self.names if names is None else names
        numbers = self.numbers
        for _, name in enumerate(names):
            x = np.arange(len(numbers[name]))
            plt.plot(x, np.asarray(numbers[name]))
        plt.legend([self.title + '(' + name + ')' for name in names])
        plt.grid(True)

    def close(self):
        """Close"""
        if self.file is not None:
            self.file.close()


class LoggerMonitor:
    """Load and visualize multiple logs."""

    def __init__(self, _paths):
        """paths is a distionary with {name:filepath} pair"""
        self.loggers = []
        for title, path in _paths.items():
            logger = Logger(path, title=title, resume=True)
            self.loggers.append(logger)

    def plot(self, names=None):
        """Plot"""
        plt.figure()
        plt.subplot(121)
        legend_text = []
        for logger in self.loggers:
            legend_text += plot_overlap(logger, names)
        plt.legend(legend_text, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.grid(True)


if __name__ == '__main__':
    # # Example
    # logger = Logger('test.txt')
    # logger.set_names(['Train loss', 'Valid loss','Test loss'])

    # length = 100
    # t = np.arange(length)
    # train_loss = np.exp(-t / 10.0) + np.random.rand(length) * 0.1
    # valid_loss = np.exp(-t / 10.0) + np.random.rand(length) * 0.1
    # test_loss = np.exp(-t / 10.0) + np.random.rand(length) * 0.1

    # for i in range(0, length):
    #     logger.append([train_loss[i], valid_loss[i], test_loss[i]])
    # logger.plot()

    # Example: logger monitor
    paths = {
        'resadvnet20': '/home/wyang/code/pytorch-classification/checkpoint/cifar10/resadvnet20/log.txt',
        'resadvnet32': '/home/wyang/code/pytorch-classification/checkpoint/cifar10/resadvnet32/log.txt',
        'resadvnet44': '/home/wyang/code/pytorch-classification/checkpoint/cifar10/resadvnet44/log.txt',
    }

    field = ['Valid Acc.']

    monitor = LoggerMonitor(paths)
    monitor.plot(names=field)
    savefig('test.eps')
