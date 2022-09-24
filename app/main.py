"""
Accident Analysis
"""

try:
    import wx
    import wx.grid
except ImportError:
    raise ImportError ("The wxPython module is required to run this program.")

APP_NAME = "Accident Analysis"

class mainFrame(wx.Frame):
    """
    Main Frame
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(mainFrame, self).__init__(*args, **kw)
        self.initialise()
            
    def initialise(self):

        # create a panel in the frame
        pnl = wx.Panel(self)
        #self.SetBackgroundColour((19,162,166,255))
        self.SetBackgroundColour("white")

        # Add Search box
        searchBox = wx.StaticBox(pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 80))
        searchBox.SetBackgroundColour("grey")
        # Search box items
        dateTl = wx.StaticText(searchBox, label="Date ")
        dateFrCt = wx.TextCtrl(searchBox)
        dateTo = wx.StaticText(searchBox, label="to ")
        dateToCt = wx.TextCtrl(searchBox)
        accTl = wx.StaticText(searchBox, label="Accident Type ")
        accKyCt = wx.TextCtrl(searchBox)
        typeList = ['Select from list', 'zero', 'one', 'two', 'three', 'four', 'five',
                      'six', 'seven', 'eight']
        accCh = wx.Choice(searchBox, choices=typeList)
        outTl = wx.StaticText(searchBox, label="Output ")
        outCb1 = wx.CheckBox(searchBox, label = 'Day')
        outCb2 = wx.CheckBox(searchBox, label = 'Hit&Run')
        outCb3 = wx.CheckBox(searchBox, label = 'Location')
        searchBtn = wx.Button(searchBox, label="Search", size=(100, 100))
        # Sizer 
        sizer = wx.GridBagSizer(hgap=0, vgap=0)
        # Date line
        sizer.Add(dateTl, pos=(0,0), flag=wx.ALIGN_LEFT)
        vSizer = wx.BoxSizer(wx.HORIZONTAL)
        vSizer.Add(dateFrCt, 0, wx.ALL, 0)
        vSizer.Add(dateTo, 0, wx.ALL, 0)
        vSizer.Add(dateToCt, 0, wx.ALL, 0)
        sizer.Add(vSizer, pos=(0,1), flag=wx.ALIGN_LEFT|wx.EXPAND)
        # Accident type line
        sizer.Add(accTl, pos=(1,0), flag=wx.ALIGN_LEFT)
        vSizer = wx.BoxSizer(wx.HORIZONTAL)
        vSizer.Add(accKyCt, 0, wx.ALL, 0)
        vSizer.Add(accCh, 0, wx.ALL, 0)
        sizer.Add(vSizer, pos=(1,1), flag=wx.ALIGN_LEFT|wx.EXPAND)
        # Output line
        sizer.Add(outTl, pos=(2,0), flag=wx.ALIGN_LEFT)
        vSizer = wx.BoxSizer(wx.HORIZONTAL)
        vSizer.Add(outCb1, 0, wx.ALL, 0)
        vSizer.Add(outCb2, 0, wx.ALL, 0)
        vSizer.Add(outCb3, 0, wx.ALL, 0)
        sizer.Add(vSizer, pos=(2,1), flag=wx.ALIGN_LEFT|wx.EXPAND)
        sizer.Add(searchBtn, pos=(0,2), span=(3,1), flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.EXPAND)
        # Set sizer
        searchBox.SetSizer(sizer)

        box = wx.StaticBox(pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 450))
        box.SetBackgroundColour("white")

        # Create a wxGrid object
        grid = wx.grid.Grid(box, -1)

        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        grid.CreateGrid(100, 10)

        # We can set the sizes of individual rows and columns
        # in pixels
        grid.SetRowSize(0, 60)
        grid.SetColSize(0, 120)

        # And set grid cell contents as strings
        grid.SetCellValue(0, 0, 'wxGrid is good')

        # Colours can be specified for grid cell contents
        grid.SetCellValue(3, 3, 'green on grey')
        grid.SetCellTextColour(3, 3, wx.GREEN)
        grid.SetCellBackgroundColour(3, 3, wx.LIGHT_GREY)

        # We can specify the some cells will store numeric
        # values rather than strings. Here we set grid column 5
        # to hold floating point values displayed with width of 6
        # and precision of 2
        grid.SetColFormatFloat(5, 6, 2)
        grid.SetCellValue(0, 6, '3.1415')
        # Set the whole grid read only
        grid.EnableEditing(False)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.ALL | wx.EXPAND, 0)
        box.SetSizer(sizer)
        
        # Bottom box
        boxBtm = wx.StaticBox(pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 50))
        boxBtm.SetBackgroundColour("black")
        # Create items
        charTl = wx.StaticText(boxBtm, label="Chart ")
        charTl.SetForegroundColour("white")
        cBtn1 = wx.Button(boxBtm, label="Hourly Average")
        cBtn2 = wx.Button(boxBtm, label="Accident Types")
        cBtn3 = wx.Button(boxBtm, label="By Month")
        cBtn4 = wx.Button(boxBtm, label="By Day")
        # Sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(charTl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.Add(cBtn1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.Add(cBtn2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.Add(cBtn3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.Add(cBtn4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        boxBtm.SetSizer(sizer)
        
        # and create a sizer to manage the layout of child widgets
        menubox = wx.StaticBox(pnl, wx.ID_ANY, "", pos =wx.DefaultPosition, size =(-1, 50))
        menubox.SetBackgroundColour((19,162,166,255))
        # button for Dataset
        btn1 = wx.Button(pnl, size =(200, 40), label="Dataset")
        bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        bmp = wx.Bitmap(bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        btn1.SetBitmap(bmp)
        self.Bind(wx.EVT_BUTTON, self.onDataset, btn1)
        #  button for Analyse
        btn2 = wx.Button(pnl, size =(200, 40), label="Analyse")
        bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        bmp = wx.Bitmap(bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        btn2.SetBitmap(bmp)
        self.Bind(wx.EVT_BUTTON, self.onAnalyse, btn2)
        #  button for Analyse
        btn3 = wx.Button(pnl, size =(200, 40), label="Alcohol")
        bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        bmp = wx.Bitmap(bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        btn3.SetBitmap(bmp)
        self.Bind(wx.EVT_BUTTON, self.onAlcohol, btn3)
        #  button for Location
        btn4 = wx.Button(pnl, size =(200, 40), label="Location")
        bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        bmp = wx.Bitmap(bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        btn4.SetBitmap(bmp)
        self.Bind(wx.EVT_BUTTON, self.onLocation, btn4)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(btn1, 0, wx.EXPAND, 0)
        sizer.Add(btn2, 0, wx.EXPAND, 0)
        sizer.Add(btn3, 0, wx.EXPAND, 0)
        sizer.Add(btn4, 0, wx.EXPAND, 0)
        menubox.SetSizer(sizer)
        

        # Sizer for grid
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(menubox, 0, wx.ALL | wx.EXPAND,0)
        sizer.Add(searchBox, 0, wx.ALL | wx.EXPAND, 0)
        sizer.Add(box, 5, wx.ALL |wx.EXPAND, 0)
        sizer.Add(boxBtm, 0, wx.ALL |wx.EXPAND | wx.ALIGN_BOTTOM, 0)
        pnl.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to "+ APP_NAME)


    def onDataset(self, event):
        wx.MessageBox("Dataset will happen")

    def onAnalyse(self, event):
        wx.MessageBox("Analyse will happen")

    def onAlcohol(self, event):
        wx.MessageBox("Alcohol will happen")

    def onLocation(self, event):
        wx.MessageBox("Location will happen")

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        importItem = fileMenu.Append(-1, "&Import\tCtrl-I",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnImport, importItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnImport(self, event):
        """Import function will be here later"""
        wx.MessageBox("Import function will be linked here later.")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This app helps to analyse a dataset of Victoria State Accidents.",
                      APP_NAME,
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frame = mainFrame(None, title=APP_NAME, size=(800,600))
    frame.Show()
    app.MainLoop()