import matplotlib.pyplot as plt

pts = []

def onclick(event):
    if event.xdata is None or event.ydata is None:
        return
    x = round(event.xdata, 2)
    y = round(event.ydata, 2)
    pts.append((x, y))
    ax.plot([x], [y], 'o')   # list-wrapped → always displays
    fig.canvas.draw()
    print(pts)

fig, ax = plt.subplots()

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xticks(range(0, 11))
ax.set_yticks(range(0, 11))
ax.grid(True)

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
