from os import path

snippet_text_1 = """Hello,

This is a demo text snippet. It does have any sort of variable.
So ultimately whatever we write here will be sent to people without any change.

Thank you
"""

snippet_text_2 = """Hello {{ Name }},

This is a demo text snippet. It contains variables. 
So the mail body will be changed for each individual.

This message was sent to {{ Username }}, aged {{ Age }} 
If you are not the recipient, reply to this email.

Thank you
"""

snippet_text_3 = path.join(path.dirname(__file__), 'files', 'imaginary file.txt')

snippet_html_1 = """Hello,
<br><br>
This is a demo text snippet. It does have any sort of variable.<br>
So ultimately whatever we write here will be sent to people without any change.<br>
<br>
Thank you
"""

snippet_html_2 = """Hello {{ Name }},
<br><br>
This is a demo text snippet. It contains variables.<br>
So the mail body will be changed for each individual.
<br><br>
This message was sent to </i>{{ Username }}</i>, aged <i>{{ Age }}</i><br> 
If you are not the recipient, reply to this email.
<br><br>
Thank you
"""