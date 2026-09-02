import sys
import traceback
import wx
from virtual_os.core.os_frame import VirtualOSFrame
from virtual_os.core.bsod import BSODFrame

bsod_instance = None

def handle_exception(exc_type, exc_value, exc_traceback):
    global bsod_instance

    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    tb_lines = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    # A hibakezelést az eseményciklus biztonságos fázisára ütemezzük
    wx.CallAfter(_show_bsod, str(exc_type.__name__), tb_lines)

def _show_bsod(error_name, tb_lines):
    global bsod_instance

    # Elrejtjük és megsemmisítjük a többi ablakot
    top_windows = wx.GetTopLevelWindows()
    for window in top_windows:
        window.Hide()
        window.Destroy()
        
    # Létrehozzuk és megjelenítjük a BSOD-ot
    bsod_instance = BSODFrame(error_message=error_name, traceback_text=tb_lines)
    bsod_instance.Show()

def main():
    app = wx.App(False)
    app.SetExitOnFrameDelete(False)
    
    sys.excepthook = handle_exception
    
    frame = VirtualOSFrame()
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()