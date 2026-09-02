import wx

class StartMenuDialog(wx.Dialog):
    """A Start menüt megvalósító különálló Dialog ablak felugró főkapcsoló menüvel."""
    def __init__(self, parent, open_app_callback=None):
        super().__init__(parent, title="Start Menü", size=(320, 420), style=wx.DEFAULT_DIALOG_STYLE)
        self.open_app_callback = open_app_callback
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_title = wx.StaticText(panel, label="Start Menü")
        font = lbl_title.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        lbl_title.SetFont(font)
        sizer.Add(lbl_title, 0, wx.ALL, 10)
        
        # 1. Alkalmazások
        self.btn_notepad = wx.Button(panel, label="Jegyzettömb")
        self.btn_calc = wx.Button(panel, label="Számológép")
        self.btn_explorer = wx.Button(panel, label="Ez a gép")
        self.btn_settings = wx.Button(panel, label="Beállítások")
        
        sizer.Add(self.btn_notepad, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        sizer.Add(self.btn_calc, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        sizer.Add(self.btn_explorer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        sizer.Add(self.btn_settings, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        
        sizer.AddSpacer(15)
        
        # 2. Leállítási szekció - Egyetlen gomb felugró menüvel
        self.btn_power = wx.Button(panel, label="Főkapcsoló ⯅")
        sizer.Add(self.btn_power, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        
        panel.SetSizer(sizer)
        
        # Eseménykezelők kötése
        self.btn_notepad.Bind(wx.EVT_BUTTON, lambda e: self._launch_app("Jegyzettömb"))
        self.btn_calc.Bind(wx.EVT_BUTTON, lambda e: self._launch_app("Számológép"))
        self.btn_explorer.Bind(wx.EVT_BUTTON, lambda e: self._launch_app("Ez a gép"))
        self.btn_settings.Bind(wx.EVT_BUTTON, lambda e: self._launch_app("Beállítások"))
        
        # Főkapcsoló gomb eseménye
        self.btn_power.Bind(wx.EVT_BUTTON, self._show_power_menu)
        
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key_down)

    def _show_power_menu(self, event):
        """Létrehozza és megjeleníti a felugró menüt a gomb alatt."""
        menu = wx.Menu()
        
        item_sleep = menu.Append(wx.ID_ANY, "Alvó állapot")
        item_shutdown = menu.Append(wx.ID_ANY, "Leállítás")
        item_restart = menu.Append(wx.ID_ANY, "Újraindítás")
        
        self.Bind(wx.EVT_MENU, self._on_sleep, item_sleep)
        self.Bind(wx.EVT_MENU, self._on_restart, item_restart)
        self.Bind(wx.EVT_MENU, self._on_shutdown, item_shutdown)
        
        # Megjelenítés a gomb közvetlen közelében
        self.PopupMenu(menu)
        menu.Destroy()

    def _launch_app(self, app_name):
        self.Close()
        if self.open_app_callback:
            self.open_app_callback(app_name)

    def _on_sleep(self, event):
        wx.MessageBox("A rendszer alvó állapotba lépett.", "Alvó állapot", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def _on_restart(self, event):
        self.Close()
        wx.MessageBox("Rendszer újraindítása...", "Újraindítás", wx.OK | wx.ICON_INFORMATION)

    def _on_shutdown(self, event):
        self.Close()
        self.GetParent().Close()

    def _on_key_down(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

class StartMenu:
    """Start menü wrapper osztály."""
    def __init__(self, parent_frame, open_app_callback=None):
        self.parent_frame = parent_frame
        self.open_app_callback = open_app_callback

    def show(self, pos=None):
        dlg = StartMenuDialog(self.parent_frame, self.open_app_callback)
        dlg.CentreOnParent()
        dlg.ShowModal()
        dlg.Destroy()