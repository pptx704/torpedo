from tkinter import *
import tkinter as tk
from tkinter import (
    ttk,
    filedialog as fd,
)

from .utils import (
    Section,
    BASE_FONT,
    image_extensions,
    audio_extensions,
    binary_extensions
)

class AttachmentSection(Section):
    def add_widgets(self):
        # Top Label
        Label(
            self,
            text = "Attachments",
            font = BASE_FONT,
            bg = 'white'
        ).place(x=0, y=0, height=25, width=400)

        # Add attachment button
        Button(
            self,
            text = "Add Attachments",
            font = BASE_FONT,
            command = self.add_attachments
        ).place(x=12, y=37, height=25, width=117)

        # Remove attachment button
        self.remove_attachment_button = Button(
            self,
            text = "Remove",
            font = BASE_FONT,
            command = self.remove_attachment,
            state = DISABLED
        )
        self.remove_attachment_button.place(x=141, y=37, height=25, width=117)

        # clear all attachment
        self.clear_attachment_button = Button(
            self,
            text = "Clear All",
            font = BASE_FONT,
            command = self.clear_attachments
        )
        self.clear_attachment_button.place(x=270, y=37, height=25, width=117)
        self.clear_attachment_button['state'] = DISABLED

        # Attachment listbox
        self.attachments = Variable(self)
        self.attachment_listbox = Listbox(
            self,
            font = BASE_FONT,
            listvariable = self.attachments
        )
        self.attachment_listbox.bind('<<ListboxSelect>>', self.invoke_remove_button)
        self.attachment_listbox.place(x=12, y=74, height=212, width=376)
        
    def add_attachments(self):
        filetypes = (
            ('Image Files', image_extensions),
            ('Audio Files', audio_extensions),
            ('Other Files', binary_extensions)
        )
        filenames = fd.askopenfilenames(
            title = 'Add Attachments',
            filetypes = filetypes
        )
        for filename in filenames:
            if not filename in self.attachments.get():
                self.attachment_listbox.insert(END, filename)

        self.attachment_listbox.see(END)
        self.clear_attachment_button['state'] = ACTIVE

    def invoke_remove_button(self, event):
        self.remove_attachment_button['state'] = NORMAL

    def remove_attachment(self):
        index = self.attachment_listbox.curselection()
        self.attachment_listbox.delete(index)
        self.remove_attachment_button['state'] = DISABLED
        if len(self.attachments.get()) == 0:
            self.clear_attachment_button['state'] = DISABLED

    def clear_attachments(self):
        self.attachment_listbox.delete(0, END)
        self.clear_attachment_button['state'] = DISABLED
        self.remove_attachment_button['state'] = DISABLED