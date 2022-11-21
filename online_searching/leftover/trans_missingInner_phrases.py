import params
from utils.utils import read_all_lines
from online_searching.gg_translator.google_translation import google_translate

def gg_trans_missing():
    google_translate(params.MISSING_INNER_PHRASES, params.MISSING_INNER_PHRASES_TRANS)
def genx():
    fout = open(params.MISSING_INNER_PHRASES_TRANS, "w")
    fin = open(params.MISSING_INNER_PHRASES)
    ic = 0
    while True:
        line = fin.readline()
        if line == "":
            break
        ic += 1
        fout.write("%s_%s\n" % ("S_INNER", ic))
    fout.close()
    fin.close()
def load_trans_missing_inner(exclude_dict = {}):
    d = dict()
    try:
        lines_inp = read_all_lines(params.MISSING_INNER_PHRASES)
        lines_trans = read_all_lines(params.MISSING_INNER_PHRASES_TRANS)
        for i in range(len(lines_trans)):
            w = lines_inp[i]
            t = lines_trans[i]
            if w not in exclude_dict:
                d[w] = t
    except:
        print("Warning: No fixing map found.")
    return d
if __name__== "__main__":
    gg_trans_missing()
    # genx()

