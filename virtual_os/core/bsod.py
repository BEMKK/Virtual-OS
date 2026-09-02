"""
BSOD (Blue Screen of Death) crash handler component for Virtual OS.
"""
import wx

class BSODFrame(wx.Frame):
    def __init__(self, error_message="FATAL_SYSTEM_ERROR", traceback_text=""):
        super().__init__(None, title="System Error", size=(1024, 768), style=wx.DEFAULT_FRAME_STYLE)
        
        self.SetBackgroundColour(wx.Colour(0, 0, 170))
        self.CentreOnScreen()
        
        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        font_large = wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        font_small = wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        
        lbl_header = wx.StaticText(self.panel, label=":( Virtual OS hiba miatt összeomlott.")
        lbl_header.SetForegroundColour(wx.Colour(255, 255, 255))
        lbl_header.SetFont(font_large)
        
        error_info = (
            f"\nHIBAKÓD: {error_message}\n\n"
            f"A rendszer védelme érdekében a Virtual OS leállt.\n\n"
            f"Részletek:\n{traceback_text}\n\n"
            f"Nyomjon meg egy billentyűt a kilépéshez..."
        )
        
        self.lbl_body = wx.StaticText(self.panel, label=error_info)
        self.lbl_body.SetForegroundColour(wx.Colour(255, 255, 255))
        self.lbl_body.SetFont(font_small)
        
        sizer.Add(lbl_header, 0, wx.ALL, 20)
        sizer.Add(self.lbl_body, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        
        self.panel.SetSizer(sizer)
        self.panel.Layout()

        # Eseménykezelés elhalasztása 1000 ms-ra (hogy véletlen se záródjon be azonnal)
        wx.CallLater(1000, self._bind_events)

    def _bind_events(self):
        # Beállítjuk a fókuszt a panelre
        self.panel.SetFocus()
        
        # EVT_CHAR_HOOK az egész ablakra elfogja a billentyűzetet
        self.Bind(wx.EVT_CHAR_HOOK, self.on_close_system)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.on_close_system)

    def on_close_system(self, event):
        self.Close()
        wx.GetApp().ExitMainLoop()