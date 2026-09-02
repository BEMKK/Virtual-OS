"""
Ez a gép (File Explorer) application for Virtual OS.
"""
import wx
import os
from virtual_os.apps.base_app import BaseAppWindow
from virtual_os.core.config import system_config

class ExplorerApp(BaseAppWindow):
    def __init__(self, parent, window_manager=None, open_app_callback=None):
        super().__init__(parent, title="Ez a gép", size=(650, 450), window_manager=window_manager)
        self.open_app_callback = open_app_callback
        
        # Virtual mock file system structure
        self.virtual_fs = {
            "Dokumentumok": {
                "Jegyzetek.txt": "Ez egy minta szöveges fájl a Dokumentumok mappában.\nVirtual OS v0.3.0.",
                "Projekt_terv.txt": "1. Moduláris felépítés\n2. Tab sorrend beállítása\n3. Akadálymentesítés."
            },
            "Letöltések": {
                "Útmutató.txt": "Üdvözöljük a Virtual OS-ben!\nA billentyűzet-navigációhoz használja a Tab és a Nyíl billentyűket."
            },
            "Képek": {},
            "Helyi lemez (C:)": {
                "Rendszer.txt": "Rendszerfájlok és beállítások."
            }
        }
        
        self.current_folder = "Dokumentumok"
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Address Bar / Path Status
        self.lbl_path = wx.StaticText(panel, label=f"Mappa: Ez a gép > {self.current_folder}")
        path_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.lbl_path.SetFont(path_font)
        main_sizer.Add(self.lbl_path, 0, wx.ALL, 10)
        
        # Splitter window: Left = Folders Tree/List, Right = Files List
        splitter = wx.SplitterWindow(panel, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        
        left_panel = wx.Panel(splitter)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl_folders = wx.StaticText(left_panel, label="Mappák:")
        self.folder_list = wx.ListBox(left_panel, choices=list(self.virtual_fs.keys()))
        self.folder_list.SetSelection(0)
        self.folder_list.Bind(wx.EVT_LISTBOX, self.on_folder_select)

        left_sizer.Add(lbl_folders, 0, wx.ALL, 5)
        left_sizer.Add(self.folder_list, 1, wx.EXPAND | wx.ALL, 5)
        left_panel.SetSizer(left_sizer)
        
        right_panel = wx.Panel(splitter)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl_files = wx.StaticText(right_panel, label="Fájlok:")
        self.file_list = wx.ListCtrl(right_panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.file_list.InsertColumn(0, "Fájlnév", width=250)
        self.file_list.InsertColumn(1, "Típus", width=120)
        self.file_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_file_activated)
        self.file_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_file_context_menu)        

       
        right_sizer.Add(lbl_files, 0, wx.ALL, 5)
        right_sizer.Add(self.file_list, 1, wx.EXPAND | wx.ALL, 5)
        right_panel.SetSizer(right_sizer)
        
        splitter.SplitVertically(left_panel, right_panel, 200)
        main_sizer.Add(splitter, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        
        panel.SetSizer(main_sizer)
        self.populate_files(self.current_folder)

    def on_folder_select(self, event):
        sel = self.folder_list.GetStringSelection()
        if sel:
            self.current_folder = sel
            self.lbl_path.SetLabel(f"Mappa: Ez a gép > {self.current_folder}")
            self.populate_files(sel)

    def populate_files(self, folder_name):
        self.file_list.DeleteAllItems()
        files = self.virtual_fs.get(folder_name, {})
        for idx, (filename, content) in enumerate(files.items()):
            file_type = "Szöveges dokumentum" if filename.endswith(".txt") else "Fájl"
            self.file_list.InsertItem(idx, filename)
            self.file_list.SetItem(idx, 1, file_type)

    def on_file_activated(self, event):
        filename = event.GetLabel()
        files = self.virtual_fs.get(self.current_folder, {})
        if filename in files:
            content = files[filename]
            if self.open_app_callback:
                self.open_app_callback("Jegyzettömb", initial_file=filename, initial_content=content)

    def on_file_context_menu(self, event):
        selected_idx = event.GetIndex()
        filename = event.GetLabel()
    
        menu = wx.Menu()
        item_open = menu.Append(wx.ID_ANY, "Megnyitás")
        item_pin = menu.Append(wx.ID_ANY, "Kitűzés a tálcára")
        menu.AppendSeparator()
        item_delete = menu.Append(wx.ID_ANY, "Törlés (Lomtárba)")
    
        # Eseménykezelők kötése
        self.Bind(wx.EVT_MENU, lambda e: self.on_file_activated(event), item_open)
        self.Bind(wx.EVT_MENU, lambda e: self.delete_file(filename), item_delete)
    
        self.PopupMenu(menu)
        menu.Destroy()

    def delete_file(self, filename):
        if filename in self.virtual_fs[self.current_folder]:
            content = self.virtual_fs[self.current_folder].pop(filename)
            # Áthelyezés a globális Lomtárba:
            system_config.move_to_trash(name=filename, content=content, path=self.current_folder)
            self.populate_files(self.current_folder)
