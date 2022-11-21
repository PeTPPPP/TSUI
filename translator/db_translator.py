import params
from online_searching.kegg.kegg import load_full_jader_drug_map
from online_searching.meddra.meddra import load_meddra_map
from online_searching.leftover.leftover import load_leftover_map, load_header_map, load_fixing_map
from online_searching.leftover.trans_missingInner_phrases import load_trans_missing_inner
import codecs
import io
import os
from utils import utils
import csv

G_PREF = "GG_"
MISS_PREF = "*_"


def load_all_map(skip_inner=True):
    drug_meddra_map = dict()
    load_full_jader_drug_map(d=drug_meddra_map)
    load_meddra_map(d=drug_meddra_map, with_manual=not params.MEDDRA_USE_NOMATCH)
    leflover_map = load_leftover_map()
    header_map, _ = load_header_map()
    fixing_map = load_fixing_map()
    d_force = utils.merge_dict([drug_meddra_map, leflover_map])

    if skip_inner:
        inner_map = {}
    else:
        inner_map = load_trans_missing_inner(exclude_dict=d_force)
    # print("Header map: ", header_map)
    return drug_meddra_map, leflover_map, header_map, fixing_map, inner_map


def check_missing_inner_tokens(inp_file, skip_ids_drugmeddra, drugmeddra_map, skip_ids_leftover=[], dmap_leftover={},
                               missing_inner_set=set()):
    f = codecs.open(inp_file, "r", "utf-8")
    line_id = 0
    nSize = 0
    skip_map1 = -1 in skip_ids_drugmeddra
    skip_map2 = -1 in skip_ids_leftover
    is_header = True
    search_dict_list = [drugmeddra_map, dmap_leftover]
    while True:
        lines = readNLines(f, 10000)
        if len(lines) == 0:
            print("\n Total lines: ", line_id)

            break
        for line in lines:
            if line == "":
                print(inp_file, line_id)
                break
            line_id += 1

            if is_header:
                is_header = False
                continue

            if line_id > 0:
                if not line[0].isalpha():
                    continue
            if line_id % 100 == 0:
                print("\r%s" % line_id, end="")
            ios = io.StringIO(line.strip())
            token_list = list(csv.reader(ios))

            if len(token_list) == 0:
                continue
            token_list = token_list[0]
            if nSize == 0:
                nSize = len(token_list)
            for col_id, token in enumerate(token_list):
                if not skip_map1 and col_id not in skip_ids_drugmeddra:
                    if token != "":
                        translated_token = utils.get_dict(drugmeddra_map, token, -1)
                        if translated_token == -1:
                            miss_tokens = check_missing_translate2(token, all_map=search_dict_list)
                            for tk in miss_tokens:
                                missing_inner_set.add(tk)

                elif not skip_map2 and col_id not in skip_ids_leftover:
                    if token != "":
                        translated_token = utils.get_dict(dmap_leftover, token, -1)
                        if translated_token == -1:
                            miss_tokens = check_missing_translate2(token, all_map=search_dict_list)
                            for tk in miss_tokens:
                                missing_inner_set.add(tk)


def extract_missing_inner_tokens():
    drugmeddra_map, leftover_map, header_map, fixing_map, _ = load_all_map()
    print("MapSize: ", len(drugmeddra_map), len(leftover_map), len(header_map))
    missing_set = set()
    fout = open("%s/MissingInnerTokens.txt" % params.TMP_DIR, "w")
    print("Run extract missing inner trans")
    for i in range(len(params.JADER_TRANS_FILES)):
        # if i != 3:
        #    continue
        file_inp = params.JADER_TRANS_FILES[i]
        skip_ids_drugmeddra, skip_ids_leftover = params.JADER_TRANS_SKIP_COLUMS[i]
        print("Run: ", file_inp)
        check_missing_inner_tokens(file_inp, skip_ids_drugmeddra, drugmeddra_map, skip_ids_leftover, leftover_map,
                                   missing_set)

    for w in sorted(list(missing_set)):
        fout.write("%s\n" % w)
    fout.close()


def readNLines(f, nLine):
    """Reads in nLine lines from input (f)
    f - filename
    nLine - number of lines to read in
    replace - logical value indicating replacement of semicolon in output
    """
    lines = []
    cc = 0
    while True:
        line = f.readline()
        if line == "":
            break
        cc += 1
        lines.append(line)
        if cc == nLine:
            break

    return lines


def generate_translation_output_path(inp_file):
    file_name = os.path.basename(inp_file)

    file_parts = file_name.split(".")
    file_base, extension = file_parts[0], file_parts[-1]

    out_file = "%s/%s_EN.%s" % (params.JADER_TRANSLATION_DIR, file_base, extension)
    return out_file


class Counter:
    def __init__(self):
        self.c = 0

    def inc(self, v=1):
        self.c += v

    def dec(self, v=1):
        self.c -= v

    def get(self):
        return self.c


def get_tran_from_all_map(k, allmap):
    for d in allmap:
        v = utils.get_dict(d, k, -1)
        if v != -1:
            break
    return v


def try_strip_trans(k, allmap):
    k = k.strip()
    return get_tran_from_all_map(k, allmap)
def try_translate2(inp_str, all_map=[], reduce=False, force_in_map=False):
    strip_trans = try_strip_trans(inp_str, all_map)
    if strip_trans != -1:
        return strip_trans, True

    tokens = utils.split_str(inp_str)
    # res = []
    res_codes = []
    is_success = True

    # print("Try: ", inp_str)
    # print(tokens)
    for p in tokens:
        token, cd = p
        if force_in_map and cd != -1 and cd != 2:
            cd = 0
        # print("TC: ", token, cd, token.isdigit())
        if cd == 0:
            v = get_tran_from_all_map(token, all_map)
            # print("V: ", v, "#", token)
            # res.append(v)
            res_codes.append([v, cd])
            if v == -1:
                is_success = False
                # print("\tFalse at: ", token, cd)
                break
        else:

            res_codes.append([token, cd])
    # print("RES: ", res_codes)
    if is_success:
        res = utils.restore_str(res_codes, reduce=reduce)
    else:
        res = inp_str

    if is_success:
        pass
    else:
        pass

    return res, is_success


C_BRACKET = {'{', '(', '「', '＜', '<'}


def is_bracket(c):
    if c in C_BRACKET:
        return True
    return False


def check_missing_translate2(inp_str, all_map=[], only_inner=False):
    tokens = utils.split_str(inp_str)
    res = []
    is_success = True
    trans_res_b = []
    inner_invalid = set()
    # print("Try: ", inp_str)
    for i, p in enumerate(tokens):
        token, cd = p
        if cd == 0:
            v = get_tran_from_all_map(token, all_map)
            print("Get v: ", token, v)
            res.append(v)
            if v == -1:
                is_success = False
                trans_res_b.append(False)
                # print("Invalid: ", token)
                if only_inner:
                    if i > 0:
                        if is_bracket(tokens[i - 1][0]):
                            inner_invalid.add(token)
                else:
                    inner_invalid.add(token)
            else:
                trans_res_b.append(True)
                # print("\tFalse at: ", token, cd)

        else:
            res.append(token)
            trans_res_b.append(True)

    return inner_invalid


def tran_file(inp_file, skip_ids_drugmeddra, drugmeddra_map, skip_ids_leftover=[], dmap_leftover={},
              header_map={}, inner_map={}, unknown_translation_set=set(), fix_map=dict(), count_missing=Counter()):
    f = codecs.open(inp_file, "r", "utf-8")
    fout_path = generate_translation_output_path(inp_file=inp_file)
    fout = codecs.open(fout_path, 'w', 'utf-8')
    line_id = 0
    nSize = 0
    skip_map1 = -1 in skip_ids_drugmeddra
    skip_map2 = -1 in skip_ids_leftover
    is_header = True
    search_dict_list = [drugmeddra_map, dmap_leftover, inner_map, fix_map]
    is_drug_file = inp_file.__contains__("drug")
    DRUG_COL_ID = 4
    # db = True
    while True:
        lines = readNLines(f, 10000)
        if len(lines) == 0:
            print("\n Total lines: ", line_id)

            break
        for line in lines:
            if line == "":
                print(inp_file, line_id)
                break
            line_id += 1
            # if line.__contains__('トリクロホスナトリウム'):
            #    print("Here: ", line)
            # exit(-1)
            if is_header:
                line = line.strip()
                try:
                    line = header_map[line]
                    line = line.replace(",", "\t")
                    fout.write("%s\n" % line)
                    is_header = False
                    continue

                except:
                    print("Error: No header map for: ", inp_file)
                    print("Header: ", line)
                    exit(-1)

            if line_id > 0:
                if not line[0].isalpha():
                    continue
            if line_id % 100 == 0:
                print("\r%s" % line_id, end="")
            ios = io.StringIO(line.strip())
            token_list = list(csv.reader(ios))

            if len(token_list) == 0:
                continue
            token_list = token_list[0]
            if nSize == 0:
                nSize = len(token_list)
            translated_tokens = []

            for col_id, token in enumerate(token_list):
                is_drug_col = is_drug_file and col_id == DRUG_COL_ID
                if not skip_map1 and col_id not in skip_ids_drugmeddra:
                    if token != "":
                        translated_token = utils.get_dict(drugmeddra_map, token, -1)
                        if translated_token == -1:
                            trans2_token, is_success = try_translate2(token, all_map=search_dict_list, reduce=is_drug_col, force_in_map=is_drug_col)
                            if is_success:
                                # if token.__contains__('セフテラム　ピボキシル'):
                                #     print("Trans: ", trans2_token)
                                #     exit(-1)
                                token = trans2_token
                            else:
                                unknown_translation_set.add(token)
                                print("Found missing 1: ", token)
                                print(trans2_token, is_success)
                                exit(-1)
                                translated_unknown_token = utils.get_dict(fix_map, token, -1)
                                if translated_unknown_token == -1:
                                    token = "%s%s" % (MISS_PREF, token)
                                    count_missing.inc()
                        else:
                            token = translated_token

                elif not skip_map2 and col_id not in skip_ids_leftover:
                    if token != "":
                        translated_token = utils.get_dict(dmap_leftover, token, -1)
                        if translated_token == -1:
                            trans2_token, is_success = try_translate2(token, all_map=search_dict_list, reduce=is_drug_col)
                            if is_success:
                                token = trans2_token
                            else:
                                unknown_translation_set.add(token)
                                print("Found missing 2: ", token)
                                print(trans2_token, is_success)
                                exit(-1)
                                translated_unknown_token = utils.get_dict(fix_map, token, -1)
                                if translated_unknown_token == -1:
                                    token = "%s%s" % (MISS_PREF, token)
                                    count_missing.inc()
                        else:
                            token = translated_token

                token = token.replace("\t", " ").strip()
                token = token.replace("\"", "")
                token = token.replace("{DF}", "DF")
                translated_tokens.append(token)
            if len(translated_tokens) < nSize:
                for col_id in range(len(translated_tokens), nSize):
                    translated_tokens.append("")

            liner = "\t".join(translated_tokens)

            fout.write("%s\n" % liner)

    print("\n")
    print("Translation completed.: %s\n" % fout_path)
    fout.close()


def run_translation_1(skip_inner=False):
    drugmeddra_map, leftover_map, header_map, fixing_map, inner_map = load_all_map(skip_inner=skip_inner)
    print("MapSize: ", len(drugmeddra_map), len(leftover_map), len(header_map), len(fixing_map), len(inner_map))
    fx = open("%s/DictAll.txt" % params.TMP_DIR, "w")
    unknown_translation_set = set()
    count_missing = Counter()
    for k, v in drugmeddra_map.items():
        fx.write("%s\t%s\n" % (k, v))
    fx.write("_________________\n")
    for k, v in leftover_map.items():
        fx.write("%s\t%s\n" % (k, v))

    fx.close()

    for i in range(len(params.JADER_TRANS_FILES)):
        # if i != 1:
        #    continue
        file_inp = params.JADER_TRANS_FILES[i]
        skip_ids_drugmeddra, skip_ids_leftover = params.JADER_TRANS_SKIP_COLUMS[i]

        print("Translating %s..." % file_inp)
        tran_file(file_inp, skip_ids_drugmeddra=skip_ids_drugmeddra, drugmeddra_map=drugmeddra_map,
                  skip_ids_leftover=skip_ids_leftover, dmap_leftover=leftover_map, header_map=header_map,
                  inner_map=inner_map, unknown_translation_set=unknown_translation_set, fix_map=fixing_map,
                  count_missing=count_missing)

    fout = open("%s_2" % params.MISSING_FILE, "w")
    for w in sorted(list(unknown_translation_set)):
        fout.write("%s\n" % w)
    fout.close()
    if count_missing.get() > 0:
        print("There exist missing translation. N_MISSING COUNT, N_MISSING_TOKEN_SET_SIZE: ", count_missing.get(),
              len(unknown_translation_set))
        print("Please manually translate missing tokens at %s and write to %s then re run.\n" % (
        params.MISSING_FILE, params.MISSING_TRANS_FIX_FILE))

    else:
        print("Translation successful. No missing.")


def run_translation_test(skip_inner=False):

    drugmeddra_map, leftover_map, header_map, fixing_map, inner_map = load_all_map(skip_inner=skip_inner)
    mm = '不明'
    # mm = 'シレキセチル'

    # search_dict_list = [drugmeddra_map, leftover_map, inner_map, fixing_map]
     #print(get_tran_from_all_map(mm, search_dict_list))
    # exit(-1)
    if mm in drugmeddra_map:
        print("In MeddraDrug", drugmeddra_map[mm])
    if mm in inner_map:
        print("Inner map", inner_map[mm])
    if mm in fixing_map:
        print("Fixing at ", fixing_map[mm])

    a, b = try_translate2(mm, all_map=[drugmeddra_map, leftover_map, fixing_map, inner_map], force_in_map=True)
    print("Trans" , a)
    print("B", b)
    # inpx = [["a", 0], ["b", 0], ["a", 0], ["a",1] ,[",",1]]
    # print(utils.restore_str(inpx, reduce=True))

def t2():
    line = "AB-04008126,02,001,被疑薬,腹膜透析液（８−１）,エクストラニール,腹腔内,20031108,20040321,2000,mL,1,慢性腎臓病,投与中止,,"
    ios = io.StringIO(line.strip())
    token_list = list(csv.reader(ios))

    token_list = token_list[0]

    nSize = len(token_list)
    translated_tokens = []

    file_inp = params.JADER_TRANS_FILES[0]
    skip_ids_drugmeddra, skip_ids_leftover = params.JADER_TRANS_SKIP_COLUMS[0]
    if token_list[0] == "AB-04008126":
        db = True

        print("DB  ...")



    drugmeddra_map, leftover_map, header_map, fixing_map, inner_map = load_all_map(skip_inner=False)


    for col_id, token in enumerate(token_list):
        if col_id not in skip_ids_drugmeddra:
            if token != "":
                translated_token = utils.get_dict(drugmeddra_map, token, -1)
                print(token, translated_token)
                if translated_token == -1:
                    trans2_token, is_success = try_translate2(token, all_map=[ drugmeddra_map, leftover_map, header_map, fixing_map, inner_map ], reduce=False)

                    print(trans2_token)
if __name__ == "__main__":
    run_translation_test()
    # t2()
    ## DO NOT FORGET TO RUN KEGG MODDING FOR COMBINATION RESOLVE

