import os

import joblib
import numpy as np
import time
import jaconv
import re

seps = {'{', '(', '「', '＜', '<', ')', '）', '＞', '」', '〕', '>', '}', ']', '/', ' ', ';', '"', '\t', '|'}
d_map_sep = {'{': '{', '(': '(', '「': '\"', '＜': "<", '<': '<', ')': ')', '）': ')', '＞': '>', '」': '\"', '〕': ')',
             '>': '>', '}': '}', ']': ']', '/': '/', ' ': ' ', ';': ';', '"': '"', '\t': '\t', '|':'|'}

def is_sep(c):
    return c in seps
def split_str(inp_str):
    inp_str = jaconv.z2h(inp_str, kana=False, digit=True, ascii=True)

    res = []
    cur_token = ""
     #print("SCX")
    for c in inp_str:
        if c in seps:
            cd = int(cur_token.isascii())
            if cd > 0:
                if cur_token.isdigit():
                    cd = 2
            if cur_token != "":
                res.append([cur_token, cd])
            re_map_c = d_map_sep[c]
            res.append([re_map_c, -1])
            cur_token = ""
        else:
            cur_token += c
    if cur_token != "":
        cd = int(cur_token.isascii())
        if cd > 0:
            if cur_token.isdigit():
                cd = 2
        # print("CC: ", cur_token, cd)
        res.append([cur_token, cd])

    return res

def merge_dict(d_list):
    d = {}
    for di in d_list:
        for k, v in di.items():
            d[k] = v
    return d
def restore_str(res, reduce=True):
    # print("Reduce", res)
    tokens = []
    prev_str = ""
    for p in res:
        # print(type(p))
        if type(p) == list:
            w, cd = p
        else:
            w = p
            cd = is_sep(w)
        # print(p, w, cd)
        if reduce:
            if cd == 0:
                if w != prev_str:
                    tokens.append(w)
                    prev_str = w
            else:
                tokens.append(w)
        else:
            tokens.append(w)
    # print("R token: ", tokens)
    return "".join(tokens)


def read_all_lines(path):
    fin = open(path)
    lines = [line.strip() for line in fin.readlines()]
    fin.close()
    return lines


def get_insert_dict(d, k, v):
    try:
        v = d[k]
    except:
        d[k] = v

    return v


def getCurrentTimeString():
    t = time.localtime()
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", t)
    return currentTime


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def convertHexToBinString888(hexString):
    # scale = 16  ## equals to hexadecimal
    # num_of_bits = 888
    return bin(int(hexString, 16))[2:].zfill(888)


def convertBinString888ToArray(binString888):
    ar = np.ndarray(888, dtype=float)
    ar.fill(0)
    for i in range(887, -1, -1):
        if binString888[i] == "1":
            ar[i] = 1
    return ar

def remove_multiple_char(s, c = ' '):
    a = re.sub(r'%s+'%c, c, s)
    return a
def convertHex888ToArray(hex888):
    return convertBinString888ToArray(convertHexToBinString888(hex888))


def get_dict(d, k, v=-1):
    try:
        v = d[k]
    except:
        pass
    return v


def get_insert_key_dict(d, k, v=0):
    try:
        v = d[k]
    except:
        d[k] = v
    return v


def add_dict_counter(d, k, v=1):
    try:
        v0 = d[k]
    except:
        v0 = 0
    d[k] = v0 + v


def sort_dict(dd):
    kvs = []
    for key, value in sorted(dd.items(), key=lambda p: (p[1], p[0])):
        kvs.append([key, value])
    return kvs[::-1]


def sum_sort_dict_counter(dd):
    cc = 0
    for p in dd:
        cc += p[1]
    return cc


def get_update_dict_index(d, k):
    try:
        current_index = d[k]
    except:
        current_index = len(d)
        d[k] = current_index
    return current_index


def get_dict_index_only(d, k):
    try:
        current_index = d[k]
    except:
        current_index = -1

    return current_index


def load_list_from_file(path):
    list = []
    fin = open(path)
    while True:
        line = fin.readline()
        if line == "":
            break
        list.append(line.strip())
    fin.close()
    return list


def reverse_dict(d):
    d2 = dict()
    for k, v in d.items():
        d2[v] = k
    return d2


def save_obj(obj, path):
    joblib.dump(obj, path)


def load_obj(path):
    return joblib.load(path)


def loadMapFromFile(path, sep="\t", keyPos=0, valuePos=1):
    fin = open(path)
    d = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split(sep)
        d[parts[keyPos]] = parts[valuePos]
    fin.close()
    return d


def loadMapSetFromFile(path, sep="\t", keyPos=0, valuePos=1, sepValue="", isStop=""):
    fin = open(path)
    dTrain = dict()

    if isStop != "":
        dTest = dict()

    d = dTrain

    while True:
        line = fin.readline()
        if line == "":
            break
        if isStop != "":
            if line.startswith(isStop):
                d = dTest
                continue
        parts = line.strip().split(sep)
        v = get_insert_key_dict(d, parts[keyPos], set())
        if sepValue == "":
            v.add(parts[valuePos])
        else:
            values = parts[valuePos]
            values = values.split(sepValue)
            for value in values:
                v.add(value)
    fin.close()
    if isStop != "":
        return dTrain, dTest
    return dTrain
