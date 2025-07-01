import numpy as np

def logic():
    from 机器学习.perceptron import pcn

    a = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]])
    b = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]])

    p = pcn.pcn(a[:, 0:2], a[:, 2:])
    p.pcntrain(a[:, 0:2], a[:, 2:], 0.25, 10)

    q = pcn.pcn(b[:, 0:2], b[:, 2:])
    q.pcntrain(b[:, 0:2], b[:, 2:], 0.25, 10)

