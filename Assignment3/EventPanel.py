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
        self.Bind(wx.EVT_BUTTON, self.OnAdd, id=addBtn.GetId())
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
            renamed = EventInfoDialog(None, title='Event Info')
            renamed.summary_text.SetLabelText(e['summary'])
            if 'dateTime' in e['start'].keys():
                start = e['start']['dateTime']
                start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
                stime = datetime.strftime(start, '%H:%M:%S')
                start = datetime.strftime(start, '%Y-%m-%d')
            else:
                start = e['start']['date']
                stime = "None"

            if 'dateTime' in e['end'].keys():
                end = e['end']['dateTime']
                end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
                etime = datetime.strftime(end, '%H:%M:%S')
                end = datetime.strftime(end, '%Y-%m-%d')
            else:
                end = e['end']['date']
                etime = "None"

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

            if 'location' in e.keys():
                renamed.location.SetLabelText(e['location'])

            if 'description' in e.keys():
                renamed.desc.SetLabelText(e['description'])

            renamed.ShowModal()
            renamed.Destroy()


    def OnDelete(self, event):
        sel = self.list.GetFirstSelected()
        if sel != -1:
            print(self.event_ids[sel]['id'])
            utils.delete_event(self.event_ids[sel]['id'])
            self.OnUpdate(None)

    def OnAdd(self, event):
        addDial = EventInfoDialog(None, title='Add Event')
        if addDial.ShowModal() == wx.ID_OK:
            summary = addDial.summary_text.GetLineText(0)
            start_date = addDial.start_date.GetLineText(0)
            start_time = addDial.start_time.GetLineText(0)
            if start_time == '':
                start_datetime = ""
            else:
                start_datetime = datetime.strptime(start_date + " " + start_time, '%Y-%m-%d %H:%M:%S')
            end_date = addDial.end_date.GetLineText(0)
            end_time = addDial.end_time.GetLineText(0)
            if end_time == "":
                end_datetime = ""
            else:
                end_datetime = datetime.strptime(end_date + " " + end_time, '%Y-%m-%d %H:%M:%S')
            reminder = addDial.reminder.GetLineText(0)
            location = addDial.location.GetLineText(0)
            desc = addDial.desc.GetLineText(0)

            if start_time == "":
                created_event = utils.create_event_from_data(summary=summary, location=location, description=desc, start={'date': start_date},
                                             end={'date': end_date}, defaultReminder=reminder)
            else:
                created_event = utils.create_event_from_data(summary=summary, location=location, description=desc,
                                                             start={'dateTime': start_datetime},
                                                             end={'dateTime': end_datetime}, defaultReminder=reminder)
            success, err = utils.add_event(created_event)
            if not success:
                warn = wx.MessageDialog(None, message=str(err), caption='Add Event Warning')
                warn.ShowModal()
                warn.Destroy()
            else:
                addDial.Destroy()
                self.OnUpdate(None)

    def APIInfo(self, event):
        http, py = utils.APILookup(event.GetEventObject().name)
        dial = APIInfoDialog(None, title='API Info')
        dial.setEvent(http, py)
        dial.ShowModal()
        dial.Destroy()
