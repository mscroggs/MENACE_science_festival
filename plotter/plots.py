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
        if a[1] == "0":
            y += 3
        if a[1] == "1":
            y += 1
        if a[1] == "2":
            y -= 1

        xa.append(i+1)
        ya.append(y)
        if a[0][0] == "0":
            x0.append(i+1)
            y0.append(y)
        if a[0][0] == "1":
            x1.append(i+1)
            y1.append(y)
        if a[0][0] == "2":
            x2.append(i+1)
            y2.append(y)


    gs = gridspec.GridSpec(1,5)


    fig = plt.figure(figsize=(15,5))
    plt.gcf().subplots_adjust(top=0.93)



    p1 = plt.subplot(gs[:,:-1])

    cornercol = "#0000ff"
    edgecol = "#ff0000"
    centercol = "#006400"

    op = {"mec":"k","mew":0.6}
    p1.plot(xa, ya, "k-")
    p1.plot(x0, y0, "o", c=cornercol, **op)
    p1.plot(x1, y1, "o", c=edgecol, **op)
    p1.plot(x2, y2, "o", c=centercol, **op)


    if len(data)==0:
        xlim = (0,50)
        ylim = (-25,25)
    else:
        xlim = (0,50*(1+(i+1)//50))
        ylim = (-25,25*(1+max(0,max(ya))//25))
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xticks(range(0,xlim[1]+1,10), **kwargs())
    plt.yticks(range(-20,ylim[1]+1,10), **kwargs())

    plt.xlabel("Games played", **kwargs())
    plt.ylabel("Change in number of beads in first box\n(3"+u"\u00D7"+"WINS + 1"+u"\u00D7"+"DRAWS - 1"+u"\u00D7"+"LOSSES)", **kwargs())


    p2 = plt.subplot(gs[:,-1])
    p2.plot([10,10],[0,30],"k-")
    p2.plot([20,20],[0,30],"k-")
    p2.plot([0,30],[10,10],"k-")
    p2.plot([0,30],[20,20],"k-")

    op = {"edgecolor":"k"}

    for pos in [(5,5),(25,25),(5,25),(25,5)]:
        circ=plt.Circle(pos, radius=4, facecolor=cornercol, fill=True, **op)
        p2.add_patch(circ)
    for pos in [(15,5),(15,25),(5,15),(25,15)]:
        circ=plt.Circle(pos, radius=4, facecolor=edgecol, fill=True, **op)
        p2.add_patch(circ)
    circ=plt.Circle((15,15), radius=4, facecolor=centercol, fill=True, **op)
    p2.add_patch(circ)

    plt.annotate("MENACE's first move", **kwargs(), xy=(15,32),ha="center")
    plt.axis('equal')
    plt.axis("off")

    plt.savefig(filename, dpi=120)
    plt.clf()
    plt.close(fig)
