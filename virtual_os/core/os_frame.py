"""
Main Virtual OS Desktop Frame module.
"""
import wx
from virtual_os.core.desktop import DesktopPanel
from virtual_os.core.taskbar import TaskbarPanel
from virtual_os.core.start_menu import StartMenu
from virtual_os.core.window_manager import WindowManager
from virtual_os.core.config import system_config
from virtual_os.apps.recicle_bin import RecycleBinApp

from virtual_os.apps.notepad import NotepadApp
from virtual_os.apps.calculator import CalculatorApp
from virtual_os.apps.settings import SettingsApp
from virtual_os.apps.explorer import ExplorerApp

class VirtualOSFrame(wx.Frame):
    """Main desktop shell window for Virtual OS."""
    def __init__(self):
        super().__init__(None, title="Virtual OS for Blinds (v0.3.2)", size=(1024, 768))
        self.CentreOnScreen()
        
        self.main_panel = wx.Panel(self, style=wx.TAB_TRAVERSAL)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 1. Desktop Panel
        self.desktop_panel = DesktopPanel(self.main_panel, open_app_callback=self.open_app)
        self.main_sizer.Add(self.desktop_panel, 1, wx.EXPAND)
        
        # 2. Taskbar Panel
        self.taskbar_panel = TaskbarPanel(self.main_panel, on_start_click_callback=self.show_start_menu)
        self.main_sizer.Add(self.taskbar_panel, 0, wx.EXPAND)
        
        self.main_panel.SetSizer(self.main_sizer)
        
        # 3. Start Menu Component
        self.start_menu = StartMenu(self, open_app_callback=self.open_app)
        
        # Window Manager initialization
        self.window_manager = WindowManager(self.taskbar_panel)
        
        # Setup Tab order & Keyboard Shortcuts
        self.setup_shortcuts()
        
        # Register EVT_CHAR_HOOK for shell tab navigation across Desktop <-> Start <-> Taskbar Apps <-> System Tray
        self.Bind(wx.EVT_CHAR_HOOK, self.on_shell_char_hook)
        
        # Register theme updates
        system_config.add_listener(self.on_theme_changed)
        
        # Default focus to desktop icons list
        wx.CallAfter(self.desktop_panel.set_focus_to_list)

    def get_shell_focus_widgets(self):
        """Return full ordered list of focusable shell widgets across panels."""
        widgets = [self.desktop_panel.desktop_list]
        taskbar_widgets = self.taskbar_panel.get_taskbar_controls()
        widgets.extend(taskbar_widgets)
        return widgets

    def on_shell_char_hook(self, event):
        """Intercept Tab, Shift+Tab, and F6 for shell focus traversal across panels."""
        key = event.GetKeyCode()
        shift_down = event.ShiftDown()
        
        current_focus = wx.Window.FindFocus()
        shell_widgets = self.get_shell_focus_widgets()
        
        # Check if focus is within shell widgets
        in_shell = False
        if current_focus:
            for w in shell_widgets:
                if current_focus == w:
                    in_shell = True
                    break
        
        if key == wx.WXK_TAB and in_shell:
            idx = shell_widgets.index(current_focus)
            next_idx = (idx - 1) % len(shell_widgets) if shift_down else (idx + 1) % len(shell_widgets)
            target = shell_widgets[next_idx]
                
            if target == self.desktop_panel.desktop_list:
                self.desktop_panel.set_focus_to_list()
            else:
                target.SetFocus()
            return
        elif key == wx.WXK_F6 and in_shell:
            # Switch between Desktop List and Taskbar Start Button
            if current_focus == self.desktop_panel.desktop_list:
                self.taskbar_panel.btn_start.SetFocus()
            else:
                self.desktop_panel.set_focus_to_list()
            return

        event.Skip()

    def setup_shortcuts(self):
        """Configure system-wide keyboard hotkeys (Start menu, Alt+Tab, Win+D)."""
        accel_entries = [
            (wx.ACCEL_CTRL, ord('E'), 1001),      # Ctrl+E for Start Menu
            (wx.ACCEL_ALT, wx.WXK_TAB, 1002),     # Alt+Tab for Window Switcher
            (wx.ACCEL_CTRL, ord('D'), 1003),      # Ctrl+D for Show Desktop (Win+D equivalent)
        ]
        accel_table = wx.AcceleratorTable(accel_entries)
        self.SetAcceleratorTable(accel_table)
        
        self.Bind(wx.EVT_MENU, lambda e: self.show_start_menu(self.taskbar_panel.btn_start.GetPosition()), id=1001)
        self.Bind(wx.EVT_MENU, lambda e: self.window_manager.cycle_windows(), id=1002)
        self.Bind(wx.EVT_MENU, lambda e: self.window_manager.toggle_show_desktop(self.desktop_panel.desktop_list), id=1003)

    def show_start_menu(self, pos):
        """Display Windows-style Start popup menu via StartMenu module."""
        self.start_menu.show(pos)

    def open_app(self, app_name, **kwargs):
        """Factory method to instantiate and register Virtual OS applications."""
        app_win = None
        
        if app_name == "Jegyzettömb":
            initial_file = kwargs.get("initial_file")
            initial_content = kwargs.get("initial_content")
            app_win = NotepadApp(
                self, 
                window_manager=self.window_manager, 
                initial_file=initial_file, 
                initial_content=initial_content
            )
        elif app_name == "Számológép":
            app_win = CalculatorApp(self, window_manager=self.window_manager)
        elif app_name == "Beállítások":
            app_win = SettingsApp(self, window_manager=self.window_manager)
        elif app_name in ["Ez a gép", "Fájlkezelő"]:
            app_win = ExplorerApp(self, window_manager=self.window_manager, open_app_callback=self.open_app)
        elif app_name == "Lomtár":
            app_win = RecycleBinApp(self, window_manager=self.window_manager)

        else:
            wx.MessageBox(f"Ismeretlen alkalmazás: {app_name}", "Hiba", wx.OK | wx.ICON_ERROR)
            return
            
        if app_win:
            self.window_manager.register_window(app_win, app_win.app_name)
            app_win.Show()

    def on_theme_changed(self, config):
        """Apply theme color updates across the shell."""
        if config.theme == "Sötét":
            bg_color = wx.Colour(40, 40, 40)
            fg_color = wx.Colour(240, 240, 240)
        elif config.theme == "Világos":
            bg_color = wx.Colour(250, 250, 250)
            fg_color = wx.Colour(10, 10, 10)
        else: # Klasszikus
            bg_color = wx.Colour(230, 230, 230)
            fg_color = wx.Colour(0, 0, 0)
            
        self.taskbar_panel.SetBackgroundColour(bg_color)
        self.taskbar_panel.Refresh()
