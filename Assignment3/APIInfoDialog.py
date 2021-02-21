import wx

class APIInfoDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(APIInfoDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((400, 400))


    def InitUI(self):
        self.SetTitle("API Call Information")

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self, wx.ID_ANY)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='HTTP Info:')
        hbox1.Add(st1, flag=wx.RIGHT, border=8)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.http_info = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        hbox4.Add(self.http_info, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox4, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT , border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self.panel, label='Python Code:')
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.api_info = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        hbox3.Add(self.api_info, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND,
                 border=10)

        vbox.Add((-1, 25))

        self.panel.SetSizer(vbox)

    def OnClose(self, e):

        self.Destroy()

    def setEvent(self, http, py):
        self.http_info.AppendText(http)
        s = ''
        for elm in py:
            s = s + elm + '\n' + '\n'

        self.api_info.AppendText(s)
        self.panel.Layout()

