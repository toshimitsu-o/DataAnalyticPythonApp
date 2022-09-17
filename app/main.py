"""
Accident Analysis
"""

try:
    import wx
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

        

        # button for Dataset
        btn1 = wx.Button(pnl, label="Dataset")
        self.Bind(wx.EVT_BUTTON, self.onDataset, btn1)
        #  button for Analyse
        btn2 = wx.Button(pnl, label="Analyse")
        self.Bind(wx.EVT_BUTTON, self.onAnalyse, btn2)
        #  button for Analyse
        btn3 = wx.Button(pnl, label="Alcohol")
        self.Bind(wx.EVT_BUTTON, self.onAlcohol, btn3)
        #  button for Location
        btn4 = wx.Button(pnl, label="Location")
        self.Bind(wx.EVT_BUTTON, self.onLocation, btn4)


        box = wx.StaticBox(pnl, wx.ID_ANY, "", pos =(0, 0), size =(780, 450))
        # put some text with a larger bold font on it
        st = wx.StaticText(box, label="Main Box")

        boxBtm = wx.StaticBox(pnl, wx.ID_ANY, "", pos =(0, 0), size =(780, 50))
        # put some text with a larger bold font on it
        st = wx.StaticText(boxBtm, label="Bottom Box")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)
        # and create a sizer to manage the layout of child widgets
        sizer = wx.GridBagSizer(hgap=2, vgap=1)
        sizer.Add(btn1, pos=(0,0), flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        sizer.Add(btn2, pos=(0,1), flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        sizer.Add(btn3, pos=(0,2), flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        sizer.Add(btn4, pos=(0,3), flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        sizer.Add(box, pos=(1,0), span=(0,4), flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        sizer.Add(boxBtm, pos=(2,0), span=(0,4), flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        pnl.SetSizerAndFit(sizer)
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