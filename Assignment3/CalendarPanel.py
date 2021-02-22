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
import wx
import utils
from APIInfoDialog import APIInfoDialog
from CalendarInfoDialog import CalendarInfoDialog

class CalendarPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.index = 0
        self.cal_ids = []
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Summary')
        self.list.InsertColumn(1, 'Time Zone')
        self.list.InsertColumn(2, 'Access Role')
        hbox.Add(self.list, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

        btnPanel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        updateBtn = wx.Button(btnPanel, wx.ID_ANY, 'Calendar List', size=(90, 30))
        updateBtn.name = "Calendar List"
        infoBtn = wx.Button(btnPanel, wx.ID_ANY, 'Calendar Info', size=(90, 30))
        infoBtn.name = "Calendar Get"
        delBtn = wx.Button(btnPanel, wx.ID_ANY, 'Delete Calendar', size=(90, 30))
        delBtn.name = "Calendar Delete"
        addBtn = wx.Button(btnPanel, wx.ID_ANY, 'Add Calendar', size=(90, 30))
        addBtn.name = "Calendar Insert"

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
        self.list.InsertColumn(1, 'Time Zone', width=self.list.GetSize()[0]/3)
        self.list.InsertColumn(2, 'Access Role', width=self.list.GetSize()[0] / 3)
        cals = utils.get_calendar_list(10)
        self.cal_ids.clear()
        for c in cals:
            self.cal_ids.append(c)
            self.list.Append((c['summary'], c['timeZone'], c['accessRole']))

    def OnInfo(self, event):
        sel = self.list.GetFirstSelected()
        if sel < 0:
            warn = wx.MessageDialog(None, message='Must select an event!', caption='Event Info Warning')
            warn.ShowModal()
            warn.Destroy()
        else:
            c = utils.get_calendar_info(self.cal_ids[sel]['id'])
            info = CalendarInfoDialog(None, title='Calendar Info')
            info.summary_text.SetLabelText(c['summary'])
            if 'timeZone' in c.keys():
                info.time_zone.SetLabelText(c['timeZone'])

            if 'location' in c.keys():
                info.location.SetLabelText(c['location'])

            if 'description' in c.keys():
                info.desc.SetLabelText(c['description'])

            info.ShowModal()
            info.Destroy()


    def OnDelete(self, event):
        sel = self.list.GetFirstSelected()
        if sel != -1 and self.cal_ids[sel]['id'] != utils.get_primary_calendar_id():
            utils.delete_calendar(self.cal_ids[sel]['id'])
            self.OnUpdate(None)

    def OnAdd(self, event):
        addDial = CalendarInfoDialog(None, title='Add calendar')
        if addDial.ShowModal() == wx.ID_OK:
            summary = addDial.summary_text.GetLineText(0)
            time_zone = addDial.time_zone.GetLineText(0)
            location = addDial.location.GetLineText(0)
            desc = addDial.desc.GetLineText(0)
            created_cal = utils.create_calendar(summary=summary, timeZone=time_zone, location=location, description=desc)

            success, err = utils.add_calendar(created_cal)
            if not success:
                warn = wx.MessageDialog(None, message=str(err), caption='Add Calendar Warning')
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
