from .template import SnippetParsingError

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import re
from csv import DictReader


class Binder:
    """
    This class uses a mailtorpedo.reader.Reader object and a mailtorpedo.template.Template 
    object and creates an iterable object containing tuples, each having an email addresses 
    and a email.mime.multipart.MimeMultipart object when told.
    """
    def __init__(self, reader, template):
        """
        reader: mailtorpedo.reader.CSVReader or mailtorpedo.reader.ExcelReader instance
        template: mailtorpedo.template.Teamplate instance
        """
        self.reader = reader
        self.template = template
        self._set_type()

    def _set_type(self):
        """
        Decides whether the mailbody needs to be modified for each individual or not.

        Returns None
        """
        for snippet in self.template.snippets:
            if snippet.type in ("plain", "html"):
                if self.reader.check_template(snippet):
                    break

        if self.reader.is_required():
            self.type = "solo"  # for individually modified
        else:
            self.type = "bulk"  # for unmodified

    def parse(self):
        """
        Creates a email.mime.multipart.MimeMultipart instance for each associated email
        address in self.reader object.
        
        Returns iterable containing tuples each having an email address and assosicated
        mime object.
        """
        reader = self.reader.parsed_dict()
        for row in reader:
            mime = MIMEMultipart()
            for snippet in self.template.snippets:
                if snippet.type in ("plain", "html"):
                    snippet_content = snippet.content
                    if self.type == 'solo':
                        for header in self.reader.headers:
                            snippet_content = re.sub(
                                f"{{{{ {header} }}}}", row[header], snippet_content
                            )
                    content = MIMEText(snippet_content, snippet.type)
                    mime.attach(content)
            mime["Subject"] = self.template.subject
            mime["To"] = row[self.reader.email_field]
            yield (row[self.reader.email_field], mime)

    def add_attachments(self, mime):
        for snippet in self.template.snippets:
            if snippet.type in ("plain", "html"):
                continue
            if snippet.type == "image":
                with open(snippet.content, "rb") as img:
                    content = MIMEImage(img.read())
                    content.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=snippet.content.split("/")[-1],
                    )
            elif snippet.type == "audio":
                with open(snippet.content, "rb") as audio:
                    content = MIMEAudio(audio.read())
                    content.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=snippet.content.split("/")[-1],
                    )
            elif snippet.type == "bin":
                with open(snippet.content, "rb") as binary:
                    content = MIMEApplication(binary.read())
                    content.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=snippet.content.split("/")[-1],
                    )
            else:
                raise SnippetParsingError("Unidentified Snippet")

            mime.attach(content)
        return mime