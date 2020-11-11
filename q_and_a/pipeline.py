import argparse

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def convert_pdf_to_string(file_path):

	output_string = StringIO()
	with open(file_path, 'rb') as in_file:
	    parser = PDFParser(in_file)
	    doc = PDFDocument(parser)
	    rsrcmgr = PDFResourceManager()
	    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	    interpreter = PDFPageInterpreter(rsrcmgr, device)
	    for page in PDFPage.create_pages(doc):
	        interpreter.process_page(page)
	text = output_string.getvalue()
	text = text.replace('\x0c','')
	text = text.replace('\xa0','')
	text = text.replace('\n','')
	text = text.replace('ﬀ', 'ff') # double f's seem to get messed up a lot?
	return(text)

def convert_string_to_json(file_string):
	file_json = {}
	print(file_string.split('.'))

	return file_json

def passed_arguments():
	parser = argparse.ArgumentParser(description="Script for inference pipeline.")
	parser.add_argument("--filepath",
											type=str,
											required=False,
											help="Path to PDF file")
                      
	parser.add_argument("--model",
											type=int,
											required=False,
											help="Baseline model to test on. \n0 = BERT\n1=DistilBERT")

	parser.add_argument("--data_path",
											type=str,
											required=False,
											help="Path to evaluation dataset")

	parser.add_argument("--impossible_on",
											type=int,
											required=False,
											help="0: no impossible questions\n1: impossible questions")

	args = parser.parse_args()
	return args


if __name__ == '__main__':
   args = passed_arguments()
   filepath = args.filepath
   filestring = convert_pdf_to_string(filepath)
   convert_string_to_json(filestring)

  