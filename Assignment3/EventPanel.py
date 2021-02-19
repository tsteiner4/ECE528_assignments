import glob

import wx
import utils
from datetime import datetime
from EventInfoDialog import EventInfoDialog

""" https://realpython.com/python-gui-with-wxpython/ for reference """
class EventPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.index = 0
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Summary')
        self.list.InsertColumn(1, 'Start Date')
        self.list.InsertColumn(2, 'Time')
        hbox.Add(self.list, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

        btnPanel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        updateBtn = wx.Button(btnPanel, wx.ID_ANY, 'Update Events', size=(90, 30))
        infoBtn = wx.Button(btnPanel, wx.ID_ANY, 'Event Info', size=(90, 30))
        delBtn = wx.Button(btnPanel, wx.ID_ANY, 'Delete', size=(90, 30))
        clrBtn = wx.Button(btnPanel, wx.ID_ANY, 'Clear', size=(90, 30))

        updateBtn.Bind(wx.EVT_RIGHT_DOWN, self.APIInfo)

        self.Bind(wx.EVT_BUTTON, self.OnUpdate, id=updateBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnInfo, id=infoBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=clrBtn.GetId())
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnInfo)

        vbox.Add((-1, 20))
        vbox.Add(updateBtn)
        vbox.Add(infoBtn, 0, wx.TOP, 5)
        vbox.Add(delBtn, 0, wx.TOP, 5)
        vbox.Add(clrBtn, 0, wx.TOP, 5)

        btnPanel.SetSizer(vbox)
        hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        self.SetSizer(hbox)

    def OnUpdate(self, event):
        self.list.ClearAll()
        self.list.InsertColumn(0, 'Summary', width=self.list.GetSize()[0]/3)
        self.list.InsertColumn(1, 'Start Date', width=self.list.GetSize()[0]/3)
        self.list.InsertColumn(2, 'Time', width=self.list.GetSize()[0]/3)
        events = utils.get_calendar_events(10)
        for e in events:
            if 'date' in e['start'].keys():
                start = e['start']['date']
                time = "None"
            else:
                start = e['start']['dateTime']
                start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
                time = datetime.strftime(start, '%H:%M:%S')
                start = datetime.strftime(start, '%Y-%m-%d')

            self.list.Append((e['summary'], start, time))
            # ind = self.list.InsertItem(self.index, e['summary'])
            # self.list.SetStringItem(ind, 1, start)
            # self.list.SetStringItem(ind, 2, time)
            # self.index += 1

    def OnInfo(self, event):
        sel = self.list.GetFirstSelected()
        text = self.list.GetItemText(sel, 0)
        renamed = wx.GetTextFromUser('Rename item', 'Rename dialog', text)

        if renamed != '':
            self.list.Delete(sel)
            item_id = self.list.Insert(renamed, sel)
            self.list.SetSelection(item_id)

    def OnDelete(self, event):

        sel = self.list.GetSelection()
        if sel != -1:
            self.list.Delete(sel)

    def OnClear(self, event):
        self.list.ClearAll()

    def APIInfo(self, event):
        dial = EventInfoDialog(None, title='API Info')
        dial.setEvent(self.list.GetItemText(self.list.GetFirstSelected(), 0))
        dial.ShowModal()
        dial.Destroy()

    """
    To get name from button ->
    b = wx.Button(self, 10, "Default Button", (20, 20))
    b.myname = "default button"
    self.Bind(wx.EVT_BUTTON, self.OnClick, b)
    def OnClick(self, event):
        name = event.GetEventObject().myname
    """