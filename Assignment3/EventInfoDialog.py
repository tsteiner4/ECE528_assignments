import wx

class EventInfoDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(EventInfoDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((500, 500))
        self.Centre()


    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridBagSizer(0, 0)
        self.panel = wx.Panel(self, wx.ID_ANY)

        text1 = wx.StaticText(self.panel, label="Summary")
        sizer.Add(text1, pos=(0, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.summary_text = wx.TextCtrl(self.panel)
        sizer.Add(self.summary_text, pos=(0, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND, border=10)

        text3 = wx.StaticText(self.panel, label="Start Date")
        sizer.Add(text3, pos=(1, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.start_date = wx.TextCtrl(self.panel)
        sizer.Add(self.start_date, pos=(1, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND, border=10)

        text5 = wx.StaticText(self.panel, label="Start Time")
        sizer.Add(text5, pos=(2, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.start_time = wx.TextCtrl(self.panel)
        sizer.Add(self.start_time, pos=(2, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND, border=10)

        text3 = wx.StaticText(self.panel, label="End Date")
        sizer.Add(text3, pos=(3, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.end_date = wx.TextCtrl(self.panel)
        sizer.Add(self.end_date, pos=(3, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND,
                  border=10)
        text6 = wx.StaticText(self.panel, label="End Time")
        sizer.Add(text6, pos=(4, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.end_time = wx.TextCtrl(self.panel)
        sizer.Add(self.end_time, pos=(4, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND, border=10)

        text2 = wx.StaticText(self.panel, label="Recurring?")
        sizer.Add(text2, pos=(5, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.recurring = wx.TextCtrl(self.panel)
        sizer.Add(self.recurring, pos=(5, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND,
                  border=10)

        text2 = wx.StaticText(self.panel, label="Reminder?")
        sizer.Add(text2, pos=(6, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.reminder = wx.TextCtrl(self.panel)
        sizer.Add(self.reminder, pos=(6, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND,
                  border=10)
        text7 = wx.StaticText(self.panel, label="Location")
        sizer.Add(text7, pos=(7, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.location = wx.TextCtrl(self.panel)
        sizer.Add(self.location, pos=(7, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND,
                  border=10)
        text8 = wx.StaticText(self.panel, label="Description")
        sizer.Add(text8, pos=(8, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.desc = wx.TextCtrl(self.panel)
        sizer.Add(self.desc, pos=(8, 1), span=(3, 1), flag=wx.ALL | wx.EXPAND,
                  border=10)

        self.btn1 = wx.Button(self.panel, wx.ID_ANY, "OK")
        sizer.Add(self.btn1, pos=(11, 0), flag=wx.ALL, border=10)
        self.btn1.Bind(wx.EVT_BUTTON, self.OnOK)
        # self.CreateStdDialogButtonSizer(self.panel, flags=wx.OK | wx.CANCEL)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(8)
        # vbox.Add(sizer, flag= wx.ALL, border=10)
        self.panel.SetSizer(sizer)
        sizer.Fit(self)

    def OnClose(self, e):
        self.Destroy()
    #
    def OnOK(self, e):
        self.EndModal(wx.ID_OK)
        self.Destroy()
