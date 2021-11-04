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
fig = Figure(figsize = (10, 10), dpi=85)
plot_1 = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, app)
canvas.draw()

toolbar_frame = tk.Frame(app)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

prompt_1_name = ttk.Label(app, text="Please Specificy File Destination:", font=("timesnewroman", 12))
prompt_1 = ttk.Entry(app)
prompt_1.insert(0, ".txt")

def specificyRange():
    global rangePrompt_1, rangePrompt_2
    window = tk.Toplevel(app)
    window.geometry("300x110")
    window.title("Specificy Range")
    blankspace = ttk.Label(window)
    blankspace.grid(row=0, column=0)
    rangePrompt_1 = ttk.Entry(window, width="10")
    rangePrompt_1_label = ttk.Label(window, text="Specificy range > "+str(max(dataX))+':')
    rangePrompt_2 = ttk.Entry(window, width="10")
    rangePrompt_2_label = ttk.Label(window, text="Specificy range < "+str(min(dataX))+':')
    rangePrompt_1_label.grid(row=1, column=1, sticky = 'w')
    rangePrompt_1.grid(row=2, column=1, sticky = 'w')
    rangePrompt_2_label.grid(row=3, column=1, sticky = 'w')
    rangePrompt_2.grid(row=4, column=1, sticky = 'w')

blankspace.grid(row = 0, column = 0, columnspan = 4)
settings.grid(row = 0, column = 0, sticky = 'w')
canvas.get_tk_widget().grid(row = 3, column = 1) #this is the graph (where data will be plotted)
prompt_1_name.grid(row = 1, column = 1, sticky = "ns")
prompt_1.grid(row = 2, column = 1, sticky = "ns")
toolbar_frame.grid(row = 4, column = 1, sticky = 'w')
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

def makeLineOfBestFit(dataX, dataY):
    try:
        scope[0].append(int(rangePrompt_1.get()))
    except:
        pass
    try:
        scope[1].append(int(rangePrompt_2.get()))
    except:
        pass
    if len(scope[0]) > 2:
        scope[0].pop(0)
    if len(scope[1]) > 2:
        scope[1].pop(0)
    LineOfBestFit = []
    newX = [x for x in range(int(min(dataX)-((scope[1][len(scope[1])-1])*-1)), int(max(dataX)+1+((scope[0][len(scope[0])-1]))))]
    linearDifference = []
    exponentialDifference = []
    parabolaDifference = []
    linearLine = [[], []]
    bestSlope = []
    exponentialLine = [[], []]
    bestRate = []
    parabolaLine = [[], []]

    try:
        for i in range(len(dataX)-1):
            x1, x2 = dataX[i], dataX[i+1]
            y1, y2 = dataY[i], dataY[i+1]
            slope = ((x2-x1)/(y2-y1))
            bestSlope.append(slope)
            bestRate.append(y2/y1)
        bestSlope = sum(bestSlope)/len(bestSlope)
        bestRate = sum(bestRate)/len(bestRate)
    except:
        bestRate = bestSlope = 1

    parabolaB = exponentialB = linearB = [y for y in dataY if dataX[dataY.index(y)] == 0]
    if linearB == []:
        linearB = dataY[0]-(bestSlope*dataX[0])
        linearLine[1] = [(bestSlope*x)+linearB for x in dataX]
        exponentialB = dataY[0]/(bestRate**dataX[0])
        exponentialLine[1] = [exponentialB*(bestRate**x) for x in dataX]
        parabolaB = dataY[0]-(dataX[0]**2)
        parabolaLine[1] = [(x**2)+parabolaB for x in dataX]

        linearLine[0] = [(bestSlope*x)+linearB for x in newX]
        exponentialLine[0] = [exponentialB*(bestRate**x) for x in newX]
        parabolaLine[0] = [(x**2)+parabolaB for x in newX]
    else:
        linearLine[1] = [(bestSlope*x)+linearB[0] for x in dataX]
        exponentialLine[1] = [exponentialB[0]*(bestRate**x) for x in dataX]
        parabolaLine[1] = [(x**2)+parabolaB[0] for x in dataX]
        linearLine[0] = [(bestSlope*x)+linearB[0] for x in newX]
        exponentialLine[0] = [exponentialB[0]*(bestRate**x) for x in newX]
        parabolaLine[0] = [(x**2)+parabolaB[0] for x in newX]

    for i in range(len(dataX)):
        if linearLine[1][i]-dataY[i] < 0:
            linearDifference.append((linearLine[1][i]-dataY[i])*-1)
        else:
            linearDifference.append(linearLine[1][i]-dataY[i])
        if exponentialLine[1][i]-dataY[i] < 0:
            exponentialDifference.append((exponentialLine[1][i]-dataY[i])*-1)
        else:
            exponentialDifference.append(exponentialLine[1][i]-dataY[i])
        if parabolaLine[1][i]-dataY[i] < 0:
            parabolaDifference.append((parabolaLine[1][i]-dataY[i])*-1)
        else:
            parabolaDifference.append(parabolaLine[1][i]-dataY[i])
    linearDifference = sum(linearDifference)/len(linearDifference)
    exponentialDifference = sum(exponentialDifference)/len(exponentialDifference)
    parabolaDifference = sum(parabolaDifference)/len(parabolaDifference)
    differences = [(linearDifference, linearLine[0], "Linear Graph"), (exponentialDifference, exponentialLine[0], "Exponential Graph"), (parabolaDifference, parabolaLine[0], "Parabola Graph")]
    LineOfBestFit, graphType = min(differences)[1], min(differences)[2]


    return (newX, LineOfBestFit, graphType, (linearLine, exponentialLine, parabolaLine))


def updatePlot_1(i):
    global dataX, dataY
    plot_1.clear()
    plot_1.set_xlabel("Runs")
    plot_1.set_ylabel("Words")

    file = prompt_1.get()
    try:
        dataX, dataY = fetchData(file)[0], fetchData(file)[1]
        plot_1.scatter(dataX, dataY)
        #newX, newY, graphType = makeLineOfBestFit(dataX, dataY)[0], makeLineOfBestFit(dataX, dataY)[1], makeLineOfBestFit(dataX, dataY)[2]
        #plot_1.set_title(graphType+'\n')
        #plot_1.plot(newX, newY)
    except FileNotFoundError:
        pass
    except ZeroDivisionError:
        raise Exception


app.title("Graph App")
app.geometry("575x540")
animatePlot = matAnimate.FuncAnimation(fig, updatePlot_1, interval=500)
app.mainloop()
