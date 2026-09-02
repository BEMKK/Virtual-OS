"""
Számológép (Calculator) application for Virtual OS.
"""
import wx
import math
from virtual_os.apps.base_app import BaseAppWindow

class CalculatorApp(BaseAppWindow):
    def __init__(self, parent, window_manager=None):
        super().__init__(parent, title="Számológép", size=(340, 420), window_manager=window_manager)
        
        self.current_value = "0"
        self.pending_op = None
        self.stored_value = None
        self.new_entry = True
        
        self.init_ui()
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

    def init_ui(self):
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Display
        self.display = wx.TextCtrl(
            panel, 
            value="0", 
            style=wx.TE_RIGHT | wx.TE_READONLY,
            size=(-1, 50)
        )
        display_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.display.SetFont(display_font)
        self.display.SetName("Kijelző")
        
        main_sizer.Add(self.display, 0, wx.EXPAND | wx.ALL, 10)
        
        # Button Grid (6 rows x 4 columns)
        grid = wx.GridSizer(6, 4, 4, 4)
        
        buttons = [
            ("Százalék", self.on_percent), ("Beírás törlése", self.on_ce), ("Előzmények törlése", self.on_c), ("Utoljára beírt törlése", self.on_backspace),
            ("1/x", self.on_reciprocal), ("x²", self.on_square), ("√x", self.on_sqrt), ("Osztva", lambda e: self.on_operator("÷")),
            ("7", lambda e: self.on_digit("7")), ("8", lambda e: self.on_digit("8")), ("9", lambda e: self.on_digit("9")), ("Szorozva", lambda e: self.on_operator("×")),
            ("4", lambda e: self.on_digit("4")), ("5", lambda e: self.on_digit("5")), ("6", lambda e: self.on_digit("6")), ("Mínusz", lambda e: self.on_operator("-")),
            ("1", lambda e: self.on_digit("1")), ("2", lambda e: self.on_digit("2")), ("3", lambda e: self.on_digit("3")), ("Plusz", lambda e: self.on_operator("+")),
            ("Plusz vagy mínusz", self.on_negate), ("0", lambda e: self.on_digit("0")), ("Tizedesvessző", self.on_decimal), ("Egyenlő", self.on_equals)
        ]
        
        for label, handler in buttons:
            btn = wx.Button(panel, label=label, size=(60, 45))
            btn_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            btn.SetFont(btn_font)
            btn.Bind(wx.EVT_BUTTON, handler)
            grid.Add(btn, 1, wx.EXPAND)
            
        main_sizer.Add(grid, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        panel.SetSizer(main_sizer)

    def set_display(self, text):
        self.current_value = str(text)
        self.display.SetValue(self.current_value)

    def get_number(self):
        val_str = self.current_value.replace(',', '.')
        try:
            return float(val_str)
        except ValueError:
            return 0.0

    def format_number(self, num):
        if math.isnan(num) or math.isinf(num):
            return "Hiba"
        if num.is_integer():
            return str(int(num))
        # Format floating point reasonably
        res = f"{num:.10g}".replace('.', ',')
        return res

    def on_digit(self, digit):
        if self.new_entry or self.current_value == "0" or self.current_value == "Hiba":
            self.set_display(digit)
            self.new_entry = False
        else:
            if len(self.current_value) < 15:
                self.set_display(self.current_value + digit)

    def on_decimal(self, event):
        if self.new_entry or self.current_value == "Hiba":
            self.set_display("0,")
            self.new_entry = False
        elif "," not in self.current_value:
            self.set_display(self.current_value + ",")

    def on_c(self, event):
        self.current_value = "0"
        self.stored_value = None
        self.pending_op = None
        self.new_entry = True
        self.set_display("0")

    def on_ce(self, event):
        self.set_display("0")
        self.new_entry = True

    def on_backspace(self, event):
        if self.new_entry or self.current_value == "Hiba":
            return
        if len(self.current_value) > 1:
            self.set_display(self.current_value[:-1])
        else:
            self.set_display("0")
            self.new_entry = True

    def on_negate(self, event):
        num = self.get_number()
        num = -num
        self.set_display(self.format_number(num))

    def on_square(self, event):
        num = self.get_number()
        res = num ** 2
        self.set_display(self.format_number(res))
        self.new_entry = True

    def on_sqrt(self, event):
        num = self.get_number()
        if num < 0:
            self.set_display("Érvénytelen bemenet")
        else:
            self.set_display(self.format_number(math.sqrt(num)))
        self.new_entry = True

    def on_reciprocal(self, event):
        num = self.get_number()
        if num == 0:
            self.set_display("Nullával osztás nem lehetséges")
        else:
            self.set_display(self.format_number(1.0 / num))
        self.new_entry = True

    def on_percent(self, event):
        num = self.get_number()
        if self.stored_value is not None:
            res = (self.stored_value * num) / 100.0
        else:
            res = num / 100.0
        self.set_display(self.format_number(res))

    def on_operator(self, op):
        current_num = self.get_number()
        if self.stored_value is not None and not self.new_entry:
            self.calculate()
        else:
            self.stored_value = current_num
            
        self.pending_op = op
        self.new_entry = True

    def calculate(self):
        if self.stored_value is None or self.pending_op is None:
            return
        
        current_num = self.get_number()
        res = 0.0
        
        if self.pending_op == "+":
            res = self.stored_value + current_num
        elif self.pending_op == "-":
            res = self.stored_value - current_num
        elif self.pending_op == "×":
            res = self.stored_value * current_num
        elif self.pending_op == "÷":
            if current_num == 0:
                self.set_display("Nullával osztás nem lehetséges")
                self.stored_value = None
                self.pending_op = None
                self.new_entry = True
                return
            res = self.stored_value / current_num
            
        self.set_display(self.format_number(res))
        self.stored_value = res
        self.new_entry = True

    def on_equals(self, event):
        if self.pending_op:
            self.calculate()
            self.pending_op = None
            self.stored_value = None

    def on_key_down(self, event):
        key = event.GetKeyCode()
        
        if key == wx.WXK_TAB:
            self.on_base_char_hook(event)
            return
            
        unicode_char = chr(event.GetUnicodeKey()) if event.GetUnicodeKey() != 0 else ''
        
        if unicode_char.isdigit():
            self.on_digit(unicode_char)
        elif unicode_char in ['.', ',']:
            self.on_decimal(None)
        elif unicode_char == '+':
            self.on_operator("+")
        elif unicode_char == '-':
            self.on_operator("-")
        elif unicode_char == '*':
            self.on_operator("×")
        elif unicode_char == '/':
            self.on_operator("÷")
        elif key in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            self.on_equals(None)
        elif key == wx.WXK_BACK:
            self.on_backspace(None)
        elif key == wx.WXK_ESCAPE:
            self.on_c(None)
        else:
            event.Skip()

