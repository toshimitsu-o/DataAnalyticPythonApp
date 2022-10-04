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

class ChartFrame(wx.Frame):
    """Class for chart frame window"""
    def __init__(self, title, search:Search, chartType, mode, parent=None):
        self.search = search
        self.chartType = chartType
        self.mode = mode

        wx.Frame.__init__(self, parent=parent, title=title, size=(800,600))

        self.result = None

        # create a panel in the frame
        self.pnl = wx.Panel(self)
        self.SetBackgroundColour("white")

        box = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 40))
        box.SetBackgroundColour("black")
        # Create items
        charTl = wx.StaticText(box, label="Chart ")
        charTl.SetForegroundColour("white")

        # Sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(charTl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
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
        
        if self.chartType == "Hourly Average":
            self.result = self.search.hourly_average(mode=self.mode)
            print(self.result)
            if self.mode == "alcohol":
                self.drawMultiBarChart()
            else:
                self.drawBarChart()
        elif self.chartType == "Accident Types":
            self.result = self.search.accident_type(mode=self.mode)
            print(self.result)
            if self.mode == "alcohol":
                self.drawMultiBarChart()
            else:
                self.drawBarChart()
        elif self.chartType == "By Month":
            self.result = self.search.calculate_by_month(mode=self.mode)
            print(self.result)
            if self.mode == "alcohol":
                self.drawMultiBarChart()
            else:
                self.drawBarChart()
        elif self.chartType == "By Day":
            self.result = self.search.calculate_by_day(mode=self.mode)
            print(self.result)
            if self.mode == "alcohol":
                self.drawMultiBarChart()
            else:
                self.drawBarChart()
        elif self.chartType == "LGA":
            self.result = self.search.calcAllLgas()
            self.drawBarChart()
        elif self.chartType == "Region":
            self.result = self.search.calcAllRegions()
            self.drawBarChart()
        else:
            pass

        if self.mode == "alcohol":
            self.drawMultiBarChart()
        # elif self.mode == "location":
        #     self.drawMapChart()
        else:
            self.drawBarChart()
        
    def drawBarChart(self):
        # labels = ['one', 'two', 'three', 'four', 'five']
        # data = [23,85, 72, 43, 52]
        labels = [i[0] for i in self.result]
        data = [i[1] for i in self.result]

        # Make figure and axes.
        self.axes.plot(1, 0)
        self.axes.set_xlabel('Month')
        self.axes.set_ylabel('Accident')
        self.axes.set_title(self.chartType)

        self.axes.bar(labels, data)

    def drawMultiBarChart(self):
        labels = [i[0] for i in self.result[0]]
        data1 = [i[1] for i in self.result[0]]
        data2 = [i[1] for i in self.result[1]]
        width = 0.3

        # Make figure and axes.
        self.axes.plot(1, 0)
        self.axes.set_xlabel('Month')
        self.axes.set_ylabel('Accident')

        self.axes.bar(labels, data1, width=width, label='Alcohol Related')
        self.axes.bar(np.arange(len(data2)) + width, data2, width=width, label='Non-Alcohol')
        self.axes.legend()

        self.axes.set_title(self.chartType)
    
    def drawMapChart(self):
        x = [144.9698,145.14671,144.80134,145.07011,144.9653,145.7914,145.00873,145.07229,145.02638,145.15439,145.04213,144.95479,145.06288,144.35796,145.07832,144.89081,145.16073,144.96245,144.99091]
        y = [-37.82202,-37.83166,-37.74003,-37.17891,-37.81808,-38.23087,-37.90637,-37.80207,-37.82156,-37.84541,-37.73512,-37.66725,-37.67821,-38.0824,-37.70195,-37.82599,-37.66936,-37.8127,-37.86532]
        #self.axes.plot(1, 0)
        datafile = 'images/vicmap.png'
        img = self.axes.imread(datafile)
        self.axes.scatter(x, y, s=50, c='blue', alpha=0.3, edgecolors='none', label='Lable A')
        #self.axes.imshow(img, zorder=0)
        self.axes.legend()
        self.axes.grid(True)