# from __future__ import print_function
# import datetime
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from CalendarApp import *
#
# # If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
import utils
import wx
from CalendarApp import *


service = None

if __name__ == '__main__':
    utils.auth_setup()
    # utils.get_calendar_events()
    app = wx.App()
    frm = MainFrame(None, title='Calendar List', size=(500, 500))
    frm.Show()
    app.MainLoop()
