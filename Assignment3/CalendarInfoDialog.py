import wx

class CalendarInfoDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(CalendarInfoDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((500, 500))
        self.Centre()


    def InitUI(self):
        sizer = wx.GridBagSizer(0, 0)
        self.panel = wx.Panel(self, wx.ID_ANY)

        text1 = wx.StaticText(self.panel, label="Summary")
        sizer.Add(text1, pos=(0, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.summary_text = wx.TextCtrl(self.panel)
        sizer.Add(self.summary_text, pos=(0, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND, border=10)

        text2 = wx.StaticText(self.panel, label="Time Zone")
        sizer.Add(text2, pos=(1, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.time_zone = wx.TextCtrl(self.panel)
        sizer.Add(self.time_zone, pos=(1, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND,
                  border=10)
        text7 = wx.StaticText(self.panel, label="Location")
        sizer.Add(text7, pos=(2, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.location = wx.TextCtrl(self.panel)
        sizer.Add(self.location, pos=(2, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND,
                  border=10)
        text8 = wx.StaticText(self.panel, label="Description")
        sizer.Add(text8, pos=(3, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.desc = wx.TextCtrl(self.panel)
        sizer.Add(self.desc, pos=(3, 1), span=(3, 1), flag=wx.ALL | wx.EXPAND,
                  border=10)

        self.btn1 = wx.Button(self.panel, wx.ID_ANY, "OK")
        sizer.Add(self.btn1, pos=(7, 0), flag=wx.ALL, border=10)
        self.btn1.Bind(wx.EVT_BUTTON, self.OnOK)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(3)

        self.panel.SetSizer(sizer)
        sizer.Fit(self)

    def OnClose(self, e):
        self.Destroy()
    #
    def OnOK(self, e):
        self.EndModal(wx.ID_OK)
        self.Destroy()
