#this file will preprocess the data
#jek343

import json
import matplotlib.pyplot as plt

with open('sample_data.json', 'r') as f:
    data_dict = json.load(f)['data']

#data_dict is a list of 100 posts
#each post is a dictionary with the following keys:
# 'folders', 'nr', 'data', 'created', 'bucket_order', 'no_answer_followup', 
# 'change_log', 'bucket_name', 'history', 'type', 'tags', 'tag_good', 'unique_views', 
# 'children', 'tag_good_arr', 'id', 'config', 'status', 'request_instructor', 
# 'request_instructor_me', 'bookmarked', 'num_favorites', 'my_favorite', 'is_bookmarked', 
# 'is_tag_good', 'q_edits', 'i_edits', 's_edits', 't', 'default_anonymity'

#ADD MEANING OF EACH OF THE KEYS ABOVE
#nr - unique post number used in url


#Converting to a super simple data structure with very little remaining info.
#Here is the layout of the data structure:
#{nr:   
#   folders: [],
#   question: "",
#   s_answer: "",
#   i_answer: "" }

simple_dict = {}

for post in data_dict:
    post_id = post['nr']
    folders = post['folders']
    question = post['history'][0]['content']
    s_answer = ""
    i_answer = ""
    for answer in post['children']:
        if answer['type'] == "i_answer":
            i_answer = answer['history'][0]['content']
        elif answer['type'] == "s_answer":
            s_answer = answer['history'][0]['content']

    simple_dict[post_id] = {"folders": folders, "question": question, "s_answer": s_answer, "i_answer": i_answer}
    



