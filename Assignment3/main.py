
from CalendarApp import *


service = None

if __name__ == '__main__':
    utils.auth_setup()
    app = wx.App()
    frm = MainFrame(None, title='Calendar List', size=(500, 500))
    frm.Show()
    app.MainLoop()
