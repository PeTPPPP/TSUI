import params
from online_searching.meddra.meddra_web_search import run_search
from online_searching.meddra.meddra_parser import parse


def check1(path1, missing1_file):
    fin = open(path1)
    fout = open(missing1_file, "w")

    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split("\t")
        if parts[1] == "noMatch":
            fout.write("%s\n" % parts[0])
    fin.close()
    fout.close()


def search2(missing1_file, raw_search_dict, map_text_round2_file):
    run_search(missing1_file, raw_search_dict)
    parse(raw_search_dict, out_text_map=map_text_round2_file)
