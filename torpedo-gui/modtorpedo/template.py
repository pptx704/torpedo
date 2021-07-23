import os
import pathlib
from bs4 import BeautifulSoup

from .utils import (
    audio_extensions,
    image_extensions,
    common_file_extensions,
    disallowed_file_extensions,
)


class SnippetParsingError(Exception):
    pass


class Template:
    """
    This class is responsible for having all the information that will be
    used for generating mimes for each email address later on.
    """
    def __init__(self, subject):
        """
        subject: str
            Subject of the emails that will be sent.
        """
        self.snippets = []
        self.subject = subject

    def add_snippet(self, *args):
        """
        Takes mailtorpedo.template.Snippet objects as argument and adds
        them to self.snippets for future referencing.
        
        *args: mailtorpedo.template.Snippet instances

        Returns None
        """
        for snippet in list(args):
            if snippet.type in ("plain", "html"):
                if any(i.type == snippet.type for i in self.snippets):
                    raise SnippetParsingError(
                        f"Another {snippet.type} MIMEType already present."
                    )
            self.snippets.append(snippet)


class Snippet:
    """
    This class contains one specific type of object that will be
    sent through the emails later on. Snippet might be plaintext
    or html that will be used as email body, or files that will
    be attached with the emails. Plaintext and HTML can be
    personalized for all, whereas the attachments will be the 
    same for each individual.
    """
    def __init__(self, content, snippet_type=None):
        """
        content: str
            Can be file path which will be sent as attachment with
            the emails, or plaintext or html that will be sent as
            email body.
        snippet_type (optional): str
            Can be used if user needs to specify the type of snippet.
            For example a audio file with an extension not present in
            the package's known extensions.
            
            snippet_type can be the following:
                image -> Image files
                audio -> Audio files
                bin -> Any other file attachments
                plain -> Plain text
                html -> HTML

            Use the following statements for file extension reference:
                print(mailtorpedo.utils.image_extensions)
                    For known image extensions
                print(mailtorpedo.utils.audio_extensions)
                    For known audio extensions
                print(mailtorpedo.utils.common_file_extensions)
                    For known file extensions
                print(mailtorpedo.utils.disallowed_file_extensions)
                    For files not allowed to be sent over email
        """
        self.content = content
        if not snippet_type and os.path.exists(self.content):
            if content.split(".")[-1] in image_extensions:
                self.type = "image"
            elif content.split(".")[-1] in audio_extensions:
                self.type = "audio"
            elif content.split(".")[-1] in common_file_extensions:
                self.type = "bin"
            elif content.split(".")[-1] in disallowed_file_extensions:
                raise SnippetParsingError("Filetype not allowed")
        elif not snippet_type:
            if bool(BeautifulSoup(self.content, "html.parser").find()):
                self.type = "html"
            else:
                self.type = "plain"
        else:
            self.type = snippet_type
