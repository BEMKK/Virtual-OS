import wx
from virtual_os.apps.base_app import BaseAppWindow
from virtual_os.core.config import system_config

class RecycleBinApp(BaseAppWindow):
    def __init__(self, parent, window_manager=None):
        super().__init__(parent, title="Lomtár", size=(500, 350), window_manager=window_manager)
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list_ctrl.InsertColumn(0, "Név", width=200)
        self.list_ctrl.InsertColumn(1, "Eredeti hely", width=200)
        
        btn_empty = wx.Button(panel, label="Lomtár ürítése")
        btn_empty.Bind(wx.EVT_BUTTON, self.on_empty)
        
        sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_empty, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        panel.SetSizer(sizer)
        
        self.refresh_list()

    def refresh_list(self):
        self.list_ctrl.DeleteAllItems()
        for idx, item in enumerate(system_config.recycle_bin):
            self.list_ctrl.InsertItem(idx, item["name"])
            self.list_ctrl.SetItem(idx, 1, item["path"])

    def on_empty(self, event):
        system_config.empty_trash()
        self.refresh_list()