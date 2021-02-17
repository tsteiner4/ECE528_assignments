"""
Reference
https://zetcode.com/wxpython/
"""

import wx
# import images
from InfoPopupMenu import InfoPopupMenu
from EventPanel import EventPanel
from CreateNewEvent import CreateNewEvent
from ListbookWidget import ListbookWidget, TabPanel
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
        # self.panel_one = TabPanel(self)
        # self.panel_two = CreateNewEvent(self)
        # self.panel_two.Hide()
        #
        # vbox = wx.BoxSizer(wx.VERTICAL)
        # vbox.Add(self.panel_one, 1, wx.EXPAND)
        # vbox.Add(self.panel_two, 1, wx.EXPAND)
        #
        # # vbox.Add(-1, 25)
        # hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # closeButton = wx.Button(self, label='Close', pos=(20, 20))
        # hbox1.Add(closeButton)
        # vbox.Add(hbox1)
        # closeButton.Bind(wx.EVT_BUTTON, self.OnSwitch)


        panelOne = TabPanel(self)
        panelTwo = CreateNewEvent(self)
        panelThree = TabPanel(self)
        # self.lb = wx.Listbook(self.panel)
        self.lb = wx.Listbook(self, wx.ID_ANY, style=
        # wx.BK_DEFAULT
                             # wx.BK_TOP
                             wx.BK_BOTTOM
                             # wx.BK_LEFT
                             # wx.BK_RIGHT
                             )
        pages = [(panelOne, "Calendar List"),
                 (panelTwo, "Calendar"),
                 (panelThree, "Events")]
        for page, label in pages:
            self.lb.AddPage(page, label)

        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGING, self.OnPageChanging)

        hbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.lb, 1, wx.EXPAND)
        vbox.Add(hbox1)
        #
        # hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # # put some text with a larger bold font on it
        # st = wx.StaticText(self.panel, label="Google Calendar API")
        # font = st.GetFont()
        # font.PointSize += 10
        # font = font.Bold()
        # st.SetFont(font)
        # hbox1.Add(st, 1, wx.EXPAND)
        # tc = wx.TextCtrl(self.panel)
        # hbox1.Add(tc, proportion=1)
        # vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        # vbox.Add((-1, 25))

        # self.panel_one = wx.Panel(self)
        # self.panel_two = CreateNewEvent(self)
        # self.panel_two.Hide()
        #
        # self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        # self.sizer.Add(self.panel_two, 1, wx.EXPAND)

        # and create a sizer to manage the layout of child widgets
        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        #
        # hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # notebook = ListbookWidget(self.panel)
        # hbox2.Add(notebook, 1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        # vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # closeButton = wx.Button(self.panel, label='Close', pos=(20, 20))
        #
        # closeButton.Bind(wx.EVT_BUTTON, self.OnSwitch)



        # Make right click give info on API
        # self.panel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        #
        # self.Bind(wx.EVT_CLOSE, self.OnExit)

        self.SetSizer(vbox)
        self.Layout()

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Destroy()
        # dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
        #     wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        #
        # ret = dial.ShowModal()
        #
        # if ret == wx.ID_YES:
        #     self.Destroy()
        # else:
        #     event.Veto()

    def OnSwitch(self, event):
        """"""
        # if self.panel_one.IsShown():
        #     self.SetTitle("Panel Two Showing")
        #     self.panel_one.Hide()
        #     self.panel_two.Show()
        # else:
        #     self.SetTitle("Panel One Showing")
        #     self.panel_one.Show()
        #     self.panel_two.Hide()
        # self.Layout()

    def OnRightDown(self, e):
        self.panel.PopupMenu(InfoPopupMenu(self), e.GetPosition())

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)
# ----------------------------------------------------------------------
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.lb.GetSelection()
        # print('OnPageChanged, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    # ----------------------------------------------------------------------
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.lb.GetSelection()
        # print('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()