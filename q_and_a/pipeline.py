import argparse

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import torch
from transformers import (
    BertTokenizer,
    BertForQuestionAnswering,
    AutoTokenizer,
    AutoModelForQuestionAnswering
)

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

def convert_string_to_context(file_string, length):
	context = []
	splits = file_string.split('.')
	rem = len(splits)%length
	iters = int((len(splits) - rem)/length)

	for i in range(iters):
		block = ""
		for j in range(length):
			block += splits[i*length+j] + ". "
		context.append(block)

	if rem > 0:
		block = ""
		for j in range(rem):
			block += splits[(i+1)*length+j] + ". "
		context.append(block)

	return context

def model_pick(id):
  if (id == 0):
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
  if (id == 1):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
    model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

  return tokenizer, model

def answer(model_id, context, question):
	tokenizer, model = model_pick(model_id)
 
	input_ids = []
	token_type_ids = []
	max_score = float('-inf')
	pred = ""

	for text in context:
		input_text = "[CLS] " + question + " [SEP] " + text + " [SEP]"
		if model_id == 0:

			input_ids = tokenizer.encode(input_text)
			token_type_ids = [0 if i <= input_ids.index(102) else 1 
				for i in range(len(input_ids))]
		
			start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))    
			all_tokens = tokenizer.convert_ids_to_tokens(input_ids)

		elif model_id == 1:
			input_ids = tokenizer.encode(text)
			token_type_ids = [0 if i <= input_ids.index(102) else 1 
				for i in range(len(input_ids))]
		
			start_scores, end_scores = model(torch.tensor([input_ids]))    
			all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
		
		score = (torch.max(start_scores).detach().item() + torch.max(start_scores).detach().item()) / 2
		if score > max_score:
			max_score = score
			pred =' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])

	return pred, max_score

def passed_arguments():
	parser = argparse.ArgumentParser(description="Script for inference pipeline.")
	parser.add_argument("--filepath",
											type=str,
											required=True,
											help="Path to PDF file")
											
	parser.add_argument("--context_len",
											type=int,
											required=False,
											default=1,
											help="Length of context in number of sentences")
                      
	parser.add_argument("--model",
											type=int,
											required=False,
											help="Baseline model to test on. \n0 = BERT\n1=DistilBERT")

	parser.add_argument("--question",
											type=str,
											required=False,
											help="Question to ask")


	args = parser.parse_args()
	return args


if __name__ == '__main__':
	args = passed_arguments()
	length = args.context_len
	filepath = args.filepath
	model_id = args.model
	question = args.question
	filestring = convert_pdf_to_string(filepath)
	context = convert_string_to_context(filestring, length)
	pred, score = answer(model_id, context, question)
	print("answer: ", pred)
	print("score: ", score)

  