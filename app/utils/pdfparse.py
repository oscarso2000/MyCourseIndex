import os
import io
import re

import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.pdftypes import PDFStream, PDFObjRef, resolve1, stream_value
from pdfminer.utils import isnumber
import xmltodict
from tqdm import tqdm
import boto3
from botocore.exceptions import ClientError

# Perform layout analysis for all text
laparams = pdfminer.layout.LAParams()
setattr(laparams, 'all_texts', True)


ESC_PAT = re.compile(r'[\000-\037&<>()"\042\047\134\177-\377]')


def escape_str(s):
    if isinstance(s, bytes):
        s = str(s, 'latin-1')
    return ESC_PAT.sub(lambda m: '&#%d;' % ord(m.group(0)), s)


def dumpxml(out, obj, codec=None):
    if obj is None:
        out += '<null />'
        return

    if isinstance(obj, dict):
        out += '<dict size="{}">\n'.format(len(obj))
        for (k, v) in obj.items():
            out += '<key>{}</key>\n'.format(k)
            out += '<value>'
            dumpxml(out, v)
            out += '</value>\n'
        out += '</dict>'
        return out

    if isinstance(obj, list):
        out += '<list size="{}">\n'.format(len(obj))
        for v in obj:
            dumpxml(out, v)
            out += '\n'
        out += '</list>'
        return out

    if isinstance(obj, ((str,), bytes)):
        out += '<string size="{}">{}</string>'.format(len(obj), e(obj))
        return out

    if isinstance(obj, PDFStream):
        if codec == 'raw':
            out += obj.get_rawdata()
        elif codec == 'binary':
            out += obj.get_data()
        else:
            out += '<stream>\n<props>\n'
            dumpxml(out, obj.attrs)
            out += '\n</props>\n'
            if codec == 'text':
                data = obj.get_data()
                out += '<data size="{}">{}</data>\n'.format(len(data), e(data))
            out += '</stream>'
        return out

    if isinstance(obj, PDFObjRef):
        out += '<ref id="{}" />'.format(obj.objid)
        return out

    if isinstance(obj, PSKeyword):
        out += '<keyword>{}</keyword>'.format(obj.name)
        return out

    if isinstance(obj, PSLiteral):
        out += '<literal>{}</literal>'.format(obj.name)
        return out

    if isnumber(obj):
        out += '<number>{}</number>'.format(obj)
        return out

    raise TypeError(obj)



def extract_TOC(pdf_path):
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, b"")
    pages = {page.pageid: pageno for (pageno, page)
             in enumerate(PDFPage.create_pages(document), 1)}
    
    def resolve_dest(dest):
        if isinstance(dest, str):
            dest = resolve1(document.get_dest(dest))
        elif isinstance(dest, PSLiteral):
            dest = resolve1(document.get_dest(dest.name))
        if isinstance(dest, dict):
            dest = dest['D']
        if isinstance(dest, PDFObjRef):
            dest = dest.resolve()
        return dest
    
    toc = ""

    try:
        outlines = document.get_outlines()
        toc += '<outlines>\n'
        for (level, title, dest, a, se) in outlines:
            pageno = None
            if dest:
                dest = resolve_dest(dest) # Very imperative and can cause errors that are hard to debug since we overwrite
                pageno = pages[dest[0].objid]
            elif a:
                action = a
                if isinstance(action, dict):
                    subtype = action.get("S")
                    if subtype and repr(subtype) == "/'GoTo'" and action.get("D"):
                        dest = resolve_dest(action.get("D"))
                        pageno = pages[dest[0].objid]
            string = escape_str(title).encode("utf-8", "xmlcharrefreplace")
            toc += '<outline level="{!r}" title="{}">\n'.format(level, string)
            if dest is not None:
                toc += "<dest>"
                toc = dumpxml(toc, dest)
                toc += "</dest>\n"
            if pageno is not None:
                toc += "<pageno>{}</pageno>\n".format(pageno)
            toc += "</outline>\n"
        toc += "</outlines>\n"
    except PDFNoOutlines:
        pass
    
    parser.close()
    fp.close()
    return toc


def parse_TOC(pdf_path, doc_name):
    toc_str = extract_TOC(pdf_path)
    start_idx = []
    end_idx = []
    new_doc_names = []
    start_lst_empty = True

    if toc_str:
        toc_xml = xmltodict.parse(toc_str)
    else:
        toc_xml = {"outlines": {"outline": [{"pageno": 99999999999, "@title": ""}]}}

    for outline in toc_xml["outlines"]["outline"]:
        if start_lst_empty:
            start_idx.append(outline["pageno"])
            new_doc_names.append(doc_name + "_" + outline["@title"][2:-1])
            start_lst_empty = False
        else:
            end_idx.append(outline["pageno"])
            start_idx.append(outline["pageno"])
            new_doc_names.append(doc_name + "_" + outline["@title"][2:-1])
    
    return start_idx, end_idx, new_doc_names


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

    
def make_pdf_to_txt(pdf_path, doc_name):
    start_idx, end_idx, new_doc_names = parse_TOC(pdf_path, doc_name)
    for i in tqdm(range(len(start_idx))):
        new_filename = new_doc_names[i].replace("/", "-").replace(" ", "_") + ".txt"
        new_path = os.path.join("zumbTest", new_filename)
        fp = open(new_path, "w")
        if i < len(start_idx) -1:
            print(extract_text_from_pdf(pdf_path,int(start_idx[i]), int(end_idx[i])), file=fp)
        else:
            print(extract_text_from_pdf(pdf_path,int(start_idx[i]),9999999), file=fp)
        fp.close()
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(new_path, "cs4300-data-models", new_path)
        except ClientError as e:
            return "ERROR {}".format(e.msg)
        os.system("rm -rf {}".format(new_path))
