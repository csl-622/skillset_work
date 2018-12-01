import random
import numpy as np
import matplotlib.pyplot as plt

def plot_graph(num, Nlist):
    UL = 0.03
    LL = 0.01
    R = np.array([100, 100, 100])[np.newaxis].T
    for j in range(0, 25):
        if num == 0:
            T = np.array([[random.uniform(0, LL), random.uniform(0, LL), random.uniform(0, LL)], [random.uniform(0, LL), random.uniform(0, LL), random.uniform(0, LL)], [random.uniform(0, LL), random.uniform(0, LL), random.uniform(0, LL)]])
        if num == 1:
            T = np.array([[random.uniform(LL, UL), random.uniform(LL, UL), random.uniform(LL, UL)], [random.uniform(LL, UL), random.uniform(LL, UL), random.uniform(LL, UL)], [random.uniform(LL, UL), random.uniform(LL, UL), random.uniform(LL, UL)]])
        sum = 0
        Kc_infinity_list = []
        n1_list = []
        n2_list = []
        Kc_infinity_max = 0
        n1_max = 0
        n2_max = 0
        for i in range(0, 5151):
            NT = Nlist[i] * T
            w, v = np.linalg.eig(NT)
            if abs(max(w, key=abs)) >= 1:
                sum += 1
            else:
                temp = np.linalg.inv(np.identity(3) - NT) * Nlist[i] * R
                Kc_infinity_matrix = np.dot(temp, R)
                Kc_infinity = float(np.sum(Kc_infinity_matrix,axis=0))
                Kc_infinity_list.append(Kc_infinity)
                n1_list.append(Nlist[i][0][0])
                n2_list.append(Nlist[i][1][1])
                if Kc_infinity_max < Kc_infinity:
                    Kc_infinity_max = Kc_infinity
                    n1_max = Nlist[i][0][0]
                    n2_max = Nlist[i][1][1]
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(n1_list, n2_list, Kc_infinity_list, c='b', marker='o')
        ax.set_xlabel('n1')
        ax.set_ylabel('n2')
        ax.set_zlabel('Kc_infinity')
        label = '(%d, %d, %d)' % (n1_max, n2_max, Kc_infinity_max)
        ax.text(n1_max, n2_max, Kc_infinity_max, label, None)
        if num == 0:
            plt.savefig("./RowLessThanOne/" + str(j + 1) + ".png")
        if num == 1:
            plt.savefig("./RowNotLessThanOne/" + str(j + 1) + ".png")
        plt.clf()
        plt.close()

def main():
    Nlist = []
    for i in range(0, 101):
        for j in range(0, 101 - i):
            tempN = np.array([[i, 0, 0], [0, j, 0], [0, 0, 100 - i - j]])
            Nlist.append(tempN)
    plot_graph(0, Nlist)
    plot_graph(1, Nlist)
main()
