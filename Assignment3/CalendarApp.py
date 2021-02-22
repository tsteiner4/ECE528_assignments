"""
Reference
https://zetcode.com/wxpython/
"""

import wx
from EventPanel import EventPanel
from CalendarPanel import CalendarPanel

import utils

class MainFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.Centre()
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnExit, fileItem)

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Ready")

        # create a panel in the frame
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # create the pages for list, calendar and events
        panelTwo = CalendarPanel(self)
        panelThree = EventPanel(self)
        self.lb = wx.Listbook(self, wx.ID_ANY, style=wx.BK_BOTTOM)
        pages = [(panelTwo, "Calendar"),
                 (panelThree, "Events")]
        for page, label in pages:
            self.lb.AddPage(page, label)

        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGING, self.OnPageChanging)

        hbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.lb, 1, wx.EXPAND)
        vbox.Add(hbox1)

        self.SetSizer(vbox)
        self.Layout()

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Destroy()

# ----------------------------------------------------------------------
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.lb.GetSelection()
        self.SetTitle(self.lb.GetPageText(self.lb.GetSelection()))
        # print('OnPageChanged, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    # ----------------------------------------------------------------------
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.lb.GetSelection()
        # print('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()