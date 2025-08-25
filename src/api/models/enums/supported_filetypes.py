from enum import Enum


class SupportedFileType(str, Enum):
    txt = "text/plain"
    markdown = "text/markdown"
    rtf="text/rtf"
    pdf="application/pdf"
