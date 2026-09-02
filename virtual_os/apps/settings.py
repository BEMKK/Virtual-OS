"""
Beállítások (Settings) application for Virtual OS.
"""
import wx
from virtual_os.apps.base_app import BaseAppWindow
from virtual_os.core.config import system_config

class SettingsApp(BaseAppWindow):
    def __init__(self, parent, window_manager=None):
        super().__init__(parent, title="Beállítások", size=(520, 400), window_manager=window_manager)
        
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.notebook = wx.Notebook(panel)
        
        # 1. Tab: Megjelenés
        self.theme_panel = wx.Panel(self.notebook)
        theme_sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_theme = wx.StaticText(self.theme_panel, label="Rendszer témája:")
        self.choice_theme = wx.Choice(
            self.theme_panel, 
            choices=["Klasszikus", "Világos", "Sötét"]
        )
        self.choice_theme.SetStringSelection(system_config.theme)
        
        theme_sizer.Add(lbl_theme, 0, wx.ALL, 10)
        theme_sizer.Add(self.choice_theme, 0, wx.LEFT | wx.RIGHT, 10)
        self.theme_panel.SetSizer(theme_sizer)
        
        # 2. Tab: Hangerő és Hangok
        self.sound_panel = wx.Panel(self.notebook)
        sound_sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_vol = wx.StaticText(self.sound_panel, label="Fő hangerő:")
        self.slider_volume = wx.Slider(
            self.sound_panel, 
            value=system_config.volume, 
            minValue=0, 
            maxValue=100,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        
        self.chk_sound_fx = wx.CheckBox(self.sound_panel, label="Rendszerhangok engedélyezése")
        self.chk_sound_fx.SetValue(system_config.sound_effects_enabled)
        
        sound_sizer.Add(lbl_vol, 0, wx.ALL, 10)
        sound_sizer.Add(self.slider_volume, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        sound_sizer.Add(self.chk_sound_fx, 0, wx.ALL, 10)
        self.sound_panel.SetSizer(sound_sizer)
        
        # 3. Tab: Dátum és Idő
        self.time_panel = wx.Panel(self.notebook)
        time_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.chk_24h = wx.CheckBox(self.time_panel, label="24 órás időkijelzés használata")
        self.chk_24h.SetValue(system_config.use_24h_clock)
        
        self.chk_sec = wx.CheckBox(self.time_panel, label="Másodpercek megjelenítése a tálcán")
        self.chk_sec.SetValue(system_config.show_clock_seconds)
        
        time_sizer.Add(self.chk_24h, 0, wx.ALL, 10)
        time_sizer.Add(self.chk_sec, 0, wx.ALL, 10)
        self.time_panel.SetSizer(time_sizer)
        
        # 4. Tab: Kisegítő lehetőségek
        self.access_panel = wx.Panel(self.notebook)
        access_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.chk_sr_hints = wx.CheckBox(self.access_panel, label="Képernyőolvasó (NVDA / JAWS) részletes tippek engedélyezése")
        self.chk_sr_hints.SetValue(system_config.screen_reader_hints)
        
        access_sizer.Add(self.chk_sr_hints, 0, wx.ALL, 10)
        self.access_panel.SetSizer(access_sizer)
        
        # Add tabs
        self.notebook.AddPage(self.theme_panel, "Megjelenés")
        self.notebook.AddPage(self.sound_panel, "Hangerő és Hangok")
        self.notebook.AddPage(self.time_panel, "Dátum és Idő")
        self.notebook.AddPage(self.access_panel, "Kisegítő lehetőségek")
        
        main_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        
        # Action buttons: OK, Mégse, Alkalmaz
        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, label="OK")
        btn_cancel = wx.Button(panel, label="Mégse")
        btn_apply = wx.Button(panel, label="Alkalmaz")
        
        btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        btn_apply.Bind(wx.EVT_BUTTON, self.on_apply)
        
        btn_box.Add(btn_ok, 0, wx.RIGHT, 5)
        btn_box.Add(btn_cancel, 0, wx.RIGHT, 5)
        btn_box.Add(btn_apply, 0, wx.RIGHT, 5)
        
        main_sizer.Add(btn_box, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        panel.SetSizer(main_sizer)

    def apply_settings(self):
        system_config.set_theme(self.choice_theme.GetStringSelection())
        system_config.set_volume(self.slider_volume.GetValue())
        system_config.sound_effects_enabled = self.chk_sound_fx.GetValue()
        system_config.set_clock_settings(
            use_24h=self.chk_24h.GetValue(),
            show_seconds=self.chk_sec.GetValue()
        )
        system_config.screen_reader_hints = self.chk_sr_hints.GetValue()
        system_config.notify_changes()

    def on_apply(self, event):
        self.apply_settings()

    def on_ok(self, event):
        self.apply_settings()
        self.Close()

    def on_cancel(self, event):
        self.Close()
