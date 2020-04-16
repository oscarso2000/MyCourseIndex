import io

import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

# Perform layout analysis for all text
laparams = pdfminer.layout.LAParams()
setattr(laparams, 'all_texts', True)


def extract_TOC(pdf_path):
    fp = open('mypdf.pdf', 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, password)
    # Get the outlines of the document.
    outlines = document.get_outlines()
    TOC = []
    for (level,title,dest,a,se) in outlines:
        TOC.append((level,title,dest,a,se))
    return TOC


# Note this is very inefficient but who cares it's only done once.
def extract_text_from_pdf(pdf_path, start_page, end_page):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        idx = 0
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            if idx >= start_page and idx <= end_page:
                page_interpreter.process_page(page)
            else:
                pass
            
            idx += 1

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text
