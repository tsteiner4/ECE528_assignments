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
        self.sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.btns = 1

        label_1 = wx.StaticText(self, wx.ID_ANY, "Title")
        label_1.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.button_1 = wx.Button(self, wx.ID_ANY, "button_1")
        self.sizer_1.Add(self.button_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.sizer_2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_1.Add(self.sizer_2, 1, wx.EXPAND, 0)

        self.sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_2.Add(self.sizer_3, 1, wx.EXPAND, 0)

        self.button_3 = wx.Button(self, wx.ID_ANY, "button_3")
        self.button_3.Bind(wx.EVT_BUTTON, self.add_button)
        self.sizer_3.Add(self.button_3, 0, wx.EXPAND, 0)

        # self.button_4 = wx.Button(self, wx.ID_ANY, "button_4")
        # sizer_3.Add(self.button_4, 0, wx.EXPAND, 0)

        self.button_2 = wx.Button(self, wx.ID_ANY, "button_2")
        self.sizer_1.Add(self.button_2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.SetSizer(self.sizer_1)

        self.Layout()

    def onOKButton(self, e):
        event = create_event_from_data(summary="", location="", description="", start=datetime.datetime.utcnow().isoformat(),
                               timeZone="America/Chicago", end=datetime.datetime.utcnow().isoformat(), recurrRule=[],
                               attendees=[], defaultReminder=False, reminderOverrides=[])
        print(event)

    #----------------------------------------------------------------------
    def add_button(self, event):
        """"""
        new_btn = wx.Button(self, label="Remove %s" % self.btns)
        new_btn.Bind(wx.EVT_BUTTON, self.remove_button)
        self.btns += 1
        self.sizer_3.Add(new_btn, 0, wx.CENTER|wx.ALL, 5)
        self.sizer_3.Layout()

    #----------------------------------------------------------------------
    def remove_button(self, event):
        """"""
        btn = event.GetEventObject()
        self.sizer_3.Hide(btn)
        btn.Destroy()
        self.sizer_3.Layout()