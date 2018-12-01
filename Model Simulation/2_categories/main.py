import random
import numpy as np
import matplotlib.pyplot as plt

def plot_graph(num):
    UL = 0.02
    LL = 0.01
    R = np.array([100, 100])[np.newaxis].T
    for j in range(0, 25):
        if num == 0:
            T = np.array([[random.uniform(0, LL), random.uniform(0, LL)], [random.uniform(0, LL), random.uniform(0, LL)]])
        if num == 1:
            T = np.array([[random.uniform(LL, UL), random.uniform(LL, UL)], [random.uniform(LL, UL), random.uniform(LL, UL)]])
        sum = 0
        Kc_infinity_list = []
        n1_list = []
        Kc_infinity_max = 0
        n1_max = 0
        for i in range(0, 101):
            N = np.array([[i, 0], [0, 100 - i]])
            NT = N * T
            w, v = np.linalg.eig(NT)
            if abs(max(w, key=abs)) >= 1:
                sum += 1
            else:
                temp = np.linalg.inv(np.identity(2) - NT) * N * R
                Kc_infinity_matrix = np.dot(temp, R)
                Kc_infinity = float(np.sum(Kc_infinity_matrix,axis=0))
                Kc_infinity_list.append(Kc_infinity)
                n1_list.append(N[0][0])
                if Kc_infinity_max < Kc_infinity:
                    Kc_infinity_max = Kc_infinity
                    n1_max = N[0][0]
        plt.plot(n1_list, Kc_infinity_list)
        plt.xlabel('n1')
        plt.ylabel('Kc_infinity')
        label = '(%d, %d)' % (n1_max, Kc_infinity_max)
        plt.text(n1_max, Kc_infinity_max, label, None)
        if num == 0:
            plt.savefig("./RowLessThanOne/" + str(j + 1) + ".png")
        if num == 1:
            plt.savefig("./RowNotLessThanOne/" + str(j + 1) + ".png")
        plt.clf()
        plt.close()

plot_graph(0)
plot_graph(1)
