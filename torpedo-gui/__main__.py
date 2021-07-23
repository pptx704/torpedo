from tkinter import *
from tkinter import (
    font,
    ttk
)
from os import path

from .mail import MailSection
from .attachments import AttachmentSection
from .log import LogSection

def main():
    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 973
    THEME = "#6095eb"
    root = Tk()
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(0,0)
    root.title("Torpedo")
    root['bg'] = '#454545'
    icon = PhotoImage(file = path.join(path.dirname(__file__), 'icon.png'))
    root.iconphoto(False, icon)
    
    ttk.Style().configure('pad.TEntry', padding='5 1 1 5')

    mailsection = MailSection(root, 0, 0, 800, 572)
    mailsection.add_attribute(bg=THEME)
    attachmentsection = AttachmentSection(root, 573, 0, 298, 400)
    attachmentsection.add_attribute(bg=THEME)
    logsection = LogSection(root, 573, 300, 300, 400)
    logsection.add_attribute(bg=THEME)

    mailsection.add_attachment_section(attachmentsection)
    mailsection.add_log_section(logsection)

    root.mainloop()

if __name__=="__main__":
    main()
