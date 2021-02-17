import glob
import wx
import utils

""" https://realpython.com/python-gui-with-wxpython/ for reference """
class EventPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.listbox = wx.ListBox(self)
        hbox.Add(self.listbox, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

        btnPanel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        newBtn = wx.Button(btnPanel, wx.ID_ANY, 'New', size=(90, 30))
        renBtn = wx.Button(btnPanel, wx.ID_ANY, 'Rename', size=(90, 30))
        delBtn = wx.Button(btnPanel, wx.ID_ANY, 'Delete', size=(90, 30))
        clrBtn = wx.Button(btnPanel, wx.ID_ANY, 'Clear', size=(90, 30))

        newBtn.Bind(wx.EVT_RIGHT_DOWN, self.GetInfo)

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=newBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnRename, id=renBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=clrBtn.GetId())
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename)

        vbox.Add((-1, 20))
        vbox.Add(newBtn)
        vbox.Add(renBtn, 0, wx.TOP, 5)
        vbox.Add(delBtn, 0, wx.TOP, 5)
        vbox.Add(clrBtn, 0, wx.TOP, 5)

        btnPanel.SetSizer(vbox)
        hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        self.SetSizer(hbox)

    def NewItem(self, event):
        events = utils.get_calendar_events(10)
        for e in events:
            start = e['start'].get('dateTime', e['start'].get('date'))
            self.listbox.Append(start + " " + e['summary'])

    def OnRename(self, event):

        sel = self.listbox.GetSelection()
        text = self.listbox.GetString(sel)
        renamed = wx.GetTextFromUser('Rename item', 'Rename dialog', text)

        if renamed != '':
            self.listbox.Delete(sel)
            item_id = self.listbox.Insert(renamed, sel)
            self.listbox.SetSelection(item_id)

    def OnDelete(self, event):

        sel = self.listbox.GetSelection()
        if sel != -1:
            self.listbox.Delete(sel)

    def OnClear(self, event):
        self.listbox.Clear()

    def GetInfo(self, event):
        wx.GetTextFromUser('Rename item', 'Rename dialog')

    """
    To get name from button ->
    b = wx.Button(self, 10, "Default Button", (20, 20))
    b.myname = "default button"
    self.Bind(wx.EVT_BUTTON, self.OnClick, b)
    def OnClick(self, event):
        name = event.GetEventObject().myname
    """