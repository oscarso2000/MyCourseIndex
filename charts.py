#creates the 2 charts for p2
#Data structure:
#{nr: {  
#   folders: [],
#   question: {"word": frequency},
#   s_answer: {"word": frequency},
#   i_answer: {"word": frequency} }}


import matplotlib.pyplot as plt 
import numpy as np

sample_dict = {100: {"folders": ['hw1', 'hw2'],
                    "question": {"how": 3, "know": 4, "the": 2},
                    "s_answer": {"system": 5, "fail": 2},
                    "i_answer": {"system": 1, "fail": 3, "but": 2}},
                101: {"folders": ['hw1'],
                    "question": {"know": 2, "the": 2},
                    "s_answer": {},
                    "i_answer": {"whole": 1}},
                102: {"folders": ['hw3'],
                    "question": {"how": 1, "the": 2},
                    "s_answer": {"what": 5, "fail": 2, "the": 2},
                    "i_answer": {}}}

#Chart 1:
#skewed histogram of how we chose key words
#note: docs are equivalent to tags/folders

def build_inverted_index(nrs):
    """ Builds an inverted index from the messages."""
    folders = set()
    result = {}
    for nr, nr_dict in nrs.items():
        folder = nr_dict["folders"]
        for word_freq in [nr_dict["question"], nr_dict["s_answer"], nr_dict["i_answer"]]:
            for word, freq in word_freq.items():
                for fold in folder:
                    if fold not in folders:
                        folders.add(fold)
                    if word in result:
                        if fold in result[word]:
                            result[word][fold] += freq
                        else:
                            result[word][fold] = freq
                    else:
                        result[word] = {fold: freq}
    for word, fold_freq in result.items():
        result[word] = list(fold_freq.items())
    return result, folders

#Note: these defaults don't prune any words
def compute_idf(inv_idx, n_docs, min_df=1, max_df_ratio=1.0):
    """ Compute term IDF values from the inverted index.
    Words that are too frequent or too infrequent get pruned."""
    # YOUR CODE HERE
    idf = {}
    max_df = max_df_ratio * n_docs
    for key, value in inv_idx.items():
        df = len(value)
        if df >= min_df and df <= max_df:
            #don't need +1 in denominator because we won't have any empty lists
            idf[key] = round(np.log2(n_docs / df), 2)
    return idf

inv_idx, folders = build_inverted_index(sample_dict)
n_docs = len(folders)
idf = compute_idf(inv_idx, n_docs)
idf = {k: v for k, v in sorted(idf.items(), key=lambda item: item[1], reverse=True)}
x = np.arange(len(idf.keys()))
plt.bar(x, list(idf.values()))
plt.xticks(x, list(idf.keys()))
plt.xlabel("Word")
plt.ylabel("IDF")
plt.title("IDF vs word")
plt.savefig("sample_idf.png")
plt.cla()


#Chart 2:
# #histogram by folder tag with key words

# set height of bar
heights = {}
for folder in folders:
    heights[folder] = [0 for i in range(len(inv_idx))]

#idf is sorted
key_order = list(idf.keys())
for word, folder_freq in inv_idx.items():
    for folder, freq in folder_freq:
        heights[folder][key_order.index(word)] += freq

heights = {k: v for k, v in sorted(heights.items(), key=lambda item: item[0])}

 # set width of bar
barWidth = 0.25

r = np.arange(len(inv_idx))
# Make the plot
for idx, (tag, bars) in enumerate(heights.items()):
    curr_x = [x + idx * barWidth for x in r]
    plt.bar(curr_x, bars, width=barWidth, edgecolor='white', label=tag)
 
# Add xticks on the middle of the group bars
plt.xlabel('Word')
plt.xticks([r + (barWidth * (len(folders) - 1) / 2) for r in range(len(curr_x))], key_order)
 
# Create legend & Show graphic
plt.legend()
plt.ylabel("Frequency within Folder")
plt.title("Word Frequency within Folders")
plt.savefig("sample_tag_word_freq.png")
plt.cla()

