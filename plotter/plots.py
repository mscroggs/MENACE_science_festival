import matplotlib.pylab as plt

def line_plot(data, filename):
    ys = [0]
    for a in data:
        if a[1] == "0":
            ys.append(ys[-1]+3)
        if a[1] == "1":
            ys.append(ys[-1]+1)
        if a[1] == "2":
            ys.append(ys[-1]-1)
    plt.plot(ys, "ko")
    plt.xlabel("Games played")
    plt.ylabel("Change in number of beads in first box")
    plt.savefig(filename)
    plt.clf()
