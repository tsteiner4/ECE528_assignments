import wx

class EventInfoDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(EventInfoDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((400, 400))


    def InitUI(self):
        self.SetTitle("Event Info")

        sizer = wx.GridBagSizer(15, 5)
        self.panel = wx.Panel(self, wx.ID_ANY)

        self.text1 = wx.StaticText(self.panel, label="Summary")
        sizer.Add(self.text1, pos=(0, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.summary_text = wx.TextCtrl(self.panel)
        sizer.Add(self.summary_text, pos=(0, 1), span=(3, 15), flag=wx.TOP | wx.EXPAND, border=10)

        text3 = wx.StaticText(self.panel, label="Start Date")
        sizer.Add(text3, pos=(3, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.start_date = wx.TextCtrl(self.panel)
        sizer.Add(self.start_date, pos=(3, 1), span=(1, 15), flag=wx.TOP | wx.EXPAND, border=10)

        text5 = wx.StaticText(self.panel, label="Start Time")
        sizer.Add(text5, pos=(4, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.start_time = wx.TextCtrl(self.panel)
        sizer.Add(self.start_time, pos=(4, 1), span=(1, 15), flag=wx.TOP | wx.EXPAND, border=10)

        text3 = wx.StaticText(self.panel, label="End Date")
        sizer.Add(text3, pos=(5, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.end_date = wx.TextCtrl(self.panel)
        sizer.Add(self.end_date, pos=(5, 1), span=(1, 15), flag=wx.TOP | wx.EXPAND,
                  border=10)
        text6 = wx.StaticText(self.panel, label="End Time")
        sizer.Add(text6, pos=(6, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.end_time = wx.TextCtrl(self.panel)
        sizer.Add(self.end_time, pos=(6, 1), span=(1, 15), flag=wx.TOP | wx.EXPAND, border=10)

        text2 = wx.StaticText(self.panel, label="Recurring?")
        sizer.Add(text2, pos=(7, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.recurring = wx.TextCtrl(self.panel)
        sizer.Add(self.recurring, pos=(7, 1), span=(1, 15), flag=wx.TOP | wx.EXPAND,
                  border=10)

        text2 = wx.StaticText(self.panel, label="Reminder?")
        sizer.Add(text2, pos=(8, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.reminder = wx.TextCtrl(self.panel)
        sizer.Add(self.reminder, pos=(8, 1), span=(1, 15), flag=wx.TOP | wx.EXPAND,
                  border=10)

        self.panel.SetSizer(sizer)
        # sizer.Fit(self)

    def OnClose(self, e):

        self.Destroy()
