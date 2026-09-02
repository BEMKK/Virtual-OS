"""
Core Virtual OS components.
"""
from virtual_os.core.config import system_config, ConfigManager
from virtual_os.core.desktop import DesktopPanel
from virtual_os.core.taskbar import TaskbarPanel
from virtual_os.core.start_menu import StartMenu
from virtual_os.core.window_manager import WindowManager
from virtual_os.core.os_frame import VirtualOSFrame

__all__ = [
    "system_config",
    "ConfigManager",
    "DesktopPanel",
    "TaskbarPanel",
    "StartMenu",
    "WindowManager",
    "VirtualOSFrame",
]
