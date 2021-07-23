import os
import re
import json
import platform
import smtplib

from time import time
from hashlib import md5
from datetime import datetime

from .binder import Binder


class Console:
    """
    This class manages the logfiles and cachefiles that are updated frequently
    when mailtorpedo.sender.Sender class continues sending emails.
    """
    def __init__(self, filepath):
        """
        filepath: Directory path (instance of str class)
        """
        self.console_name = os.path.join(filepath, f"torpedo_{int(time())}_log.txt")
        self.console = open(self.console_name, "a", encoding="utf-8")
        self.log("Created log file")
        self.cache_name = os.path.join(filepath, f"torpedo_{int(time())}_cache")

    def log(self, data):
        """
        Logs data in the log file with a message and current timestamp

        data: Instance of str class
            Message to be logged

        Returns None
        """
        self.console.write(f"\n{datetime.now()}-> {data}")

    def initialize_cache(self, file, creds):
        """
        Initializes cache file with MD5 hash of mailing list and user credentials

        file: File Path (instance of str class)
            Refers to the CSV or Excel file containing email data
        creds: dict instance

        Returns None
        """
        self.cache = open(self.cache_name, "a", encoding="utf-8")
        if platform.system() == 'Windows':
            os.system(f"attrib +h +s {self.cache_name}")

        with open(file, "rb") as binfile:
            hashvalue = md5(str(binfile.read()).encode()).hexdigest()
            self.cache.write(f"{hashvalue}\n")

        hashvalue = md5(str(creds).encode()).hexdigest()
        self.cache.write(f"{hashvalue}\n")
        self.cache.write("0")

    def update_cache(self, data):
        """
        Updates the number of mails sent

        data: instance of int class
            Number of emails sent from the related mailtorpedo.sender.Sender instance
        
        Returns None
        """
        self.cache.seek(67)
        self.cache.truncate()
        self.cache.write(str(data))

    def remove_cache(self):
        """
        Removes the cache file

        Returns None
        """
        os.remove(self.cache_name)

    def close(self):
        """
        Closes open logfile and cachefile

        Returns None
        """
        self.console.close()
        self.cache.close()


class ResumeConsole(Console):
    """
    Inherits from mailtorpedo.sender.Console class.
    Opens a previously saved logfile and cachefile and continues to edit that. 
    """
    def __init__(self, filename, filepath):
        """
        filename: File path (instance of str class)
            Name of the cache file found by mailtorpedo.sender.Sender class
        filepath: Directory path (instance of str class)
            Directory where the cache and log files are saved.
        """
        timestamp = filename.split("_")[1]
        self.console_name = os.path.join(filepath, f"torpedo_{timestamp}_log.txt")
        self.cache_name = os.path.join(filepath, f"torpedo_{timestamp}_cache")

        self.console = open(self.console_name, "a", encoding="utf-8")
        self.cache = open(self.cache_name, "a", encoding="utf-8")


class Sender:
    """
    This class combines all of the bulk emailing materials and use them to either
    send emails or resume a mail sending task that was incomplete previously.
    """

    def __init__(self, creds, reader, template):
        """
        creds: File path (instance of str class)
            File must contain a JSON having HOST, PORT, USER, PASSWORD values
        reader: mailtorpedo.reader.ExcelReader or mailtorpedo.reader.CSVReader instance
        template: mailtorpedo.template.Template instance
        """
        if not os.path.exists(creds):
            raise FileNotFoundError("Credential file not found.")
        else:
            with open(creds, "r", encoding="utf-8") as credfile:
                self.__credentials = json.loads(credfile.read())

        self.reader_path = reader.filename

        self.binder = Binder(reader, template)

    def get_server(self):
        """
        Authenticates smtplib.SMTP instance with values from self.credentials
        
        Returns the smtplib.SMTP instance
        """
        server = smtplib.SMTP(
            host=self.__credentials.get("HOST"),
            port=self.__credentials.get("PORT"),
        )
        server.starttls()
        server.login(
            user=self.__credentials.get("USER"), password=self.__credentials.get("PASSWORD")
        )

        return server

    def _send(self, console, cursor, mail_list):
        """
        Sends emails with the provided mailing list. Updates logs and caches after sending
        each email. Closes all open instances after mail sending is complete.

        console: mailtorpedo.sender.Console instance
        cursor: int
        mail_list: list instance containing tuples
            Each tuple contains a str instance and an 
            email.mime.multipart.MimeMultipart instance
        
        Returns None
        """

        server = self.get_server()
        email = self.__credentials.get("USER")

        console.log("Task Initialized")
        console.initialize_cache(self.binder.reader.filename, self.__credentials)

        while mail_list:
            receiver = mail_list.pop(0)
            try:
                mime = self.binder.add_attachments(receiver[1])
                server.sendmail(email, receiver[0], mime.as_string())
                console.log(f"Mail sent to {receiver[0]}")
                cursor += 1
                console.update_cache(cursor)
            except smtplib.SMTPServerDisconnected:
                console.log(
                    f"Server disconnected unexpectedly. Breakpoint {receiver[0]}"
                )
                console.log("Task Incomplete\n")
                break
            except Exception as e:
                console.log(
                    f"Python raised {type(e).__name__} error: {str(e)}\n. Breakpoint {receiver[0]}"
                )
                console.log("Task Incomplete\n")
                console.close()
                break
        else:
            console.log("Task Complete")
            server.quit()
            console.close()
            console.remove_cache()
    
    def resumable(self):
        """
        Finds out existing cachefiles which refers to incomplete mailing tasks.

        Returns if such cache exists
        """
        cred_sha = str(md5(str(self.__credentials).encode()).hexdigest())
        
        with open(self.binder.reader.filename, "rb") as binfile:
            list_sha = md5(str(binfile.read()).encode()).hexdigest()
        
        caches = [
            i
            for i in os.listdir(os.path.dirname(self.reader_path))
            if i.startswith("torpedo_") and i.endswith("_cache")
        ]

        for cache in caches:
            cachefile = open(
                os.path.join(os.path.dirname(self.reader_path), cache),
                "r", encoding="utf-8",
            )
            if (
                cachefile.readline().strip() == list_sha
                and cachefile.readline().strip() == cred_sha
            ):
                break
            else:
                cachefile.close()
        else:
            return False
        
        self.cachefile = cachefile
        return True

    def send(self):
        """
        Initializes a task of sending mails
        
        Returns None
        """
        console = Console(os.path.dirname(self.reader_path))

        mail_list = list(self.binder.parse())

        self._send(console, 0, mail_list)

    def resume(self):
        """
        If there is an incomplete task that matches current mailing list and credentials, 
        this function resumes the task.

        Returns None
        """
        
        if not self.resumable():
            raise Exception("Cache not found")

        cursor = int(self.cachefile.readline().split()[0])

        mail_list = list(self.binder.parse())
        for i in range(cursor):
            mail_list.pop(0)

        console = ResumeConsole(
            os.path.basename(self.cachefile.name), os.path.dirname(self.reader_path)
        )
        
        self.cachefile.close()
        console.log("Task Resumed")

        self._send(console, cursor, mail_list)
