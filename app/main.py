"""
Accident Analysis wxPython Main Frame
"""

try:
    import wx
    import wx.adv
    import wx.grid
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError ("The wxPython module is required to run this program.")

from search import Search
from chart import ChartFrame
import importData

APP_NAME = "Accident Analysis"

# def connect():
#     """
#     This is the sqlite3 connection.
#     """
    
#     con_str= 'accidentDatabase.db'
#     cnn = sqlite3.connect(con_str)
#     return cnn
#     cnn.close()

# def dataRowsCount():
#     """
#     To count the rows in the database.
#     """
    
#     con = connect()
#     cur=con.cursor()
#     cur.execute("SELECT * FROM Accident")
#     rows=cur.fetchall()
#     i=0
#     for r in rows:
#         i+=1
#     return i

class MainFrame(wx.Frame):
    """
    Main Frame
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw)
        self.initialise()
            
    def initialise(self):
        # Initial values

        # Define state of program: main, alcohol, location
        self.mode = "main"
        self.built = 0
        self.search = Search(To_Date=None, From_Date =None, Accident_Type_List=None, Lga=None, Region=None)
        self.resultDb = None
        self.minDate = "2013-03-01"
        self.maxDate = "2013-03-01"


        # create a panel in the frame
        self.pnl = wx.Panel(self)
        self.frame_number = 1
        #self.SetBackgroundColour((19,162,166,255))
        self.SetBackgroundColour("white")

        # try:
        #     self.result = self.search.getResult()
        # except:
        #     wx.MessageBox("Dataset is empty. Please select Dataset in the menu bar to import.")

        if self.search.checkTable():
            # Get and set dates
            dateRange = self.search.getDateRange()
            self.minDate = dateRange[0]
            self.maxDate = dateRange[1]
            self.search.From_Date = self.minDate
            self.search.To_Date = self.maxDate
            # Get result from database
            self.resultDb = self.search.getResult()

            # Make a list of accident types
            listAccidentTpes = self.search.listAccidentType()
            if (listAccidentTpes):
                self.accidentTypes = self.search.listAccidentType()
                self.accidentTypes.insert(0, "All types")
            
        else:
            self.accidentTypes = ["No Accident Types"]
        
        # create a menu bar
        self.makeMenuBar()
        # Make menu box for buttons
        self.makeMenuBox()

        # If dataset is not empty
        if self.resultDb:
            # Build main content structure
            self.buidMain()
            self.built += 1
        else:
            # Sizer for main structure
            self.mainSizer = wx.BoxSizer(wx.VERTICAL)
            
            # Box for grid
            self.box = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 450))
            self.box.SetBackgroundColour("white")
            # Sizer for main structure
            self.mainSizer.Add(self.menubox, 0, wx.ALL | wx.EXPAND,0)
            self.mainSizer.Add(self.box, 5, wx.ALL |wx.EXPAND, 0)
            self.pnl.SetSizer(self.mainSizer)
            # Disable buttons
            wx.MessageBox("Dataset is empty. Please select Dataset in the menu bar to import.")

        # Make a status bar
        #self.CreateStatusBar()
        #self.SetStatusText("Welcome to "+ APP_NAME)
    
    def updateData(self):
        if self.resultDb:
            self.rows = self.resultDb
            for i in range (0, len(self.rows)):
                #self.grid.SetRowLabelValue(i, "")
                self.grid.SetRowLabelSize(0)
                for j in range(0, 13):
                    cell = self.rows[i]
                    self.grid.SetCellValue(i, j, str(cell[j]))
        else:
            wx.MessageBox("Dataset is empty. Please select Dataset in the menu bar to import.")

    def buidMain(self):
        dateRange = self.search.getDateRange()
        self.minDate = dateRange[0]
        self.maxDate = dateRange[1]
        self.resultDb = self.search.getResult()
        self.accidentTypes = self.search.listAccidentType()
        self.accidentTypes.insert(0, "All types")
        if self.built > 0:
            # self.mainSizer.Destroy()
            # self.pnl.Layout()
            #Clear items in the sizer
            # for child in self.mainSizer.GetChildren():
            #     self.mainSizer.Detach(child.Window)
            #     self.mainSizer.Layout()
            # self.searchBox.Destroy()
            # self.box.Destroy()
            # self.boxBtm.Destroy()
            # self.mainSizer.Layout()
            
            #self.accCh = wx.Choice(self.searchBox, choices=self.accidentTypes)
            self.searchBox.Destroy()
            self.schbarSizer.Layout()
            self.makeSearchBox()
            self.schbarSizer.Add(self.searchBox, 5, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
            self.schbarSizer.Layout()

            #self.setSeaerchDates()
            self.updateGrid()
            #self.schSizer.Layout()
        else:
            # Make search bar for search box and summary
            self.makeSchbar()
            # Make grid box
            self.makeGridBox()
            # Make bottom box for chart buttons
            self.makeBtmBox()
            # Sizer for main structure
            self.mainSizer = wx.BoxSizer(wx.VERTICAL)
            self.mainSizer.Add(self.menubox, 0, wx.ALL | wx.EXPAND,0)
            self.mainSizer.Add(self.schbarSizer, 0, wx.ALL | wx.EXPAND, 0)
            self.mainSizer.Add(self.box, 5, wx.ALL |wx.EXPAND, 0)
            self.mainSizer.Add(self.boxBtm, 0, wx.ALL |wx.EXPAND | wx.ALIGN_BOTTOM, 0)
            self.pnl.SetSizer(self.mainSizer)
            self.pnl.Layout()
    
    def makeMenuBox(self):
        # Box for menu box buttons
        self.menubox = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =wx.DefaultPosition, size =(-1, 55))
        self.menubox.SetBackgroundColour((19,162,166,255))
        # button for Dataset
        self.btn1 = wx.Button(self.pnl, size =(160, 40), label="Dataset")
        self.bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        self.bmp = wx.Bitmap(self.bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        self.btn1.SetBitmap(self.bmp)
        self.Bind(wx.EVT_BUTTON, self.onFileOpen, self.btn1)
        #  button for Analyse
        self.btn2 = wx.Button(self.pnl, size =(160, 40), label="Analyse")
        self.bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        self.bmp = wx.Bitmap(self.bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        self.btn2.SetBitmap(self.bmp)
        self.Bind(wx.EVT_BUTTON, self.onAnalyse, self.btn2)
        #  button for Analyse
        self.btn3 = wx.Button(self.pnl, size =(160, 40), label="Alcohol")
        self.bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        self.bmp = wx.Bitmap(self.bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        self.btn3.SetBitmap(self.bmp)
        self.Bind(wx.EVT_BUTTON, self.onAlcohol, self.btn3)
        #  button for Location
        self.btn4 = wx.Button(self.pnl, size =(160, 40), label="Location")
        self.bmp = wx.Bitmap('btn.png', wx.BITMAP_TYPE_PNG).ConvertToImage()
        self.bmp = wx.Bitmap(self.bmp.Scale(30, 30, wx.IMAGE_QUALITY_HIGH))
        self.btn4.SetBitmap(self.bmp)
        self.Bind(wx.EVT_BUTTON, self.onLocation, self.btn4)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.btn1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)
        self.sizer.Add(self.btn2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)
        self.sizer.Add(self.btn3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)
        self.sizer.Add(self.btn4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)
        self.menubox.SetSizer(self.sizer)

    def makeSearchBox(self):
        # Make Search box
        self.searchBox = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 60))
        self.searchBox.SetBackgroundColour((247,247,247,255))
        # Search box items
        self.dateTl = wx.StaticText(self.searchBox, label="Date ")
        self.dateFrCt = wx.adv.DatePickerCtrl(self.searchBox)

        self.dateTo = wx.StaticText(self.searchBox, label="to ")
        self.dateToCt = wx.adv.DatePickerCtrl(self.searchBox)

        self.accTl = wx.StaticText(self.searchBox, label="Accident Type ")
        self.accKyCt = wx.TextCtrl(self.searchBox)
        self.accCh = wx.Choice(self.searchBox, choices=self.accidentTypes)
        self.outTl = wx.StaticText(self.searchBox, label="Output ")
        self.outCb1 = wx.CheckBox(self.searchBox, label = 'Day')
        self.outCb2 = wx.CheckBox(self.searchBox, label = 'Hit&Run')
        self.outCb3 = wx.CheckBox(self.searchBox, label = 'Location')
        self.searchBtn = wx.Button(self.searchBox, label="Search", size=(100, 30))
        self.searchBtn.Bind(wx.EVT_BUTTON, self.onSearch)
        # Sizer 
        self.schSizer = wx.GridBagSizer(hgap=0, vgap=0)
        # Date line
        self.schSizer.Add(self.dateTl, pos=(0,0), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.vSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vSizer.Add(self.dateFrCt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        self.vSizer.Add(self.dateTo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        self.vSizer.Add(self.dateToCt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        self.schSizer.Add(self.vSizer, pos=(0,1), flag=wx.ALIGN_LEFT|wx.EXPAND)
        # Accident type line
        self.schSizer.Add(self.accTl, pos=(1,0), flag=wx.ALIGN_LEFT)
        self.vSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vSizer.Add(self.accKyCt, 0, wx.ALL, 0)
        self.vSizer.Add(self.accCh, 0, wx.ALL, 0)
        self.schSizer.Add(self.vSizer, pos=(1,1), flag=wx.ALIGN_LEFT|wx.EXPAND)
        # Output line
        # self.schSizer.Add(self.outTl, pos=(2,0), flag=wx.ALIGN_LEFT)
        # self.vSizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.vSizer.Add(self.outCb1, 0, wx.ALL, 0)
        # self.vSizer.Add(self.outCb2, 0, wx.ALL, 0)
        # self.vSizer.Add(self.outCb3, 0, wx.ALL, 0)
        #self.schSizer.Add(self.vSizer, pos=(2,1), flag=wx.ALIGN_LEFT|wx.EXPAND)
        self.schSizer.Add(self.searchBtn, pos=(0,2), span=(2,1), flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.EXPAND)
        # Set sizer
        self.searchBox.SetSizer(self.schSizer)
        # Set dates controls
        if self.resultDb:
            self.setSeaerchDates()

    def setSeaerchDates(self):
        minY = int(self.minDate[0:4])
        minM = int(self.minDate[5:7].lstrip('0'))-1
        minD = int(self.minDate[-2:].lstrip('0'))
        maxY = int(self.maxDate[0:4])
        maxM = int(self.maxDate[5:7].lstrip('0'))-1
        maxD = int(self.maxDate[-2:].lstrip('0'))
        self.dateFrCt.SetValue(wx.DateTime.FromDMY(minD,minM,minY))
        self.dateFrCt.SetRange(wx.DateTime.FromDMY(minD,minM,minY),wx.DateTime.FromDMY(maxD,maxM,maxY))
        self.dateToCt.SetValue(wx.DateTime.FromDMY(maxD,maxM,maxY))
        self.dateToCt.SetRange(wx.DateTime.FromDMY(minD,minM,minY),wx.DateTime.FromDMY(maxD,maxM,maxY))

    def makeSumBox(self):
        foundLbl = "230 found (out of 23000)"
        injuryLbl = "Injury: 200"
        fatalityLbl = "fatality: 30"

        # Box for result summary
        self.sumBox = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, -1))
        self.sumBox.SetBackgroundColour("white")
        # Items
        self.sumTl = wx.StaticText(self.sumBox, label="Summary ")
        self.found = wx.StaticText(self.sumBox, label=foundLbl)
        self.injury = wx.StaticText(self.sumBox, label=injuryLbl)
        self.fatality = wx.StaticText(self.sumBox, label=fatalityLbl)
        # Sizer
        self.sumSizer = wx.BoxSizer(wx.VERTICAL)
        self.sumSizer.Add(self.sumTl, 0, wx.ALL | wx.EXPAND, 0)
        self.sumSizer.Add(self.found, 0, wx.ALL | wx.EXPAND, 0)
        self.sumSizer.Add(self.injury, 0, wx.ALL | wx.EXPAND, 0)
        self.sumSizer.Add(self.fatality, 0, wx.ALL | wx.EXPAND, 0)
        self.sumBox.SetSizer(self.sumSizer)
    
    def makeSchbar(self):
        # Make search box for search form
        self.makeSearchBox()
        # Make summary box for result summary
        self.makeSumBox()
        # Search Bar
        self.schbarSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.schbarSizer.Add(self.searchBox, 5, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        #self.schbarSizer.Add(self.sumBox, 1, wx.ALL | wx.ALIGN_TOP | wx.EXPAND, 0)
    
    def makeGridBox(self):
        # Box for grid
        self.box = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 450))
        self.box.SetBackgroundColour("white")

        self.buildGrid()

        self.gridSizer = wx.BoxSizer(wx.VERTICAL)
        self.gridSizer.Add(self.grid, 0, wx.ALL | wx.EXPAND, 0)
        self.box.SetSizer(self.gridSizer)

    def updateGrid(self):
        self.grid.Destroy()
        #self.gridSizer.Destroy(self.grid)
        # Clear items in the sizer
        # for child in self.gridSizer.GetChildren():
        #     self.gridSizer.Detach(child.Window)
        #     self.gridSizer.Layout()
        self.buildGrid()
        self.gridSizer.Add(self.grid, 0, wx.ALL | wx.EXPAND, 0)
        self.gridSizer.Layout()
    
    def buildGrid(self):
        # Create a wxGrid object
        self.grid = wx.grid.Grid(self.box, -1)

        if self.resultDb:
            # This is to create the grid with same rows as database.
            r = self.search.dataRowsCount()
            self.grid.CreateGrid(r, 13)
            self.grid.SetColLabelValue(0, "No")
            self.grid.SetColSize(0, 12)
            self.grid.SetColLabelValue(1, "Date")
            self.grid.SetColSize(1, 90)
            self.grid.SetColLabelValue(2, "Time")
            self.grid.SetColSize(2, 70)
            self.grid.SetColLabelValue(3, "Type")
            self.grid.SetColSize(3, 150)
            self.grid.SetColLabelValue(4, "Day")
            self.grid.SetColSize(4, 60)
            self.grid.SetColLabelValue(5, "Severity")
            self.grid.SetColSize(5, 150)
            self.grid.SetColLabelValue(6, "Longitude")
            self.grid.SetColSize(6, 70)
            self.grid.SetColLabelValue(7, "Latitude")
            self.grid.SetColSize(7, 70)
            self.grid.SetColLabelValue(8, "LGA")
            self.grid.SetColSize(8, 100)
            self.grid.SetColLabelValue(9, "Region")
            self.grid.SetColSize(9, 120)
            self.grid.SetColLabelValue(10, "Fatalities")
            self.grid.SetColSize(10, 60)
            self.grid.SetColLabelValue(11, "Injuries")
            self.grid.SetColSize(11, 60)
            self.grid.SetColLabelValue(12, "Alcohol")
            self.grid.SetColSize(12, 60)
            self.updateData()

            # Set the whole grid read only
            self.grid.EnableEditing(False)

    def makeBtmBox(self):
        # Bottom box for chart buttons
        self.boxBtm = wx.StaticBox(self.pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 50))
        self.boxBtm.SetBackgroundColour("black")
        # Create items
        self.charTl = wx.StaticText(self.boxBtm, label="Chart ")
        self.charTl.SetForegroundColour("white")
        self.cBtn1 = wx.Button(self.boxBtm, label="Hourly Average")
        self.cBtn2 = wx.Button(self.boxBtm, label="Accident Types")
        self.cBtn3 = wx.Button(self.boxBtm, label="By Month")
        self.cBtn4 = wx.Button(self.boxBtm, label="By Day")
        self.cBtn5 = wx.Button(self.boxBtm, label="LGA")
        self.cBtn6 = wx.Button(self.boxBtm, label="Region")
        self.cBtn7 = wx.Button(self.boxBtm, label="Map")
        # Bind event handler with all buttons
        buttons = [self.cBtn1,self.cBtn2,self.cBtn3,self.cBtn4,self.cBtn5,self.cBtn6]
        for btn in buttons:
            self.Bind(wx.EVT_BUTTON, self.onChart, btn)
        self.Bind(wx.EVT_BUTTON, self.onMap, self.cBtn7)

        # Sizer
        self.boxBtmSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.setBoxBtmSizer()
        self.boxBtm.SetSizer(self.boxBtmSizer)

    def setBoxBtmSizer(self, mode=""):
        if mode != "":
            # Clear items in the sizer
            for child in self.boxBtmSizer.GetChildren():
                self.boxBtmSizer.Detach(child.Window)
                self.boxBtmSizer.Layout()
        if mode == "location":
            self.cBtn1.Hide()
            self.cBtn2.Hide()
            self.cBtn3.Hide()
            self.cBtn4.Hide()
            self.cBtn5.Show()
            self.cBtn6.Show()
            self.cBtn7.Show()
            self.boxBtmSizer.Add(self.charTl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.boxBtmSizer.Add(self.cBtn5, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.boxBtmSizer.Add(self.cBtn6, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.boxBtmSizer.Add(self.cBtn7, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        else:
            self.cBtn1.Show()
            self.cBtn2.Show()
            self.cBtn3.Show()
            self.cBtn4.Show()
            self.cBtn5.Hide()
            self.cBtn6.Hide()
            self.cBtn7.Hide()
            self.boxBtmSizer.Add(self.charTl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.boxBtmSizer.Add(self.cBtn1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.boxBtmSizer.Add(self.cBtn2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.boxBtmSizer.Add(self.cBtn3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.boxBtmSizer.Add(self.cBtn4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        if mode != "":
            # Update the layout
            self.boxBtmSizer.Layout()

    def onFileOpen(self, event):
        # Ask the user what new file to open
        with wx.FileDialog(self, "Open XYZ file", wildcard="CSV files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                filepath = str(pathname)
                #data = importData.importData(filepath)
                importData.performImport(filepath)
            except IOError:
                wx.LogError("Cannot open file")
            else:
                wx.MessageBox("Dataset import success!")
                # Build main content structure
                self.buidMain()
    
    def importBox(self): # Not using this
        #Dataset import
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

    def onAnalyse(self, event):
        self.mode = "main"
        self.setBoxBtmSizer(self.mode)

    def onAlcohol(self, event):
        self.mode = "alcohol"
        self.setBoxBtmSizer(self.mode)

    def onLocation(self, event):
        self.mode = "location"
        self.setBoxBtmSizer(self.mode)
    
    def onSearch(self, event):
        self.search.From_Date = self.dateFrCt.GetValue().Format("%Y-%m-%d")
        self.search.To_Date = self.dateToCt.GetValue().Format("%Y-%m-%d")
        self.search.Accident_Type_Keyword = self.accKyCt.GetValue()
        if self.accCh.GetCurrentSelection() == 0: # If all is selected
            self.search.Accident_Type_List = None
        else:
            self.search.Accident_Type_List = self.accidentTypes[(self.accCh.GetCurrentSelection())]
        #print(self.search)
        self.resultDb = self.search.getResult()
        self.updateGrid()
    
    def onChart(self, event):
        type = event.GetEventObject().GetLabel()
        title = 'Chart {}'.format(self.frame_number)
        frame = ChartFrame(title=title, search=self.search, chartType=type, mode=self.mode)
        self.frame_number += 1
    
    def onMap(self, event):
        x = [ i[6] for i in self.rows if i[10]==1]
        y = [i[7] for i in self.rows if i[10]==1]

        x1 = [ i[6] for i in self.rows if i[11]==1]
        y1 = [i[7] for i in self.rows if i[11]==1]

        x2 = [ i[6] for i in self.rows if i[12]==1]
        y2 = [i[7] for i in self.rows if i[12]==1]

        
        fig, ax = plt.subplots()
        left = 140.95260170441142
        right = 150.061662159373
        bottom = -39.12502305202676
        top = -33.992432778690606
        plt.xlim([left, right])
        plt.ylim([bottom, top])
        datafile = 'images/vicmap.png'
        img = plt.imread(datafile)
        plt.imshow(img, zorder=0,extent=[left, right, bottom, top])
        ax.scatter(x, y, zorder=1, s=5, c='red', alpha=0.4, edgecolors='none', label='Fatality',)
        ax.scatter(x1, y1, zorder=1, s=5, c='green', alpha=0.4, edgecolors='none', label='Injury',)
        ax.scatter(x2, y2, zorder=1, s=5, c='blue', alpha=0.4, edgecolors='none', label='Alcohol related',)
        
        ax.legend()
        #ax.grid(True)
        plt.show()

    def makeMenuBar(self):
        """
        A menu bar is composed of menus.
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
        # Make the menu bar and add items
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)
        # Bind actions to menu items
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

# class ChartFrame(wx.Frame):
#     """Class for chart frame window"""
#     def __init__(self, title, parent=None):
#         wx.Frame.__init__(self, parent=parent, title=title, size=(1000,625))

#         # create a panel in the frame
#         pnl = wx.Panel(self)
#         self.SetBackgroundColour("white")

#         # bar box
#         box = wx.StaticBox(pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, 40))
#         box.SetBackgroundColour("black")
#         # Create items
#         charTl = wx.StaticText(box, label="Chart ")
#         charTl.SetForegroundColour("white")
#         # Sizer
#         sizer = wx.BoxSizer(wx.HORIZONTAL)
#         sizer.Add(charTl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
#         box.SetSizer(sizer)

#         # Main
#         main = wx.StaticBox(pnl, wx.ID_ANY, "", pos =(0, 0), size =(-1, -1))
#         text = wx.StaticText(main, label="Chart will be inserted")
#         # Sizer
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
#         main.SetSizer(sizer)

#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
#         sizer.Add(main, 5, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER | wx.EXPAND, 0)
#         pnl.SetSizer(sizer)

#         self.Show()

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frame = MainFrame(None, title=APP_NAME, size=(1280,800))
    frame.Show()
    app.MainLoop()