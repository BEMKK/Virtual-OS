# Virtual OS (v0.3.3)

A Virtual OS egy billentyűzet-orientált virtuális operációsrendszer asztali környezet, Python és **wxPython** alapon.

## A projekt áttekintése

A projekt célja egy olyan operációs rendszer felület szimulációja, amely főként billentyűzettel kezelhető, és a felülete illetve kezelése hasonlít a Windows megjelenéséhez és kezeléséhez.

## Főbb Funkciók

- **Saját BSOD (Blue Screen of Death) kivételkezelő**: Végzetes hibák esetén nem omlik össze a program a szokásos módon, hanem a Windows-hoz hasonló kék halál képernyőt jelenít meg a hiba részleteivel.
- **Asztal és Tálca**:
  - Asztali alkalmazásikonok lista nézetben.
  - Tálca Start gombbal, kitűzött alkalmazásokkal, a megnyitott ablakok gombjaival és Értesítési területtel (System Tray).
  - Értesítési terület beépített digitális órával és hangerőszabályzóval.
- **Ablakkezelő (Window Manager)**:
  - Dinamikus tálca-gomb szinkronizáció.
  - `Alt + Tab` ablakváltó támogatás.
  - `Ctrl + D` (Win+D megfelelője) az Asztal gyors megjelenítéséhez / ablakok tálcára kicsinyítéséhez.
- **Beépített Virtual OS Alkalmazások**:
  - **Jegyzettömb (`NotepadApp`)**: Szöveges fájlok megnyitása, szerkesztése és mentése.
  - **Számológép (`CalculatorApp`)**: Matematikai műveletek végrehajtása.
  - **Fájlkezelő (`ExplorerApp`)**: Virtuális meghajtók és könyvtárak böngészése.
  - **Beállítások (`SettingsApp`)**: Rendszertémák (Klasszikus, Világos, Sötét).
  - 🗑️ **Lomtár (`RecycleBinApp`)**: Törölt fájlok a virtuális könyvtárakban.

---

## Projektstruktúra

virtual_os/core/
├── main.py                  # Belépési pont és globális sys.excepthook (BSOD)
├── window_manager.py        # Ablakkezelő (Alt+Tab, Win+D, tálca szinkron)
├── bsod.py                  # Kék képernyő (BSOD) hibamegjelenítő
├── config.py                # Globális beállítások és Observer mintájú eseménykezelés
├── desktop.py               # Asztal panel és alkalmazáslista
├── os_frame.py              # Fő operációs rendszer ablak (VirtualOSFrame)
├── start_menu.py            # Start menü és főkapcsoló dialógus
├── taskbar.py               # Tálca, óra, hangerő és tálcagombok

virtual_os/apps/
└── base_app.py              # Alap osztály a belső alkalmazásablakokhoz
└── notepad.py            # Jegyzettömb
└── calculator.py            # Számológép
└── settings.py            # Beállítások alkalmazás
└── explorer.py        # Fájlkezelő
└── recycle.py (hibásan írva recicle.py)            # Lomtár

## Indítás és használat
A projektet a "python main.py" paranccsal indíthatod a projekt forráskódjának mappájából, vagy közvetlenül a main.py futtatásával.
