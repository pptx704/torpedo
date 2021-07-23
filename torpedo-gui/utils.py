from tkinter import (
    Frame,
    font
)


class Section(Frame):
    def __init__(self, master, x, y, height, width):
        super(Section, self).__init__(master)
        self.place(x=x, y=y, height=height, width=width)
        self.add_widgets()
    
    def add_attribute(self, **kwargs):
        for i in kwargs.keys():
            self[i] = kwargs[i]

EXCEL_FILES = (
    'xlxs', 'xls', 'xlr', 'xls', 'xlsb', 'xlsm', 'xlsx', 'xlw'
)
CSV_FILES = (
    'txt', 'csv', 'tsv'
)

BASE_FONT = ("Trebuchet MS", 10, "normal")

image_extensions = '*.3fr *.ari *.arw *.bay *.bmp *.cap *.cr2 *.cr3 *.crw *.dcr *.dcs *.dds *.dib *.dng *.drf *.eip *.emf *.erf *.fff *.gif *.ico *.ief *.iiq *.jfif *.jpe *.jpeg *.jpg *.jxr *.k25 *.kdc *.mef *.mos *.mrw *.nef *.nrw *.orf *.ori *.pbm *.pef *.pgm *.png *.pnm *.ppm *.ptx *.pxn *.raf *.ras *.raw *.rgb *.rw2 *.rwl *.sr2 *.srf *.srw *.svg *.tif *.tiff *.wdp *.webp *.wmf *.x3f *.xbm *.xpm *.xwd'
audio_extensions = '*.aac *.ac3 *.adt *.adts *.aif *.aifc *.aiff *.au *.ec3 *.flac *.lpcm *.m3u *.m4a *.mid *.midi *.mka *.mp2 *.mp3 *.mpa *.oga *.ogg *.opus *.ra *.rmi *.snd *.wav *.wax *.weba *.wma'
binary_extensions = '*.csv *.doc *.docm *.docx *.htm *.html *.ods *.odt *.pdf *.pps *.ppsm *.ppsx *.ppt *.pptm *.pptx *.rtf *.txt *.wps *.xlr *.xls *.xlsb *.xlsm *.xlsx *.xlw *.xml *.xps'
