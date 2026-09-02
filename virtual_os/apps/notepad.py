"""
Jegyzettömb (Notepad) application for Virtual OS.
"""
import wx
import datetime
import os
from virtual_os.apps.base_app import BaseAppWindow

class NotepadApp(BaseAppWindow):
    def __init__(self, parent, window_manager=None, initial_file=None, initial_content=None):
        super().__init__(parent, title="Névtelen - Jegyzettömb", size=(700, 500), window_manager=window_manager)
        
        self.current_file = initial_file
        self.is_modified = False
        
        self.init_ui()
        self.init_menubar()
        self.init_statusbar()
        self.init_shortcuts()
        
        if initial_content is not None:
            self.text_ctrl.SetValue(initial_content)
            self.is_modified = False
            self.update_title()
        elif initial_file and os.path.exists(initial_file):
            self.load_file(initial_file)

    def init_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.text_ctrl = wx.TextCtrl(
            panel, 
            style=wx.TE_MULTILINE | wx.TE_NOHIDESEL
        )

        self.text_ctrl.SetName("Jegyzettömb szövegmező")
        
        self.text_ctrl.Bind(wx.EVT_TEXT, self.on_text_changed)
        self.text_ctrl.Bind(wx.EVT_KEY_UP, self.update_cursor_pos)
        self.text_ctrl.Bind(wx.EVT_LEFT_UP, self.update_cursor_pos)
        
        sizer.Add(self.text_ctrl, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        
        wx.CallAfter(self.text_ctrl.SetFocus)

    def init_menubar(self):
        menubar = wx.MenuBar()
        
        # 1. Fájl menü
        file_menu = wx.Menu()
        new_item = file_menu.Append(wx.ID_NEW, "&Új\tCtrl+N", "Új dokumentum létrehozása")
        open_item = file_menu.Append(wx.ID_OPEN, "&Megnyitás...\tCtrl+O", "Meglévő fájl megnyitása")
        save_item = file_menu.Append(wx.ID_SAVE, "&Mentés\tCtrl+S", "Dokumentum mentése")
        save_as_item = file_menu.Append(wx.ID_SAVEAS, "Mentés má&sként...", "Dokumentum mentése új néven")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "&Kilépés", "Jegyzettömb bezárása")
        
        menubar.Append(file_menu, "&Fájl")
        
        # 2. Szerkesztés menü
        edit_menu = wx.Menu()
        undo_item = edit_menu.Append(wx.ID_UNDO, "&Visszavonás\tCtrl+Z")
        edit_menu.AppendSeparator()
        cut_item = edit_menu.Append(wx.ID_CUT, "&Kivágás\tCtrl+X")
        copy_item = edit_menu.Append(wx.ID_COPY, "MÁ&solás\tCtrl+C")
        paste_item = edit_menu.Append(wx.ID_PASTE, "Be&illesztés\tCtrl+V")
        delete_item = edit_menu.Append(wx.ID_DELETE, "Tö&rlés\tDel")
        edit_menu.AppendSeparator()
        select_all_item = edit_menu.Append(wx.ID_SELECTALL, "Ös&szes kijelölése\tCtrl+A")
        datetime_item = edit_menu.Append(1001, "Idő/&Dátum\tF5", "Aktuális dátum és idő beszúrása")
        
        menubar.Append(edit_menu, "&Szerkesztés")
        
        # 3. Nézet menü
        view_menu = wx.Menu()
        self.statusbar_item = view_menu.AppendCheckItem(1002, "&Állapotsor", "Állapotsor megjelenítése/elrejtése")
        self.statusbar_item.Check(True)
        menubar.Append(view_menu, "&Nézet")
        
        # 4. Súgó menü
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, "A Jegyzettömb &névjegye", "Információ az alkalmazásról")
        menubar.Append(help_menu, "&Súgó")
        
        self.SetMenuBar(menubar)
        
        # Binds
        self.Bind(wx.EVT_MENU, self.on_new, new_item)
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_save_as, save_as_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        
        self.Bind(wx.EVT_MENU, lambda e: self.text_ctrl.Undo(), undo_item)
        self.Bind(wx.EVT_MENU, lambda e: self.text_ctrl.Cut(), cut_item)
        self.Bind(wx.EVT_MENU, lambda e: self.text_ctrl.Copy(), copy_item)
        self.Bind(wx.EVT_MENU, lambda e: self.text_ctrl.Paste(), paste_item)
        self.Bind(wx.EVT_MENU, lambda e: self.text_ctrl.RemoveSelection(), delete_item)
        self.Bind(wx.EVT_MENU, lambda e: self.text_ctrl.SelectAll(), select_all_item)
        self.Bind(wx.EVT_MENU, self.on_insert_datetime, id=1001)
        self.Bind(wx.EVT_MENU, self.on_toggle_statusbar, id=1002)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

    def init_statusbar(self):
        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([-1, 150])
        self.update_cursor_pos(None)

    def init_shortcuts(self):
        # Additional hotkeys if needed
        pass

    def update_title(self):
        filename = os.path.basename(self.current_file) if self.current_file else "Névtelen"
        mod_mark = "*" if self.is_modified else ""
        self.SetTitle(f"{mod_mark}{filename} - Jegyzettömb - Virtual OS")

    def update_cursor_pos(self, event):
        pos = self.text_ctrl.GetInsertionPoint()
        text = self.text_ctrl.GetValue()
        lines = text[:pos].split('\n')
        line_num = len(lines)
        col_num = len(lines[-1]) + 1
        
        self.statusbar.SetStatusText(f"Sor {line_num}, Oszlop {col_num}", 1)
        if event:
            event.Skip()

    def on_text_changed(self, event):
        if not self.is_modified:
            self.is_modified = True
            self.update_title()
        self.update_cursor_pos(None)
        event.Skip()

    def prompt_save_changes(self):
        if not self.is_modified:
            return True
        
        filename = os.path.basename(self.current_file) if self.current_file else "Névtelen"
        dialog = wx.MessageDialog(
            self,
            f"Menti a módosításokat a(z) \"{filename}\" fájlba?",
            "Jegyzettömb",
            wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION
        )
        res = dialog.ShowModal()
        dialog.Destroy()
        
        if res == wx.ID_YES:
            return self.on_save(None)
        elif res == wx.ID_NO:
            return True
        else: # Cancel
            return False

    def on_new(self, event):
        if self.prompt_save_changes():
            self.text_ctrl.Clear()
            self.current_file = None
            self.is_modified = False
            self.update_title()

    def on_open(self, event):
        if not self.prompt_save_changes():
            return
            
        with wx.FileDialog(
            self, "Fájl megnyitása", wildcard="Szöveges fájlok (*.txt)|*.txt|Minden fájl (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            self.load_file(path)

    def load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text_ctrl.SetValue(content)
            self.current_file = path
            self.is_modified = False
            self.update_title()
        except Exception as err:
            wx.MessageBox(f"Hiba a fájl megnyitásakor: {err}", "Hiba", wx.OK | wx.ICON_ERROR)

    def on_save(self, event):
        if self.current_file is None:
            return self.on_save_as(event)
        else:
            return self.save_to_file(self.current_file)

    def on_save_as(self, event):
        with wx.FileDialog(
            self, "Fájl mentése másként", wildcard="Szöveges fájlok (*.txt)|*.txt|Minden fájl (*.*)|*.*",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return False
            path = fileDialog.GetPath()
            return self.save_to_file(path)

    def save_to_file(self, path):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.text_ctrl.GetValue())
            self.current_file = path
            self.is_modified = False
            self.update_title()
            return True
        except Exception as err:
            wx.MessageBox(f"Hiba a fájl mentésekor: {err}", "Hiba", wx.OK | wx.ICON_ERROR)
            return False

    def on_insert_datetime(self, event):
        now_str = datetime.datetime.now().strftime("%H:%M %Y.%m.%d.")
        self.text_ctrl.WriteText(now_str)

    def on_toggle_statusbar(self, event):
        show = self.statusbar_item.IsChecked()
        self.statusbar.Show(show)
        self.Layout()

    def on_about(self, event):
        wx.MessageBox(
            "Jegyzettömb - Virtual OS\nVerzió: 1.0\nEgy akadálymentesített szövegszerkesztő a Virtual OS rendszerben.",
            "A Jegyzettömb névjegye",
            wx.OK | wx.ICON_INFORMATION
        )

    def on_exit(self, event):
        self.Close()

    def on_close(self, event):
        if self.prompt_save_changes():
            super().on_close(event)
        else:
            event.Veto()
