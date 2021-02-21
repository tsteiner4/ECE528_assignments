import glob

import wx
import utils
from datetime import datetime
from APIInfoDialog import APIInfoDialog
from EventInfoDialog import EventInfoDialog

""" https://realpython.com/python-gui-with-wxpython/ for reference """
class EventPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.index = 0
        self.event_ids = []
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Summary')
        self.list.InsertColumn(1, 'Start Date')
        self.list.InsertColumn(2, 'Time')
        hbox.Add(self.list, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

        btnPanel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        updateBtn = wx.Button(btnPanel, wx.ID_ANY, 'Update Events', size=(90, 30))
        updateBtn.name = "Event List"
        infoBtn = wx.Button(btnPanel, wx.ID_ANY, 'Event Info', size=(90, 30))
        infoBtn.name = "Event Get"
        delBtn = wx.Button(btnPanel, wx.ID_ANY, 'Delete', size=(90, 30))
        delBtn.name = "Event Delete"
        addBtn = wx.Button(btnPanel, wx.ID_ANY, 'Add', size=(90, 30))
        addBtn.name = "Event Insert"

        updateBtn.Bind(wx.EVT_RIGHT_DOWN, self.APIInfo)
        infoBtn.Bind(wx.EVT_RIGHT_DOWN, self.APIInfo)
        addBtn.Bind(wx.EVT_RIGHT_DOWN, self.APIInfo)
        delBtn.Bind(wx.EVT_RIGHT_DOWN, self.APIInfo)

        self.Bind(wx.EVT_BUTTON, self.OnUpdate, id=updateBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnInfo, id=infoBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=addBtn.GetId())
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnInfo)

        vbox.Add((-1, 20))
        vbox.Add(updateBtn)
        vbox.Add(infoBtn, 0, wx.TOP, 5)
        vbox.Add(addBtn, 0, wx.TOP, 5)
        vbox.Add(delBtn, 0, wx.TOP, 5)

        btnPanel.SetSizer(vbox)
        hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        self.SetSizer(hbox)

    def OnUpdate(self, event):
        self.list.ClearAll()
        self.list.InsertColumn(0, 'Summary', width=self.list.GetSize()[0]/3)
        self.list.InsertColumn(1, 'Start Date', width=self.list.GetSize()[0]/3)
        self.list.InsertColumn(2, 'Time', width=self.list.GetSize()[0]/3)
        events = utils.get_calendar_events(10)
        self.event_ids.clear()
        for e in events:
            self.event_ids.append(e)
            if 'date' in e['start'].keys():
                start = e['start']['date']
                time = "None"
            else:
                start = e['start']['dateTime']
                start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
                time = datetime.strftime(start, '%H:%M:%S')
                start = datetime.strftime(start, '%Y-%m-%d')

            self.list.Append((e['summary'], start, time))

    def OnInfo(self, event):
        sel = self.list.GetFirstSelected()
        if sel < 0:
            warn = wx.MessageDialog(None, message='Must select an event!', caption='Event Info Warning')
            warn.ShowModal()
            warn.Destroy()
        else:
            e = utils.get_event_info(self.event_ids[sel]['id'])
            renamed = EventInfoDialog(None, title='API Info')
            renamed.summary_text.SetLabelText(e['summary'])
            if 'date' in e['start'].keys():
                start = e['start']['date']
                stime = "None"
            else:
                start = e['start']['dateTime']
                start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
                stime = datetime.strftime(start, '%H:%M:%S')
                start = datetime.strftime(start, '%Y-%m-%d')

            if 'date' in e['end'].keys():
                end = e['end']['date']
                etime = "None"
            else:
                end = e['end']['dateTime']
                end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
                etime = datetime.strftime(end, '%H:%M:%S')
                end = datetime.strftime(end, '%Y-%m-%d')
            renamed.start_date.SetLabelText(start)
            renamed.start_time.SetLabelText(stime)
            renamed.end_date.SetLabelText(end)
            renamed.end_time.SetLabelText(etime)
            if 'reccuringEventId' in e.keys():
                renamed.recurring.SetLabelText('True')
            else:
                renamed.recurring.SetLabelText('False')

            if e['reminders']['useDefault']:
                renamed.reminder.SetLabelText('True')
            else:
                renamed.reminder.SetLabelText('False')
            renamed.ShowModal()
            renamed.Destroy()


    def OnDelete(self, event):

        sel = self.list.GetSelection()
        if sel != -1:
            self.list.Delete(sel)

    def OnClear(self, event):
        self.list.ClearAll()

    def APIInfo(self, event):
        http, py = utils.APILookup(event.GetEventObject().name)
        dial = APIInfoDialog(None, title='API Info')
        dial.setEvent(http, py)
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