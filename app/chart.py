"""
Accident Analysis wxPython Chart Frame
"""

try:
    import wx
    #from wx.lib.plot import PolyLine, PlotCanvas, PlotGraphics
    import numpy as np
    import matplotlib
    matplotlib.use('WXAgg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
    from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar2Wx
except ImportError:
    raise ImportError ("The wxPython module is required to run this program.")
from cProfile import label
from re import search
from tkinter import CENTER, RIGHT
from search import Search

# Some data
# Pie chart, where the slices will be ordered and plotted counter-clockwise :
labels = 'Hogs', 'Frogs', 'Logs', 'Dogs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # Only "explode" the 2nd slice (i.e. 'Hogs'). 
data = [23, 45, 56, 78, 213]

class ChartFrame(wx.Frame):
    """Class for chart frame window"""
    def __init__(self, title, parent=None, search=None, chartType=None, mode=None):
        self.search = search
        self.chartType = chartType
        self.mode = mode

        wx.Frame.__init__(self, parent=parent, title=title, size=(800,600))

        # create a panel in the frame
        self.pnl = wx.Panel(self)
        self.SetBackgroundColour("white")

        box = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 40))
        box.SetBackgroundColour("black")
        # Create items
        charTl = wx.StaticText(box, label="Chart ")
        charTl.SetForegroundColour("white")
        # Testing some parameters
        testTxt = wx.StaticText(box, label="search: "+ str(search) + " chartType: " + chartType + " mode: " + mode)
        testTxt.SetForegroundColour("red")
        # Sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(charTl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        sizer.Add(testTxt, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        box.SetSizer(sizer)

        # Main
        self.main = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, -1))

        # Plot
        self.makeCtrls()
        self.plotLayout()
        self.getChart()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        sizer.Add(self.main, 5, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER | wx.EXPAND, 0)
        self.pnl.SetSizer(sizer)

        self.Show()
        
    #-----------------------------------------------------------------------

    def makeCtrls(self):
        """Create Matplotlib navigation toolbar"""
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.main, -1, self.figure)
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()

    def plotLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.main.SetSizer(sizer)
    
    def getChart(self):
        if self.mode == "alcohol":
            self.drawMultiBarChart()
        else:
            self.drawBarChart()
        
    def drawBarChart(self):
        labels = ['one', 'two', 'three', 'four', 'five']
        data = [23,85, 72, 43, 52]

        # Make figure and axes.
        self.axes.plot(1, 0)
        self.axes.set_xlabel('Month')
        self.axes.set_ylabel('Accident')
        self.axes.set_title("I am title")

        self.axes.bar(labels, data) 

    def drawMultiBarChart(self):
        labels = ['one', 'two', 'three', 'four', 'five']
        data1 = [23,85, 72, 43, 52]
        data2 = [42, 35, 21, 16, 9]
        width = 0.3

        # Make figure and axes.
        self.axes.plot(1, 0)
        self.axes.set_xlabel('Month')
        self.axes.set_ylabel('Accident')

        self.axes.bar(labels, data1, width=width, label='Alcohol Related')
        self.axes.bar(np.arange(len(data2)) + width, data2, width=width, label='Non-Alcohol')
        self.axes.legend()

        self.axes.set_title("I am title")