#!/usr/bin/env python3
# coding: utf-8
import os
import math
from collections import Counter

# read lines from a txt file
def get_lines(path):
    with open(path, encoding='UTF-8') as f:
        lines = f.readlines()
        lines = [l.replace('\n', '') for l in lines]
    return lines

# calculate accuracy
def accuracy_score(pred, targ):
    if len(pred) != len(targ):
        print('error: pred and targlength mismatch')
        return 0
    else:
        match_count = 0
        for k in range(len(pred)):
            if pred[k] == targ[k]:
                match_count += 1
        return match_count / len(pred)

# replace oov characters with "-"
def clean_str(s, cedict):
    s_clean = []
    s_oov = []
    for loc, c in enumerate(list(s)):
        if c in cedict.keys():
            s_clean.append(c)
        else:
            s_clean.append('-')
            s_oov.append([loc, c])
    return ''.join(s_clean), s_oov

# load lexicon as dict
def load_lexicon(path):
    lexicon_lines = get_lines(path)
    cedict = dict()
    for l in lexicon_lines:
        temp = l.split('\t')
        cedict[temp[0]] = temp[-1].split(',')
    return cedict

def split_top_n(pred_lines):
    result = []
    sub_list = []
    for l in pred_lines:
        if l[0] != '=':
            sub_list.append(l)
        else:
            result.append(sub_list)
            sub_list = []
    return result

def get_topn_dict(res):
    r = dict()
    for k in res:
        temp = k.split('\t')
        key = temp[2]
        r[key] = 0.5*math.exp(-1*float(temp[1]))
    return r

def get_sum_res(sen,sen_inv):
    res = Counter(get_topn_dict(sen))
    res_inv = Counter(get_topn_dict(sen_inv))
    res_dict = dict(res+res_inv)
    for k in res_dict:
        res_dict[k] = -1*math.log(res_dict[k])
    return sorted(res_dict.items(), key = lambda kv:(kv[1], kv[0]))

# calculate the predictive accuracy for the marked polyphones  
def cal_polyphones_accuracy(sent_path, targ_path, N):
    sent = get_lines(sent_path)
    targ = get_lines(targ_path)
    cedict = load_lexicon('./model/lexicon.txt')

    # clean the polyphone marks and oov chars
    marks = []
    test_clean = []
    test_clean_inv = []
    oov_list = []
    for k in range(len(sent)):
        mark = sent[k].find('▁')
        s = sent[k].replace('▁', '')
        s, s_oov = clean_str(s, cedict)
        test_clean.append(s+'\n')
        test_clean_inv.append(s[::-1]+'\n')
        # add split mark "=" for between two sentences
        test_clean.append('=\n')
        test_clean_inv.append('=\n')
        oov_list.append(s_oov)
        marks.append(mark)

    # save temp input files
    with open('./temp_input.txt', 'w', encoding='UTF-8') as f:
        f.writelines(test_clean)
    with open('./temp_input_inv.txt', 'w', encoding='UTF-8') as f:
        f.writelines(test_clean_inv)

    # inference
    os.system('phonetisaurus-g2pfst --model=./model/model.fst --nbest={} --wordlist=./temp_input.txt > ./temp_output.txt'.format(str(N)))
    os.system('phonetisaurus-g2pfst --model=./model/model_inv.fst --nbest={} --wordlist=./temp_input_inv.txt > ./temp_output_inv.txt'.format(str(N)))

    # load temp results
    pred_lines = get_lines('./temp_output.txt')
    pred_lines_inv = get_lines('./temp_output_inv.txt')

    # reverse the results of the backward model
    temp_lines = []
    for l in pred_lines_inv:
        temp = l.split('\t')
        temp_lines.append(
            '\t'.join([temp[0][::-1], temp[1], ' '.join(temp[-1].split(' ')[::-1])]))
    pred_lines_inv = temp_lines

    pred_lines = split_top_n(pred_lines)
    pred_lines_inv = split_top_n(pred_lines_inv)
    
    pred = []
    for k in range(len(marks)):
        r = get_sum_res(pred_lines[k],pred_lines_inv[k])
        pred.append(r[0][0].split(' ')[marks[k]])

    print('polyphone_accuracy %:')
    print('bi_direction_weighted :', accuracy_score(pred, targ)*100)


if __name__ == '__main__':
    N = 2
    print('')
    print('------------------')
    print('dataset: g2pM-test')
    sent_path = '../../data/data_g2pm_raw/test.sent'
    targ_path = '../../data/data_g2pm_raw/test.lb'
    cal_polyphones_accuracy(sent_path, targ_path, N)

    print('')
    print('------------------')
    print('dataset: g2pM-dev')
    sent_path = '../../data/data_g2pm_raw/dev.sent'
    targ_path = '../../data/data_g2pm_raw/dev.lb'
    cal_polyphones_accuracy(sent_path, targ_path, N)
    print('')
