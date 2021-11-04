import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as matAnimate
from matplotlib import style
global scope
scope = [[0], [0]]
matplotlib.use("TkAgg")
style.use("ggplot")

app = tk.Tk()
blankspace = ttk.Label(app)

settings = ttk.Menubutton(app, text="Settings")
settings.menu = tk.Menu(settings)
settings["menu"] = settings.menu
settings.menu.add_command(label="Specificy Range", command = lambda: specificyRange())
fig = Figure(figsize = (12, 12), dpi=85)
plot_1 = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, app)
canvas.draw()

blankspace.grid(row = 0, column = 0, columnspan = 4)
settings.grid(row = 0, column = 0, sticky = 'w')
canvas.get_tk_widget().grid(row = 3, column = 1) #this is the graph (where data will be plotted)
canvas._tkcanvas.grid(column = 1, sticky = 'w')

def fetchData(destination):
    x = []
    y = []
    initial_contents = None
    with open(destination) as destination_contents:
        initial_contents = destination_contents.read()
    for line in initial_contents.split("\n"):
        pair = line.split(',')
        if pair != ['']:
            x.append(int(pair[0]))
            y.append(int(pair[1]))
    return (x, y)

def updatePlot_1(i):
    global dataX, dataY
    plot_1.clear()
    plot_1.set_xlabel("Runs")
    plot_1.set_ylabel("Words")

    file = prompt_1.get()
    try:
        dataX, dataY = fetchData(file)[0], fetchData(file)[1]
        plot_1.scatter(dataX, dataY)
    except FileNotFoundError:
        pass

app.title("Graph App")
app.geometry("575x540")
animatePlot = matAnimate.FuncAnimation(fig, updatePlot_1, interval=500)
app.mainloop()
