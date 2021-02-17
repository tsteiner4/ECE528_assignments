"""
ZetCode wxPython tutorial

In this example we create a new class layout
with wx.GridBagSizer.

author: Jan Bodnar
website: www.zetcode.com
last modified: July 2020
"""
from utils import *
import wx

class CalendarListPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        self.InitUI()
        self.Centre()

    def InitUI(self):

        sizer = wx.GridBagSizer(5, 5)

        text1 = wx.StaticText(self, label="Java Class")
        sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM,
            border=15)

        # icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('exec.png'))
        # sizer.Add(icon, pos=(0, 4), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT,
        #     border=5)

        line = wx.StaticLine(self)
        sizer.Add(line, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        text2 = wx.StaticText(self, label="Name")
        sizer.Add(text2, pos=(2, 0), flag=wx.LEFT, border=10)

        tc1 = wx.TextCtrl(self)
        sizer.Add(tc1, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND)

        text3 = wx.StaticText(self, label="Package")
        sizer.Add(text3, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

        tc2 = wx.TextCtrl(self)
        sizer.Add(tc2, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND,
            border=5)

        button1 = wx.Button(self, label="Browse...")
        sizer.Add(button1, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)

        text4 = wx.StaticText(self, label="Extends")
        sizer.Add(text4, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)

        combo = wx.ComboBox(self)
        sizer.Add(combo, pos=(4, 1), span=(1, 3),
            flag=wx.TOP|wx.EXPAND, border=5)

        button2 = wx.Button(self, label="Browse...")
        sizer.Add(button2, pos=(4, 4), flag=wx.TOP|wx.RIGHT, border=5)

        sb = wx.StaticBox(self, label="Optional Attributes")

        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        boxsizer.Add(wx.CheckBox(self, label="Public"),
            flag=wx.LEFT|wx.TOP, border=5)
        boxsizer.Add(wx.CheckBox(self, label="Generate Default Constructor"),
            flag=wx.LEFT, border=5)
        boxsizer.Add(wx.CheckBox(self, label="Generate Main Method"),
            flag=wx.LEFT|wx.BOTTOM, border=5)
        sizer.Add(boxsizer, pos=(5, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

        button3 = wx.Button(self, label='Help')
        sizer.Add(button3, pos=(7, 0), flag=wx.LEFT, border=10)

        button4 = wx.Button(self, label="Ok")
        button4.Bind(wx.EVT_BUTTON, self.onOKButton)
        sizer.Add(button4, pos=(7, 3))

        button5 = wx.Button(self, label="Cancel")
        sizer.Add(button5, pos=(7, 4), span=(1, 1),
            flag=wx.BOTTOM|wx.RIGHT, border=10)

        sizer.AddGrowableCol(2)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def onOKButton(self, e):
        event = create_event_from_data(summary="", location="", description="", start=datetime.datetime.utcnow().isoformat(),
                               timeZone="America/Chicago", end=datetime.datetime.utcnow().isoformat(), recurrRule=[],
                               attendees=[], defaultReminder=False, reminderOverrides=[])
        print(event)