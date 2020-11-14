import torch
from transformers import (
    BertTokenizer,
    BertForQuestionAnswering,
)
# 1
tokenizer = BertTokenizer \
    .from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering \
    .from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
#2
question, text = "What day is it today?", "My name is Mike and I live in Ithaca."
input_text = "[CLS] " + question + " [SEP] " + text + " [SEP]"
#3
input_ids = tokenizer.encode(input_text)
token_type_ids = [0 if i <= input_ids.index(102) else 1
    for i in range(len(input_ids))]
#4
start_scores, end_scores = model(torch.tensor([input_ids]), \
    token_type_ids=torch.tensor([token_type_ids]))
#5
all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
print(' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1]))