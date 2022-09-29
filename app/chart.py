"""
Accident Analysis wxPython Chart Frame
"""

try:
    import wx
    from wx.lib.plot import PolyLine, PlotCanvas, PlotGraphics
except ImportError:
    raise ImportError ("The wxPython module is required to run this program.")
from re import search
from search import Search

def drawBarGraph():
    setWidth = 10
    # Bar graph
    points1=[(1,0), (1,10)]
    line1 = PolyLine(points1, colour='green', legend='Feb.', width=setWidth)
    points1g=[(2,0), (2,4)]
    line1g = PolyLine(points1g, colour='red', legend='Mar.', width=setWidth)
    points1b=[(3,0), (3,6)]
    line1b = PolyLine(points1b, colour='blue', legend='Apr.', width=setWidth)
    points2=[(4,0), (4,12)]
    line2 = PolyLine(points2, colour='Yellow', legend='May', width=setWidth)
    points2g=[(5,0), (5,8)]
    line2g = PolyLine(points2g, colour='orange', legend='June', width=setWidth)
    points2b=[(6,0), (6,4)]
    line2b = PolyLine(points2b, colour='brown', legend='July', width=setWidth)
    return PlotGraphics([line1, line1g, line1b, line2, line2g, line2b],
                        "Bar Graph - (Turn on Grid, Legend)", "Months", 
                        "Number of Students")

class ChartFrame(wx.Frame):
    """Class for chart frame window"""
    def __init__(self, title, parent=None, search=None, chartType=None, mode=None):
        wx.Frame.__init__(self, parent=parent, title=title, size=(1000,625))

        # create a panel in the frame
        self.pnl = wx.Panel(self)
        self.SetBackgroundColour("white")

        # bar box
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
        self.buildChart()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        sizer.Add(self.main, 5, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER | wx.EXPAND, 0)
        self.pnl.SetSizer(sizer)

        self.Show()
    
    def buildChart(self):
        # Create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        checkSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create canvas and draw
        self.canvas = PlotCanvas(self.main)
        self.canvas.Draw(drawBarGraph())
        
        toggleGrid = wx.CheckBox(self.main, label="Grid")
        toggleGrid.SetValue(True)
        toggleGrid.Bind(wx.EVT_CHECKBOX, self.OnToggleGrid)
        
        toggleLegend = wx.CheckBox(self.main, label="Legend")
        toggleLegend.SetValue(False)
        toggleLegend.Bind(wx.EVT_CHECKBOX, self.OnToggleLegend)
        
        # Layout the widgets
        mainSizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
        checkSizer.Add(toggleGrid, 0, wx.ALL, 5)
        checkSizer.Add(toggleLegend, 0, wx.ALL, 5)
        mainSizer.Add(checkSizer)
        self.main.SetSizer(mainSizer)

    def OnToggleGrid(self, event):
        self.canvas.enableGrid = event.IsChecked()  

    def OnToggleLegend(self, event):
        self.canvas.enableLegend = event.IsChecked()