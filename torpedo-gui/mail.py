from tkinter import *
import tkinter as tk
from tkinter import (
    ttk,
    filedialog as fd,
)
from .utils import (
    Section,
    BASE_FONT,
    EXCEL_FILES,
    CSV_FILES
)

from .modtorpedo import (
    CSVReader,
    ExcelReader,
    Template,
    Snippet,
    Sender
)

import threading
import json

class PasswordManager(Tk):
    def __init__(self, master):
        super(PasswordManager, self).__init__()
        self.master_frame = master
        self.add_credentials_widgets()

    def add_credentials_widgets(self):
        # label username
        Label(
            self,
            text = "Email",
            font = BASE_FONT
        ).place(x=12, y=12, height=25, width=75)

        # Username Entry
        self.username = Entry(
            self,
            font=BASE_FONT
        )
        self.username.place(x=99, y=12, height=25, width=220)

        # Label password
        Label(
            self,
            text = "Password",
            font = BASE_FONT,
        ).place(x=12, y=49, height=25, width=75)

        # Password Entry
        self.password = Entry(
            self,
            font = BASE_FONT,
            show = '*'
        )
        self.password.place(x=99, y=49, height=25, width=220)

        # Label SMTP
        Label(
            self,
            text = "SMTP",
            font = BASE_FONT
        ).place(x=12, y=86, height=25, width=75)

        # SMTP Entry
        self.smtp = Entry(
            self,
            font=BASE_FONT
        )
        self.smtp.place(x=99, y=86, height=25, width=220)
        self.smtp.insert(0, "smtp.gmail.com")

        # Label PORT
        Label(
            self,
            text = "PORT",
            font = BASE_FONT
        ).place(x=12, y=123, height=25, width=75)

        # PORT entry
        self.port = Entry(
            self,
            font = BASE_FONT
        )
        self.port.place(x=99, y=123, height=25, width=220)
        self.port.insert(0, '587')

        # Button
        Button(
            self,
            text = "Save",
            font = BASE_FONT,
            command = self.save_creds
        ).place(x=130, y = 160, height=25, width=71)

    def save_creds(self):
        filename = False
        while not filename:
            filename = fd.asksaveasfilename(
                title = "Save credentials",
                filetypes=(('json', '*.json'),),
                defaultextension="*.json"
            )
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump({
                'HOST': self.smtp.get(),
                'PORT': self.port.get(),
                'USER': self.username.get(),
                'PASSWORD': self.password.get()
            }, file, indent=4)
        
        self.master_frame.credfilename['state'] = NORMAL
        self.master_frame.credfilename.delete(0, END)
        self.master_frame.credfilename.insert(0, filename)
        self.master_frame.credfilename['state'] = 'readonly'
        self.destroy()

class MailSection(Section):
    def add_widgets(self):
        # Title
        Label(
            self,
            text = "Mail",
            font = BASE_FONT,
            bg = 'white'
        ).place(x=0, y=0, height=25, width=600)

        # DB Label
        Label(
            self,
            text = "Database",
            font = BASE_FONT
        ).place(x=12, y=37, height=25, width=75)

        # DB Entry (Disabled)
        self.dbfilename = ttk.Entry(
            self,
            state = 'readonly',
            font = BASE_FONT,
            style = 'pad.TEntry'
        )
        self.dbfilename.place(x=99, y=37, height=25, width=262)
        
        # DB Browse button
        Button(
            self,
            text = "Browse",
            command = self.open_dbfile,
            font = BASE_FONT
        ).place(x=361, y=38, height=25, width=75)

        # Database sheet options
        self.db_sheet = StringVar(self)
        self.db_sheet.set('Worksheet')

        self.db_sheet_options = OptionMenu(
            self,
            self.db_sheet,
            []
        )
        self.db_sheet_options['state'] = 'disabled'
        self.db_sheet_options.place(x=448, y=37, height=25, width=112)

        # Email Field label
        Label(
            self,
            text = "Email Column",
            font = BASE_FONT
        ).place(x=12, y=74, height=25, width=100)

        # Email Field Options
        self.email_field_name = StringVar(self)
        self.email_field_name.set('Email Column')

        self.email_field_options = OptionMenu(
            self,
            self.email_field_name,
            []
        )
        self.email_field_options.place(x=124, y=74, height=25, width=120)
        self.email_field_options['state'] = DISABLED

        # Finalize Button
        Button(
            self,
            text = "Process Emails",
            command = self.finalize,
            font = BASE_FONT
        ).place(x=448, y=74, height=25, width=112)


        # Subject Label
        Label(
            self,
            text = "Subject",
            font = BASE_FONT
        ).place(x=12, y=110, height=25, width=100)

        # Subject Field
        self.email_subject = ttk.Entry(
            self,
            font = BASE_FONT,
            style = 'pad.TEntry',
        )
        self.email_subject.place(x=124, y=110, height=25, width=436)

        self.header_buttons = list()

        # Email Body
        self.email_body = Text(
            self,
            font = (BASE_FONT[0], 12),
        )
        self.email_body['fg'] = 'grey'
        self.email_body.place(x=12, y = 148, height=364, width=548)
        self.email_body.insert(0.0, "Email body here. Use buttons to insert variables easily.")
        self.email_body.bind('<Button-1>', self.clear_email_body)

        # Credentials
                # DB Label
        Label(
            self,
            text = "Credentials",
            font = BASE_FONT
        ).place(x=12, y=524, height=25, width=100)

        # Credentials Entry (Disabled)
        self.credfilename = ttk.Entry(
            self,
            state = 'readonly',
            font = BASE_FONT,
            style = 'pad.TEntry'
        )
        self.credfilename.place(x=124, y=524, height=25, width=262)
        
        # Credentials browse button
        Button(
            self,
            text = "Browse",
            command = self.open_credfile,
            font = BASE_FONT
        ).place(x=386, y=525, height=25, width=75)

        # Credentials create button
        Button(
            self,
            text = "Create",
            command = self.create_credentials,
            font = BASE_FONT
        ).place(x=473, y=525, height=25, width=87)

        # Send Button
        self.sendbutton = Button(
            self,
            text = "Send",
            #command = self.create_credfile,
            font = BASE_FONT,
            state = DISABLED,
            command = self.send_mails
        )
        self.sendbutton.place(x=12, y=562, height=25, width=75)

        # Stop Button
        self.resumebutton = Button(
            self,
            text = "Resume",
            #command = self.create_credfile,
            font = BASE_FONT,
            state = DISABLED,
            command = self.resume_mail
        )
        self.resumebutton.place(x=99, y=562, height=25, width=75)

        # Resume Button
        self.stopbutton = Button(
            self,
            text = "Stop",
            #command = self.create_credfile,
            font = BASE_FONT,
            state = DISABLED,
            command = self.stop_mail
        )
        self.stopbutton.place(x=186, y=562, height=25, width=75)

        # Progress bar
        self.progress = ttk.Progressbar(
            self, 
            orient = HORIZONTAL,
            length = 100,
            mode = 'determinate',
        )
        self.progress.place(x=273, y=562, height=25, width=285)

    def open_dbfile(self):
        try:  
            filetypes = (
                ('CSV Files', '*.csv *.txt'),
                ('Microsoft Excel Files', '*.xlxs *.xls *.xlr *.xls *.xlsb *.xlsm *.xlsx *.xlw')
            )

            filename = fd.askopenfilename(
                title = "Select your database file",
                filetypes= filetypes
            )

            if not filename:
                return

            self.dbfilename['state'] = NORMAL
            self.dbfilename.delete(0, END)
            self.dbfilename.insert(0, filename)
            self.dbfilename['state'] = 'readonly'

            if filename.split('.')[-1] in CSV_FILES:
                self.reader = CSVReader(filename, None)
                self.db_sheet_options['state'] = DISABLED
            elif filename.split('.')[-1] in EXCEL_FILES:
                self.reader = ExcelReader(filename, None)
                self.db_sheet_options['state'] = NORMAL
                self.db_sheet_options['menu'].delete(0, END)
                self.db_sheet.set(self.reader.workbook.sheetnames[0])
                for sheet in self.reader.workbook.sheetnames:
                    self.db_sheet_options['menu'].add_command(label=sheet, command=lambda i=sheet: self.add_sheet_multicommand(i))
            else:
                self.db_sheet_options['menu'].delete(0, END)
                self.db_sheet.set("Worksheet")
                self.db_sheet_options['state'] = DISABLED
                return

            self.add_email_fields(self.reader.headers)
            self.add_header_buttons(self.reader.headers)
        except Exception as e:
            self.log_section.log(f"Error: {e}")

    def add_email_fields(self, headers):
        try:
            self.email_field_options['state'] = NORMAL
            self.email_field_options['menu'].delete(0, END)
            self.email_field_name.set(self.reader.headers[0])
            for header in self.reader.headers:
                self.email_field_options['menu'].add_command(label=header, command=lambda i=header: self.add_email_multicommand(i))
        except Exception as e:
            self.log_section.log(f"Error: {e}")
    def add_header_buttons(self, headers):
        try:
            while self.header_buttons:
                button = self.header_buttons.pop(0)
                button.destroy()

            for i in range(len(headers)):
                mod = i%5
                div = i//5
                button = Button(
                    self,
                    text = headers[i],
                    command = lambda i=i: self.add_header_to_text(headers[i])
                )
                button.place(x = 12*(mod+1)+100*(mod), y = 160+12*(div+1)+(div-1)*25, height=25, width=100)
                self.header_buttons.append(button)
            
            self.email_body.place(x=12, y=172+25*div+12*(div+1), height=600-(172+25*div+12*(div+1))-88, width=548)
        except Exception as e:
            self.log_section.log(f"Error: {e}")

    def add_header_to_text(self, header):
        try:
            if self.email_body.get(0.0, END)[-2:-1] == " ":
                self.email_body.insert(END, f"{{{{ {header} }}}}")
            else:
                self.email_body.insert(END, f" {{{{ {header} }}}}")
        except Exception as e:
            self.log_section.log(f"Error: {e}")
    
    def clear_email_body(self, event):
        try:
            data = self.email_body.get(0.0, END)
            if data == "Email body here. Use buttons to insert variables easily.\n":
                self.email_body.delete(0.0, END)
            self.email_body['fg'] = 'black'
        except Exception as e:
            self.log_section.log(f"Error: {e}")

    def open_credfile(self):
        try:
            filetypes = (
                ('JSON Files', '*.json'),
            )

            filename = fd.askopenfilename(
                title = "Select your credential file",
                filetypes= filetypes
            )

            if not filename:
                return

            self.credfilename['state'] = NORMAL
            self.credfilename.delete(0, END)
            self.credfilename.insert(0, filename)
            self.credfilename['state'] = 'readonly'
        except Exception as e:
            self.log_section.log(f"Error: {e}")

    def change_sheet(self, sheet):
        try:
            self.reader.sheet_index = sheet
            self.reader.change_sheet(sheet)
            self.add_header_buttons(self.reader.headers)
        except Exception as e:
            self.log_section.log(f"Error: {e}")
    
    def change_email(self, email):
        self.reader.email_field = email

    def finalize(self):
        try:
            # snippet
            self.snippets = [] 
            self.snippets.append(Snippet(self.email_body.get(0.0, END)))
            # create template
            self.template = Template(self.email_subject.get())
            self.template.add_snippet(*self.snippets)
        
            # Add attachments
            snippets = [Snippet(file) for file in self.attachment_section.attachments.get()]
            self.template.add_snippet(*snippets)
        
            # Sender
            self.sender = Sender(self.credfilename.get(), self.reader, self.template, self.log_section)
            self.sender.stop_button = self.stopbutton
            self.sendbutton['state'] = NORMAL
            if self.sender.resumable():
                self.resumebutton['state'] = NORMAL
            self.log_section.log("Emails processed")

            # Progress
            self.progress['value'] = 0
        except Exception as e:
            self.log_section.log(f"Error: {e}")

    def add_email_multicommand(self, header):
        try:
            tk._setit(self.email_field_name, header)()
            self.change_email(header)
        except Exception as e:
            self.log_section.log(f"Error: {e}")

    def add_sheet_multicommand(self, sheet):
        try:
            tk._setit(self.db_sheet, sheet)()
            self.change_sheet(sheet)
            self.add_email_fields(self.reader.headers)
        except Exception as e:
            self.log_section.log(f"Error: {e}")
    
    def add_log_section(self, logsection):
        self.log_section = logsection

    def add_attachment_section(self, attachmentsection):
        self.attachment_section = attachmentsection

    def send_mails(self):
        self.log_section.log("Task initialized")
        try:
            self.sender.progressbar = self.progress
            self.sender.stop_button = self.stopbutton
            #self.sender.send()
            th = threading.Thread(target=self.sender.send)
            th.start()
            self.stopbutton['state'] = NORMAL
            self.sendbutton['state'] = DISABLED
            self.resumebutton['state'] = DISABLED
        except Exception as e:
            self.log_section.log(f"Error: {e}")
    
    def stop_mail(self):
        self.sender.should_continue = False
        self.stopbutton['state'] = DISABLED
    
    def resume_mail(self):
        self.log_section.log("Resume task initialized")
        try:
            self.sender.progressbar = self.progress
            self.sender.should_continue = True
            #self.sender.send()
            th = threading.Thread(target=self.sender.resume)
            th.start()
            self.stopbutton['state'] = NORMAL
            self.sendbutton['state'] = DISABLED
            self.resumebutton['state'] = DISABLED
        except Exception as e:
            self.log_section.log(f"Error: {e}")

    def create_credentials(self):
        self.credroot = PasswordManager(self)
        self.credroot.geometry("331x197")
        self.credroot.title("Credential Manager")