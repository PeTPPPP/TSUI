import params
from online_searching.kegg.kegg_search_round1 import run1
from online_searching.kegg.kegg_search_round2 import run2
from online_searching.kegg.kegg_parser import extract_text_map_line
from params import TEXT_MAP_R1_FILE, TEXT_MAP_R2_FILE_PREF, TEXT_MAP_R3_FILE


def run_auto_kegg_search():
    run1()
    run2()


def load_jader_kegg_valid_map(d, path):
    fin = open(path)

    while True:
        line = fin.readline()
        if line == "":
            break
        jader_name, target_name = extract_text_map_line(line, first_drug_only=True, to_string=True)
        if len(target_name) > 0:
            d[jader_name] = target_name
    fin.close()
    return d


def load_jader_manual_map(d, path, sep="\t", skip_comments=True, only_perfetch_match=True):
    if path == "":
        print("Warning: No JADER drug manual map file.")
        return
    fin = open(path)
    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split(sep)

        txt = parts[2]

        if txt.lower().startswith('perfect'):
            txt = parts[1]
        if len(parts) > 3:
            if parts[-1].startswith("noMatch"):
                txt = parts[-1]
            elif parts[2].startswith('noMatch'):
                txt = '|'.join(parts[2:])
        d[parts[0]] = txt
        # if parts[0] == 'タナベ胃腸薬＜調律＞':
        #     print(txt)
        #     print(parts)
        #     exit(-1)
        # print(len(parts))
    fin.close()
    return d


def load_full_jader_drug_map(d=None):
    if d is None:
        d = dict()
    jader_kegg_map = d
    load_jader_kegg_valid_map(jader_kegg_map, TEXT_MAP_R1_FILE)
    load_jader_kegg_valid_map(jader_kegg_map, "%s.txt" % TEXT_MAP_R2_FILE_PREF)
    load_jader_kegg_valid_map(jader_kegg_map, TEXT_MAP_R3_FILE)
    load_jader_manual_map(jader_kegg_map, params.JADER_MANUAL_MAP_FILE)
    load_jader_manual_map(jader_kegg_map,params.JADER_MANUAL_MAP_FILE_2)

    return jader_kegg_map


if __name__ == "__main__":
    # run_auto_kegg_search()
    d= {}
    load_jader_manual_map(d, params.JADER_MANUAL_MAP_FILE)
    print("OK")
    print(d)
    print(len(d))
    fx = open("%s/REMapJADERDRUG.txt" % params.TMP_DIR , "w")
    for k, v in d.items():
        fx.write("%s\t%s\n" % (k,v))
    fx.close()
