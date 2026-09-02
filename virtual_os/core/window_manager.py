"""
Window Manager component for Virtual OS.
"""
import wx

class WindowManager:
    """Manages application windows, taskbar button synchronization, Alt+Tab, and Win+D logic."""
    def __init__(self, taskbar_panel):
        self.taskbar_panel = taskbar_panel
        # Map: app_window -> taskbar_btn
        self.open_windows = {}
        self._window_order = []
        self._desktop_showing = False
        self._minimized_states = {}

    def register_window(self, app_window, title):
        """Register a newly opened application window and create its taskbar button."""
        btn_label = f"Ablak: {title}"
        taskbar_btn = wx.Button(self.taskbar_panel, label=btn_label)
        taskbar_btn.SetName(f"{title} tálca gomb")
        
        taskbar_btn.Bind(wx.EVT_BUTTON, lambda evt: self.on_taskbar_btn_click(app_window))
        
        self.taskbar_panel.apps_sizer.Add(taskbar_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        self.taskbar_panel.Layout()
        
        self.open_windows[app_window] = taskbar_btn
        self._window_order.append(app_window)
        
        # Bring focus to newly opened app
        wx.CallAfter(self.focus_window, app_window)

    def unregister_window(self, app_window):
        """Remove a closed application window and destroy its taskbar button."""
        if app_window in self.open_windows:
            btn = self.open_windows[app_window]
            del self.open_windows[app_window]
            if app_window in self._window_order:
                self._window_order.remove(app_window)
            btn.Destroy()
            self.taskbar_panel.Layout()

    def on_taskbar_btn_click(self, app_window):
        """Toggle restore/focus or iconize when taskbar button is clicked."""
        if app_window.IsIconized():
            app_window.Restore()
            app_window.Raise()
            app_window.SetFocus()
        elif app_window.IsActive():
            app_window.Iconize(True)
        else:
            app_window.Raise()
            app_window.SetFocus()

    def focus_window(self, app_window):
        """Restore and raise window to top focus."""
        if app_window.IsIconized():
            app_window.Restore()
        app_window.Raise()
        app_window.SetFocus()

    def cycle_windows(self):
        """Alt+Tab implementation: cycle through open windows."""
        if not self._window_order:
            return
            
        # Move current front window to back of cycle list
        active_window = None
        for win in self._window_order:
            if win.IsActive():
                active_window = win
                break
                
        if active_window and len(self._window_order) > 1:
            self._window_order.remove(active_window)
            self._window_order.append(active_window)
            
        target_win = self._window_order[0]
        self.focus_window(target_win)

    def toggle_show_desktop(self, desktop_list_widget=None):
        """Win+D implementation: minimize all windows or restore them."""
        if not self.open_windows:
            if desktop_list_widget:
                desktop_list_widget.SetFocus()
            return
            
        if not self._desktop_showing:
            # Minimize all windows
            for win in list(self.open_windows.keys()):
                self._minimized_states[win] = win.IsIconized()
                if not win.IsIconized():
                    win.Iconize(True)
            self._desktop_showing = True
            if desktop_list_widget:
                desktop_list_widget.SetFocus()
        else:
            # Restore previously unminimized windows
            for win, was_min in self._minimized_states.items():
                if win in self.open_windows and not was_min:
                    win.Restore()
            self._desktop_showing = False
