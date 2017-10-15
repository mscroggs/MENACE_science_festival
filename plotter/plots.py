import matplotlib.pylab as plt

def line_plot(data, filename):
    y = 0
    xa,ya = [],[]
    x0,y0 = [],[]
    x1,y1 = [],[]
    x2,y2 = [],[]
    for i,a in enumerate(data):
        if a[1] == "0":
            y += 3
        if a[1] == "1":
            y += 1
        if a[1] == "2":
            y -= 1

        xa.append(i)
        ya.append(y)
        if a[0][0] == "0":
            x0.append(i)
            y0.append(y)
        if a[0][0] == "1":
            x1.append(i)
            y1.append(y)
        if a[0][0] == "2":
            x2.append(i)
            y2.append(y)

    plt.plot(xa, ya, "k-")
    plt.plot(x0, y0, "o", c="#045ba4")
    plt.plot(x1, y1, "o", c="#fd8ba1")
    plt.plot(x2, y2, "o", c="#0f9137")

    xlim = (0,50*(1+i//50))
    ylim = (-25,25*(1+max(ya)//25))
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xticks(range(0,xlim[1],10))
    plt.yticks(range(-20,ylim[1]+1,10))

    plt.xlabel("Games played")
    plt.ylabel("Change in number of beads in first box")
    plt.savefig(filename)
    plt.clf()
