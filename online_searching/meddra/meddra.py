import params
from online_searching.meddra.meddra_web_search import run_search
from online_searching.meddra.meddra_parser import parse
from online_searching.meddra.check_missing import check1


def run_auto_meddra_search():
    run_search(params.MEDDRA_ALL_PHRASE_FILE, params.MEDDRA_SEARCH_RAW_DICT_FILE)
    parse(search_map_raw_file=params.MEDDRA_SEARCH_RAW_DICT_FILE, out_text_map=params.MEDDRA_TEXT_MAP)
    check1(params.MEDDRA_TEXT_MAP, params.MEDDRA_MISSING_TERMS)


def load_map(d, path, load_none=params.MEDDRA_USE_NOMATCH):
    fin = open(path)
    no_match_terms = set()
    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split("\t")
        if not load_none:
            if parts[1].startswith("noMatch"):
                no_match_terms.add(parts[0])
                continue
        txt = parts[1].split("|")[-1]
        # if txt.__contains__("pt$"):
        #    print("?", line, txt, parts)
        d[parts[0]] = txt
    fin.close()


def load_manual_map(d, path, translated_offset=2):
    fin = open(path)
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip()
        parts = line.split("\t")
        d[parts[0]] = parts[translated_offset]
    fin.close()


def load_meddra_map(d=None, with_manual=False):
    if d is None:
        d = dict()
    meddra_map = d
    load_map(meddra_map, params.MEDDRA_TEXT_MAP)
    if with_manual:
        load_manual_map(meddra_map, params.MEDDRA_MANUAL_MAP)
    return meddra_map


if __name__ == "__main__":
    # run_auto_meddra_search()
    # load_manual_map({}, params.MEDDRA_MANUAL_MAP)
    load_map({}, params.MEDDRA_TEXT_MAP)
    pass
