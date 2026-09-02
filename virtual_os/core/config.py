"""
System configuration manager for Virtual OS.
"""

class ConfigManager:
    """Manages system settings, state, and observer listeners."""
    def __init__(self):
        self.volume = 100  # 0 to 100
        self.use_24h_clock = True
        self.show_clock_seconds = True
        self.theme = "Klasszikus"
        self.screen_reader_hints = True
        self.sound_effects_enabled = True
        self.recycle_bin = []  # Törölt fájlok listája: [{"name": ..., "content": ..., "path": ...}]
        
        self._listeners = []

    def add_listener(self, callback):
        """Add a callback to be called when configuration changes."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def remove_listener(self, callback):
        """Remove a configuration listener callback."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def notify_changes(self):
        """Notify all registered listeners about configuration updates."""
        for callback in self._listeners:
            try:
                callback(self)
            except Exception as e:
                print(f"[ConfigManager] Error in listener callback: {e}")

    def set_volume(self, volume_level):
        """Set volume percentage (0-100)."""
        self.volume = max(0, min(100, int(volume_level)))
        self.notify_changes()

    def set_clock_settings(self, use_24h=True, show_seconds=True):
        """Update clock display preferences."""
        self.use_24h_clock = use_24h
        self.show_clock_seconds = show_seconds
        self.notify_changes()

    def set_theme(self, theme_name):
        """Set UI visual theme."""
        if theme_name in ["Klasszikus", "Világos", "Sötét"]:
            self.theme = theme_name
            self.notify_changes()

    def move_to_trash(self, name, content, path="Asztal"):
        self.recycle_bin.append({"name": name, "content": content, "path": path})
        self.notify_changes()

    def empty_trash(self):
        self.recycle_bin.clear()
        self.notify_changes()

# Global singleton configuration instance
system_config = ConfigManager()
