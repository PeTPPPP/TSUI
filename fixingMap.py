import params
from utils import utils
INP_PATH = "%s/JADERDrugManualX.txt" % params.TMP_DIR
SEP= " # "
def fix_noMatchSuffix(suffix="noMatch"):
    fin  = open(INP_PATH)
    fout = open("%s_fixNoMatchingEndding" % INP_PATH, "w")
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip()
        # print(line)
        if line[-len(suffix):] == suffix:
            print("X", line[-len(suffix):], line)
            line = "%s\t%s" % (line[:-(len(suffix))], suffix)
        line = utils.remove_multiple_char(line, '\t')
        fout.write("%s\n" % line)
    fin.close()
    fout.close()


def check_other():
    fin = open("%s_fixNoMatchingEndding" % INP_PATH)
    f_db = open("%s_fixNoMatchingEndding_Error" % INP_PATH, "w")
    ic = 0
    iLine = 0

    while True:
        line = fin.readline()
        if line == "":
            break
        is_skip = False
        line = line.strip()
        parts = line.split("\t")
        iLine += 1
        if len(parts) != 3:

            if len(parts) >= 3 and (parts[2].__contains__('noMatch')):
                is_skip = True

            if len(parts) >= 4 and parts[3].__contains__("noMatch"):
                is_skip = True


            if parts[-1].__contains__("noMatch"):
                is_skip = True


            if iLine == 6493:
               print("Line: ", line, len(parts), parts)
               # exit(-1)
            if not is_skip:
                print(line, len(parts), parts)
                ic += 1
                f_db.write("%s%s%s\n" % (iLine, SEP, line))
    print("Miss: ", ic)
    f_db.close()

def merger_FixTab():
    def load_FixingTab_Map():
        fin = open("%s/JADERDrugManualX_fixed.txt" % params.TMP_DIR)
        d = {}
        while True:
            line = fin.readline()
            if line == "":
                break
            parts =line.strip().split(SEP)

            l_id = int(parts[0]) - 1
            txt = parts[1]
            phrases = txt.split("\t")

            d[l_id] = "%s\t%s\t%s\n" % (phrases[0], phrases[1], "|".join(phrases[2:]))
        fin.close()
        return d
    def fixTab():
        d = load_FixingTab_Map()
        fout = open("%s/JADERDrugManualTabFix.txt" % params.TMP_DIR, "w")
        fin = open("%s_fixNoMatchingEndding" % INP_PATH)
        i_line = 0
        while True:
            line = fin.readline()
            if line == "":
                break
            if i_line in d:
                line = d[i_line]
            fout.write("%s" % line)
            i_line += 1
        fin.close()
        fout.close()

    fixTab()


def check_no_match2():
    fin = open("%s/JADERDrugManualTabFix.txt" % params.TMP_DIR)
    f_db = open("%s/JADERDrugManual_MistakeNoMatch.txt" % params.TMP_DIR, "w")
    ic = 0
    iLine = 0

    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip()
        parts = line.split("\t")
        iLine += 1
        if line.__contains__("noMatch"):
            if len(parts) <3 or (not parts[2].startswith("noMatch") and not parts[-1] == 'noMatch'):
                    print(iLine, line, len(parts), parts)
                    ic += 1
                    f_db.write("%s%s%s\n" % (iLine, SEP, line))
    print("Miss: ", ic)
    f_db.close()

def fixNoMatch2():
    def load_FixNoMatch2():
        fin = open("%s/JADERDrugManual_MistakeNoMatch_fixed_GK.txt" % params.TMP_DIR)
        d = {}
        while True:
            line = fin.readline()
            if line == "":
                break
            line = utils.remove_multiple_char(line, '\t')
            parts = line.strip().split(SEP)

            l_id = int(parts[0]) - 1
            txt = parts[1]

            phrases = txt.split("\t")
            # if not phrases[2].startswith("noMatch"):
            txt = "%s\t%s\t%s\n" % (phrases[0], phrases[1], "|".join(phrases[2:]))

            d[l_id] = txt
        fin.close()
        return d


    def fixNoMatch():
        d = load_FixNoMatch2()
        fout = open("%s/JADERDrugManualFinal.txt" % params.TMP_DIR, "w")
        fin = open("%s/JADERDrugManualTabFix.txt" % params.TMP_DIR)
        i_line = 0
        while True:
            line = fin.readline()
            if line == "":
                break
            if i_line in d:
                line = d[i_line]
            fout.write("%s" % line)
            i_line += 1
        fin.close()
        fout.close()
    fixNoMatch()

def fixTabX():
    def load_TabFix():
        fin = open("%s/MissTab_GK.txt" % params.TMP_DIR)
        d = {}
        while True:
            line = fin.readline()
            if line == "":
                break
            parts = line.strip().split("||")
            l_id = int(parts[0]) - 1
            txt = parts[1]
            ts = txt.split("|")
            ts = [t.strip() for t in ts]
            ts = "|".join(ts)
            txt = ts.replace(";", "\t")
            d[l_id] = "%s\n" % txt
        return d

    def fixTab():
        fin = open("%s/JADERDrugManualFinal_BFTab.txt" % params.TMP_DIR)
        fout= open("%s/JADERDrugManualFinal.txt" % params.TMP_DIR, "w")
        d = load_TabFix()
        lid = 0
        while True:
            line = fin.readline()
            if line == "":
                break
            if lid in d:
                line = d[lid]
            fout.write("%s" % line)
            lid += 1
        fin.close()
        fout.close()

    fixTab()


def extract_missing_drug_trans():
    all_drug_phrases = utils.read_all_lines(params.DRUG_ALL_PHRASE_FILE)
    from online_searching.kegg.kegg import load_full_jader_drug_map
    d_map = {}
    load_full_jader_drug_map(d_map)
    fout = open("%s/MissingDrugTrans.txt" % params.TMP_DIR, "w")
    for w in all_drug_phrases:
        if w not in d_map:
            fout.write("%s\n" % w)
    fout.close()
if __name__ == "__main__":
    # fix_noMatchSuffix()
    # check_other()
    # merger_FixTab()
    # check_no_match2()
    # fixNoMatch2()
    # fixTabX()
    extract_missing_drug_trans()
    pass
