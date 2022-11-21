import params
from utils.utils import read_all_lines
from online_searching.gg_translator.google_translation import google_translate


def translate_leftover():
    google_translate(params.LELFOVER_ALL_PHRASE_FILE, params.LELFOVER_ALL_PHRASE_TRANSLATED_FILE)

def translate_header():
    google_translate(params.JADER_ALL_HEADER_FILE, params.JADER_ALL_HEADER_TRANSLATION_FILE)

def translate_missing():
    google_translate(params.MISSING_FILE, params.MISSING_TRANS_FIX_FILE)

def load_leftover_map(d=None, capitalized=True):
    if d is None:
        d = dict()
    lines_inp = read_all_lines(params.LELFOVER_ALL_PHRASE_FILE)
    lines_trans = read_all_lines(params.LELFOVER_ALL_PHRASE_TRANSLATED_FILE)
    assert len(lines_inp) == len(lines_trans)
    start_id = 0
    if lines_inp[0] == "":
        start_id = 1
    for i in range(start_id, len(lines_trans)):
        translated_word = lines_trans[i]
        if capitalized:
            translated_word = translated_word.capitalize()
        d[lines_inp[i]] = translated_word
    # print(d)
    return d

def load_header_map():
    d = dict()
    l = []
    lines_inp = read_all_lines(params.JADER_ALL_HEADER_FILE)
    lines_trans = read_all_lines(params.JADER_ALL_HEADER_TRANSLATION_FILE)
    for i in range(len(lines_trans)):
        d[lines_inp[i]] = lines_trans[i]
        l.append(lines_trans[i])

    return d, l

def load_fixing_map():
    d = dict()
    try:
        lines_inp = read_all_lines(params.MISSING_FILE)
        lines_trans = read_all_lines(params.MISSING_TRANS_FIX_FILE)
        for i in range(len(lines_trans)):
            d[lines_inp[i]] = lines_trans[i]
    except:
        print("Warning: No fixing map found.")


    return d
if __name__ == "__main__":
    translate_leftover()
    translate_header()
