#!/usr/bin/env python3
# coding: utf-8
import os

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

# calculate the predictive accuracy for the marked polyphones  
def cal_polyphones_accuracy(sent_path, targ_path):
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
        oov_list.append(s_oov)
        marks.append(mark)

    # save temp input files
    with open('./temp_input.txt', 'w', encoding='UTF-8') as f:
        f.writelines(test_clean)
    with open('./temp_input_inv.txt', 'w', encoding='UTF-8') as f:
        f.writelines(test_clean_inv)

    # inference
    os.system('phonetisaurus-g2pfst --model=./model/model.fst --nbest=1 --wordlist=./temp_input.txt > ./temp_output.txt')
    os.system('phonetisaurus-g2pfst --model=./model/model_inv.fst --nbest=1 --wordlist=./temp_input_inv.txt > ./temp_output_inv.txt')

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

    # generate final prediction of polyphones
    pred_forward = []
    pred_backward = []
    pred_bi_direction = []

    for k in range(len(pred_lines)):
        temp = pred_lines[k].split('\t')
        temp_inv = pred_lines_inv[k].split('\t')

        # for the forward and backward models
        # directly extract their corresponding phones
        pred_forward.append(temp[-1].split(' ')[marks[k]])
        pred_backward.append(temp_inv[-1].split(' ')[marks[k]])

        # for the bi-directional model
        # choose the one with lower -log score (higher probability)
        if float(temp[1]) < float(temp_inv[1]):
            pred_bi_direction.append(temp[-1].split(' ')[marks[k]])
        else:
            pred_bi_direction.append(temp_inv[-1].split(' ')[marks[k]])

    print('polyphone_accuracy %:')
    print('forward      :', accuracy_score(pred_forward, targ)*100)
    print('backward     :', accuracy_score(pred_backward, targ)*100)
    print('bi_direction :', accuracy_score(pred_bi_direction, targ)*100)


if __name__ == '__main__':
    print('')
    print('------------------')
    print('dataset: g2pM-test')
    sent_path = '../../data/data_g2pm_raw/test.sent'
    targ_path = '../../data/data_g2pm_raw/test.lb'
    cal_polyphones_accuracy(sent_path, targ_path)

    print('')
    print('------------------')
    print('dataset: g2pM-dev')
    sent_path = '../../data/data_g2pm_raw/dev.sent'
    targ_path = '../../data/data_g2pm_raw/dev.lb'
    cal_polyphones_accuracy(sent_path, targ_path)
    print('')
