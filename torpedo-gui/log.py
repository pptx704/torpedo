from tkinter import *
import tkinter as tk
from tkinter import (
    ttk,
    filedialog as fd,
)

from .utils import (
    Section,
    BASE_FONT
)

from datetime import datetime
from random import randint as rand

class LogSection(Section):
    def add_widgets(self):
        # Top label
        Label(
            self,
            text = "Logs",
            font = BASE_FONT,
            bg = 'white'
        ).place(x=0, y=0, height=25, width=400)

        # Clear log button
        self.clear_log_button =  Button(
            self,
            text = "Clear Logs",
            font = BASE_FONT,
            command = self.clear_log
        )
        self.clear_log_button.place(x=12, y=37, height=25, width=100)
        self.clear_log_button['state'] = DISABLED

        # Log listbox
        self.logs = Variable(self)
        self.log_listbox = Listbox(
            self,
            font = BASE_FONT,
            listvariable = self.logs,
        )
        self.log_listbox.place(x=12, y=74, height=214, width=376)

    def log(self, message):
        self.log_listbox.insert(
            END,
            f"{datetime.now().strftime('%H:%M:%S')} -> {message}"
        )
        self.log_listbox.see(END)
        self.clear_log_button['state'] = NORMAL

    def clear_log(self):
        self.log_listbox.delete(0, END)
        self.clear_log_button['state'] = DISABLED