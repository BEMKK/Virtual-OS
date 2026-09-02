"""
Desktop panel component for Virtual OS.
"""
import wx

class DesktopPanel(wx.Panel):
    """Panel representing the desktop area with executable app icons."""
    def __init__(self, parent, open_app_callback=None):
        super().__init__(parent)
        self.open_app_callback = open_app_callback
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Asztal ikonok / lista
        self.desktop_list = wx.ListCtrl(self, style=wx.LC_ICON | wx.LC_SINGLE_SEL | wx.TAB_TRAVERSAL)
        self.desktop_list.SetName("Asztal")
        self.desktop_list.SetLabel("Asztal")  # Accessibility label for screen readers
        
        # Add desktop app items
        self.desktop_list.InsertItem(0, "Jegyzettömb")
        self.desktop_list.InsertItem(1, "Számológép")
        self.desktop_list.InsertItem(2, "Beállítások")
        self.desktop_list.InsertItem(3, "Ez a gép")
        self.desktop_list.InsertItem(4, "Lomtár")
        
        self.desktop_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated)
        
        sizer.Add(self.desktop_list, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def set_focus_to_list(self):
        """Set keyboard focus directly to the desktop list."""
        self.desktop_list.SetFocus()
        if self.desktop_list.GetItemCount() > 0:
            focused = self.desktop_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_FOCUSED)
            if focused == -1:
                self.desktop_list.Focus(0)
                self.desktop_list.Select(0, True)


    def on_item_activated(self, event):
        item_text = event.GetLabel()
        if self.open_app_callback:
            self.open_app_callback(item_text)
