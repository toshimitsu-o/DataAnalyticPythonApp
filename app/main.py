"""
Accident Analysis
"""

try:
    import wx
    import wx.grid
except ImportError:
    raise ImportError ("The wxPython module is required to run this program.")

APP_NAME = "Accident Analysis"

class MainFrame(wx.Frame):
    """
    Main Frame
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw)
        self.initialise()
            
    def initialise(self):

        # Define state of program: main, alcohol, location
        self.menu = ""

        # create a panel in the frame
        self.pnl = wx.Panel(self)
        self.frame_number = 1
        #self.SetBackgroundColour((19,162,166,255))
        self.SetBackgroundColour("white")

        # Add Search box
        self.searchBox = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 80))
        self.searchBox.SetBackgroundColour((247,247,247,255))
        # Search box items
        self.dateTl = wx.StaticText(self.searchBox, label="Date ")
        self.dateFrCt = wx.TextCtrl(self.searchBox)
        self.dateTo = wx.StaticText(self.searchBox, label="to ")
        self.dateToCt = wx.TextCtrl(self.searchBox)
        self.accTl = wx.StaticText(self.searchBox, label="Accident Type ")
        self.accKyCt = wx.TextCtrl(self.searchBox)
        self.typeList = ['Select from list', 'zero', 'one', 'two', 'three', 'four', 'five',
                      'six', 'seven', 'eight']
        self.accCh = wx.Choice(self.searchBox, choices=self.typeList)
        self.outTl = wx.StaticText(self.searchBox, label="Output ")
        self.outCb1 = wx.CheckBox(self.searchBox, label = 'Day')
        self.outCb2 = wx.CheckBox(self.searchBox, label = 'Hit&Run')
        self.outCb3 = wx.CheckBox(self.searchBox, label = 'Location')
        self.searchBtn = wx.Button(self.searchBox, label="Search", size=(100, 100))
        # Sizer 
        self.schSizer = wx.GridBagSizer(hgap=0, vgap=0)
        # Date line
        self.schSizer.Add(self.dateTl, pos=(0,0), flag=wx.ALIGN_LEFT)
        self.vSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vSizer.Add(self.dateFrCt, 0, wx.ALL, 0)
        self.vSizer.Add(self.dateTo, 0, wx.ALL, 0)
        self.vSizer.Add(self.dateToCt, 0, wx.ALL, 0)
        self.schSizer.Add(self.vSizer, pos=(0,1), flag=wx.ALIGN_LEFT|wx.EXPAND)
        # Accident type line
        self.schSizer.Add(self.accTl, pos=(1,0), flag=wx.ALIGN_LEFT)
        self.vSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vSizer.Add(self.accKyCt, 0, wx.ALL, 0)
        self.vSizer.Add(self.accCh, 0, wx.ALL, 0)
        self.schSizer.Add(self.vSizer, pos=(1,1), flag=wx.ALIGN_LEFT|wx.EXPAND)
        # Output line
        self.schSizer.Add(self.outTl, pos=(2,0), flag=wx.ALIGN_LEFT)
        self.vSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vSizer.Add(self.outCb1, 0, wx.ALL, 0)
        self.vSizer.Add(self.outCb2, 0, wx.ALL, 0)
        self.vSizer.Add(self.outCb3, 0, wx.ALL, 0)
        self.schSizer.Add(self.vSizer, pos=(2,1), flag=wx.ALIGN_LEFT|wx.EXPAND)
        self.schSizer.Add(self.searchBtn, pos=(0,2), span=(3,1), flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.EXPAND)
        # Set sizer
        self.searchBox.SetSizer(self.schSizer)

        # Box for summary
        self.sumBox = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, -1))
        self.sumBox.SetBackgroundColour("white")
        # Items
        self.sumTl = wx.StaticText(self.sumBox, label="Summary ")
        self.found = wx.StaticText(self.sumBox, label="230 found (out of 23000)")
        self.injury = wx.StaticText(self.sumBox, label="Injury: 200")
        self.fatality = wx.StaticText(self.sumBox, label="fatality: 30")
        # Sizer
        self.sumSizer = wx.BoxSizer(wx.VERTICAL)
        self.sumSizer.Add(self.sumTl, 0, wx.ALL | wx.EXPAND, 0)
        self.sumSizer.Add(self.found, 0, wx.ALL | wx.EXPAND, 0)
        self.sumSizer.Add(self.injury, 0, wx.ALL | wx.EXPAND, 0)
        self.sumSizer.Add(self.fatality, 0, wx.ALL | wx.EXPAND, 0)
        self.sumBox.SetSizer(self.sumSizer)

        # Search Bar
        self.schbarSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.schbarSizer.Add(self.searchBox, 5, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        self.schbarSizer.Add(self.sumBox, 1, wx.ALL | wx.ALIGN_TOP | wx.EXPAND, 0)

        # Box for grid
        self.box = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 450))
        self.box.SetBackgroundColour("white")

        # Create a wxGrid object
        grid = wx.grid.Grid(self.box, -1)

        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        grid.CreateGrid(100, 20)

        # We can set the sizes of individual rows and columns
        # in pixels
        # grid.SetRowSize(0, 60)
        # grid.SetColSize(0, 120)

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
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(grid, 0, wx.ALL | wx.EXPAND, 0)
        self.box.SetSizer(self.sizer)
        
        # Bottom box
        self.boxBtm = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 50))
        self.boxBtm.SetBackgroundColour("black")
        # Create items
        self.charTl = wx.StaticText(self.boxBtm, label="Chart ")
        self.charTl.SetForegroundColour("white")
        self.cBtn1 = wx.Button(self.boxBtm, label="Hourly Average")
        self.Bind(wx.EVT_BUTTON, self.onChartHour, self.cBtn1)
        self.cBtn2 = wx.Button(self.boxBtm, label="Accident Types")
        self.cBtn3 = wx.Button(self.boxBtm, label="By Month")
        self.cBtn4 = wx.Button(self.boxBtm, label="By Day")
        # Sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.charTl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.sizer.Add(self.cBtn1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.sizer.Add(self.cBtn2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.sizer.Add(self.cBtn3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.sizer.Add(self.cBtn4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.boxBtm.SetSizer(self.sizer)
        
        # and create a sizer to manage the layout of child widgets
        self.menubox = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =wx.DefaultPosition, size =(-1, 50))
        self.menubox.SetBackgroundColour((19,162,166,255))
        # button for Dataset
        self.btn1 = wx.Button(self.pnl, size =(200, 40), label="Dataset")
        self.bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        self.bmp = wx.Bitmap(self.bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        self.btn1.SetBitmap(self.bmp)
        self.Bind(wx.EVT_BUTTON, self.onDataset, self.btn1)
        #  button for Analyse
        self.btn2 = wx.Button(self.pnl, size =(200, 40), label="Analyse")
        self.bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        self.bmp = wx.Bitmap(self.bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        self.btn2.SetBitmap(self.bmp)
        self.Bind(wx.EVT_BUTTON, self.onAnalyse, self.btn2)
        #  button for Analyse
        self.btn3 = wx.Button(self.pnl, size =(200, 40), label="Alcohol")
        self.bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        self.bmp = wx.Bitmap(self.bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        self.btn3.SetBitmap(self.bmp)
        self.Bind(wx.EVT_BUTTON, self.onAlcohol, self.btn3)
        #  button for Location
        self.btn4 = wx.Button(self.pnl, size =(200, 40), label="Location")
        self.bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        self.bmp = wx.Bitmap(self.bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        self.btn4.SetBitmap(self.bmp)
        self.Bind(wx.EVT_BUTTON, self.onLocation, self.btn4)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.btn1, 0, wx.EXPAND, 0)
        self.sizer.Add(self.btn2, 0, wx.EXPAND, 0)
        self.sizer.Add(self.btn3, 0, wx.EXPAND, 0)
        self.sizer.Add(self.btn4, 0, wx.EXPAND, 0)
        self.menubox.SetSizer(self.sizer)
        
        # Dataset import
        self.importBox = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =wx.DefaultPosition, size =(-1, 100))
        self.importBox.SetBackgroundColour((247,247,247,255))
        # Items
        self.importTl = wx.StaticText(self.importBox, label="Import Dataset ")
        #importTl.SetForegroundColour("white")
        self.importBtn = wx.Button(self.importBox, label="Select a file")
        self.Bind(wx.EVT_BUTTON, self.onFileOpen, self.importBtn)
        # Sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.importTl, 0, wx.ALL | wx.EXPAND,0)
        self.sizer.Add(self.importBtn, 0, wx.ALL | wx.EXPAND,0)
        self.importBox.SetSizer(self.sizer)

        # create a menu bar
        self.makeMenuBar()

        # Build main content structure
        if self.menu == "main":
            self.buidImport()
        else:
            self.buidMain()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to "+ APP_NAME)
    
    def buidImport(self):
        # Sizer for main structure
        self.importSizer = wx.BoxSizer(wx.VERTICAL)
        self.importSizer.Add(self.menubox, 0, wx.ALL | wx.EXPAND,0)
        self.importSizer.Add(self.importBox, 5, wx.ALL |wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        self.importSizer.Add(self.boxBtm, 0, wx.ALL |wx.EXPAND | wx.ALIGN_BOTTOM, 0)
        self.pnl.SetSizer(self.importSizer)

    def buidMain(self):
        # Sizer for main structure
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.menubox, 0, wx.ALL | wx.EXPAND,0)
        self.mainSizer.Add(self.schbarSizer, 0, wx.ALL | wx.EXPAND, 0)
        self.mainSizer.Add(self.box, 5, wx.ALL |wx.EXPAND, 0)
        self.mainSizer.Add(self.boxBtm, 0, wx.ALL |wx.EXPAND | wx.ALIGN_BOTTOM, 0)
        self.pnl.SetSizer(self.mainSizer)

    def onFileOpen(self, event):
        # Ask the user what new file to open
        with wx.FileDialog(self, "Open XYZ file", wildcard="CSV files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.loadFile(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def loadFile(self, filepath):
        filepath = str(filepath)
        self.menu = "main"
        #self.pnl.Update()
        wx.MessageBox("Filepath for Dataset is: " + filepath)

    def onDataset(self, event):
        wx.MessageBox("Dataset will happen")

    def onAnalyse(self, event):
        self.menu = "main"
        self.importSizer.Destroy()
        self.importBox.Destroy()
        #self.buidMain()
        self.Update()

        #wx.MessageBox("Analyse will happen")

    def onAlcohol(self, event):
        wx.MessageBox("Alcohol will happen")

    def onLocation(self, event):
        wx.MessageBox("Location will happen")
    
    def onChartHour(self, event):
        title = 'Chart {}'.format(self.frame_number)
        frame = ChartFrame(title=title)
        self.frame_number += 1

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

class ChartFrame(wx.Frame):
    """Class for chart frame window"""
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title, size=(1000,625))

        # create a panel in the frame
        pnl = wx.Panel(self)
        self.SetBackgroundColour("white")

        # bar box
        box = wx.StaticBox(pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 40))
        box.SetBackgroundColour("black")
        # Create items
        charTl = wx.StaticText(box, label="Chart ")
        charTl.SetForegroundColour("white")
        # Sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(charTl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        box.SetSizer(sizer)

        # Main
        main = wx.StaticBox(pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, -1))
        text = wx.StaticText(main, label="Chart will be inserted")
        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        main.SetSizer(sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        sizer.Add(main, 5, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER | wx.EXPAND, 0)
        pnl.SetSizer(sizer)

        self.Show()

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frame = MainFrame(None, title=APP_NAME, size=(1280,800))
    frame.Show()
    app.MainLoop()