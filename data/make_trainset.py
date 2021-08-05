#!/usr/bin/env python3
# coding: utf-8

from g2pM import G2pM
# from tqdm import tqdm
import os

# read lines from a txt file


def get_lines(path):
    with open(path, encoding='UTF-8') as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
    return lines

# get the location mark of the labeled polyphone in the g2pM dataset
# and the phones predicted by g2pM


def get_mark_phone(sentence, model):
    mark = sentence.find('▁')
    r = model(sentence.replace('▁', ''), char_split=True)
    return r[mark], r


# make dir for the generated dataset
if not os.path.exists('./data_train'):
    os.makedirs('./data_train')

model = G2pM()
cedict = model.cedict

# write the g2pM dict to the lexicon file and corpus
corpus_dict = []
lexicon = []
for k in cedict:
    ph = cedict[k]
    lexicon.append(k+'\t'+','.join(ph)+'\n')
    for p in ph:
        corpus_dict.append(k+'}'+p+'\n')

with open('./data_train/lexicon.txt', 'w', encoding='UTF-8') as f:
    f.writelines(lexicon)

with open('./data_train/aligned.corpus', 'w', encoding='UTF-8') as f:
    f.writelines(corpus_dict)
    f.writelines('-}|\n')

with open('./data_train/aligned_inv.corpus', 'w', encoding='UTF-8') as f:
    f.writelines(corpus_dict)
    f.writelines('-}|\n')

# read the training set
sent = get_lines('./data_g2pm_raw/train.sent')
targ = get_lines('./data_g2pm_raw/train.lb')

# use g2pM to convert train sentences and replace the phone of the polyphone with the label
# the corpus_inv is the corpus of the reversed senstences
corpus = []
corpus_inv = []
for k in (range(len(sent))):
    pred, r = get_mark_phone(sent[k], model)
    if pred == targ[k]:
        keys = list(sent[k].replace('▁', ''))
        vals = r
        if len(keys) == len(vals):
            kv_list = [keys[n]+'}'+vals[n] for n in range(len(keys))]
            corpus.append(' '.join(kv_list) + '\n')
            corpus_inv.append(' '.join(kv_list[::-1]) + '\n')

# write the corpus files
with open('./data_train/aligned.corpus', 'a', encoding='UTF-8') as f:
    f.writelines(corpus)

with open('./data_train/aligned_inv.corpus', 'a', encoding='UTF-8') as f:
    f.writelines(corpus_inv)
