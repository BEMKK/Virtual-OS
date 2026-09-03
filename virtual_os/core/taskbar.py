"""
Taskbar panel component for Virtual OS.
"""
import wx
import datetime
from virtual_os.core.config import system_config

class TaskbarPanel(wx.Panel):
    """Panel representing the taskbar at the bottom of the virtual desktop shell."""
    def __init__(self, parent, on_start_click_callback=None):
        super().__init__(parent)
        self.parent_frame = parent
        self.on_start_click_callback = on_start_click_callback
        
        self.SetBackgroundColour(wx.Colour(230, 230, 230))
        self.taskbar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # 1. Start Gomb (ez kerül legelőre, a 0. indexre)
        self.btn_start = wx.Button(self, label="Start menü")
        self.btn_start.SetName("Start menü gomb")
        self.btn_start.Bind(wx.EVT_BUTTON, self.on_start_click)
        self.taskbar_sizer.Add(self.btn_start, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        
        # 2. Kitűzött alkalmazások sizer-e (ez kerül a Start gomb mögé)
        self.pinned_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        btn_pinned_notepad = wx.Button(self, label="[Jegyzettömb]", style=wx.BU_EXACTFIT)
        btn_pinned_notepad.SetToolTip("Jegyzettömb indítása")
        btn_pinned_notepad.Bind(wx.EVT_BUTTON, lambda e: wx.GetTopLevelParent(self).open_app("Jegyzettömb"))
        btn_pinned_notepad.Bind(wx.EVT_CONTEXT_MENU, self.on_pinned_context_menu)
        self.pinned_sizer.Add(btn_pinned_notepad, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        
        # Itt Add()-ot használunk Insert(1, ...) helyett!
        self.taskbar_sizer.Add(self.pinned_sizer, 0, wx.EXPAND)
        
        self.taskbar_sizer.AddSpacer(5)
        
        # 3. Nyitott alkalmazások konténere
        self.apps_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.taskbar_sizer.Add(self.apps_sizer, 1, wx.EXPAND)
        
        # 4. Értesítési terület (System Tray)
        self.tray_panel = wx.Panel(self)
        tray_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_volume = wx.Button(self.tray_panel, label=f"Hangerő: {system_config.volume}%", style=wx.BU_EXACTFIT)
        self.btn_volume.SetName("Hangerő beállítása")
        self.btn_volume.Bind(wx.EVT_BUTTON, self.on_volume_click)
        
        self.btn_clock = wx.Button(self.tray_panel, label="00:00:00", style=wx.BU_EXACTFIT)
        self.btn_clock.SetName("Óra és dátum")
        self.btn_clock.Bind(wx.EVT_BUTTON, self.on_clock_click)
        
        tray_sizer.Add(self.btn_volume, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        tray_sizer.Add(self.btn_clock, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.tray_panel.SetSizer(tray_sizer)
        
        self.taskbar_sizer.Add(self.tray_panel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.SetSizer(self.taskbar_sizer)
        
        # Óra időzítő
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_clock, self.timer)
        self.timer.Start(1000)
        self.update_clock(None)
        
        # Rendszerkonfiguráció feliratkozás
        system_config.add_listener(self.on_config_changed)

    def on_pinned_context_menu(self, event):
        """Helyi menü a kitűzött gombra (ha szükséges)."""
        pass

    def on_config_changed(self, config):
        """Hangerő és óra frissítése beállításváltozáskor."""
        self.btn_volume.SetLabel(f"Hangerő: {config.volume}%")
        self.update_clock(None)
        self.Layout()

    def update_clock(self, event):
        now = datetime.datetime.now()
        fmt = "%H:%M" if system_config.use_24h_clock else "%I:%M %p"
        if system_config.show_clock_seconds:
            fmt = "%H:%M:%S" if system_config.use_24h_clock else "%I:%M:%S %p"
        
        self.btn_clock.SetLabel(now.strftime(fmt))

    def on_start_click(self, event):
        if self.on_start_click_callback:
            self.on_start_click_callback(self.btn_start.GetPosition())

    def on_volume_click(self, event):
        """Hangerő szabályzó ablak."""
        dlg = wx.Dialog(self, title="Hangerő szabályzó", size=(300, 150))
        sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(dlg, label=f"Rendszer hangerő ({system_config.volume}%):")
        slider = wx.Slider(dlg, value=system_config.volume, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        btn_close = wx.Button(dlg, label="Bezárás")
        
        def on_slider_change(e):
            system_config.set_volume(slider.GetValue())
            lbl.SetLabel(f"Rendszer hangerő ({system_config.volume}%):")
            
        slider.Bind(wx.EVT_SLIDER, on_slider_change)
        btn_close.Bind(wx.EVT_BUTTON, lambda e: dlg.Close())
        
        sizer.Add(lbl, 0, wx.ALL, 10)
        sizer.Add(slider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(btn_close, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        dlg.SetSizer(sizer)
        dlg.CentreOnParent()
        dlg.ShowModal()
        dlg.Destroy()

    def on_clock_click(self, event):
        """Dátum és idő felugró ablak."""
        now = datetime.datetime.now()
        date_str = now.strftime("%Y. %B %d., %A")
        time_str = now.strftime("%H:%M:%S")
        wx.MessageBox(
            f"Mai dátum: {date_str}\nPontos idő: {time_str}",
            "Dátum és idő",
            wx.OK | wx.ICON_INFORMATION
        )

    def get_taskbar_controls(self):
        """Visszaadja a tálcán lévő összes fókuszálható elemet helyes sorrendben."""
        controls = [self.btn_start]
        
        for child in self.apps_sizer.GetChildren():
            if child.IsWindow():
                controls.append(child.GetWindow())
                
        controls.append(self.btn_volume)
        controls.append(self.btn_clock)
        
        return controls