"""
Base frame component for Virtual OS applications.
"""
import wx

class BaseAppWindow(wx.Frame):
    """Base class for all Virtual OS application windows."""
    def __init__(self, parent, title, size=(600, 450), window_manager=None):
        full_title = f"{title}"
        super().__init__(parent, title=full_title, size=size, style=wx.DEFAULT_FRAME_STYLE)
        
        self.app_name = title
        self.window_manager = window_manager
        
        self.SetMinSize((300, 200))
        self.CentreOnScreen()
        
        # Bind close event & in-window tab navigation hook
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_base_char_hook)
        
    def on_close(self, event):
        """Notify window manager on application exit and destroy frame."""
        if self.window_manager:
            self.window_manager.unregister_window(self)
        self.Destroy()

    def get_focusable_widgets(self, container=None):
        """Recursively collect all visible, enabled focusable child controls in document/tab order."""
        if container is None:
            container = self
        
        widgets = []
        for child in container.GetChildren():
            if not child.IsShown() or not child.IsEnabled():
                continue
                
            # If child is an interactive control that can receive keyboard focus
            if isinstance(child, (wx.Button, wx.TextCtrl, wx.ListBox, wx.ListCtrl, wx.Choice, wx.CheckBox, wx.Slider, wx.ComboBox, wx.TreeCtrl)):
                widgets.append(child)
            elif isinstance(child, wx.Notebook):
                # Add notebook active page controls
                page = child.GetCurrentPage()
                if page:
                    widgets.extend(self.get_focusable_widgets(page))
            elif isinstance(child, (wx.Panel, wx.SplitterWindow, wx.ScrolledWindow)):
                widgets.extend(self.get_focusable_widgets(child))
                
        return widgets

    def on_base_char_hook(self, event):
        """Handle Tab and Shift+Tab across all window controls."""
        key = event.GetKeyCode()
        shift_down = event.ShiftDown()
        ctrl_down = event.ControlDown()
        
        current_focus = wx.Window.FindFocus()
        is_multiline_text = isinstance(current_focus, wx.TextCtrl) and current_focus.IsMultiLine()
        
        if key == wx.WXK_TAB and not is_multiline_text:
            widgets = self.get_focusable_widgets()
            if widgets:
                if current_focus in widgets:
                    idx = widgets.index(current_focus)
                    next_idx = (idx - 1) % len(widgets) if shift_down else (idx + 1) % len(widgets)
                    widgets[next_idx].SetFocus()
                    return
                else:
                    widgets[0].SetFocus()
                    return
        elif key == wx.WXK_TAB and is_multiline_text and ctrl_down:
            widgets = self.get_focusable_widgets()
            if widgets and current_focus in widgets:
                idx = widgets.index(current_focus)
                next_idx = (idx - 1) % len(widgets) if shift_down else (idx + 1) % len(widgets)
                widgets[next_idx].SetFocus()
                return

        event.Skip()
