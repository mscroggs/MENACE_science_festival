import matplotlib.pylab as plt
from matplotlib import gridspec

def kwargs():
    return {"fontname":"Latin Modern Mono","fontsize":15}

def line_plot(data, filename):
    y = 0
    xa,ya = [0],[0]
    x0,y0 = [],[]
    x1,y1 = [],[]
    x2,y2 = [],[]
    for i,a in enumerate(data):
        if a == "0":
            y += 3
        if a == "1":
            y += 1
        if a == "2":
            y -= 1

        xa.append(i+1)
        ya.append(y)

    fig = plt.figure(figsize=(10,5))

    cornercol = "#FFA366"
    op = {"mec":"k","mew":0.6}
    plt.plot(xa, ya, "k-")
    plt.plot(xa, ya, "o", c=cornercol, **op)


    if len(data)==0:
        xlim = (0,50)
        ylim = (-36,25)
    else:
        xlim = (0,50*(1+(i+1)//50))
        ylim = (-36,25*(1+max(0,max(ya))//25))
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xticks(range(0,xlim[1]+1,10), **kwargs())
    plt.yticks(range(-30,ylim[1]+1,10), **kwargs())

    plt.xlabel("Games played", **kwargs())
    plt.ylabel("Change in number of beads in first box\n(3"+u"\u00D7"+"WINS + 1"+u"\u00D7"+"DRAWS - 1"+u"\u00D7"+"LOSSES)", **kwargs())


    plt.savefig(filename, dpi=120)
    plt.clf()
    plt.close(fig)
