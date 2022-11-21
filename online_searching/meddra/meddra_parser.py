from bs4 import BeautifulSoup
from utils import utils
import bs4
from unidecode import unidecode
from jaconv import jaconv
def getNextValidSibling(c):
    if c is None:
        return c
    c = c.next_sibling
    while True:
        if c is None:
            break
        if type(c) == bs4.element.NavigableString:
            c = c.next_sibling
            continue
        elif c.name == 'br' or c.name == 'hr':
            c = c.next_sibling
            continue
        break
    return c


def print_db(txt, flag):
    if flag:
        print(txt)


def parse(search_map_raw_file, out_text_map):
    dJse2MeddraHTML = utils.load_obj(search_map_raw_file)
    fout = open(out_text_map, "w")
    cc = 0
    db_flag_stop = False
    # db_key = "甲状腺機能亢進"
    for k, v in dJse2MeddraHTML.items():
        print(k)
        # if k.__contains__(db_key):
        #     print("H", db_key)
        #     db_flag_stop = True
        #     print(v)
        #     exit(-1)

        vhtml = BeautifulSoup(v, "html.parser")
        c = vhtml.find('span', {"class": "key"})
        isEnd = False

        meddraAll = []
        while True:
            c = getNextValidSibling(c)
            if c is None:
                break
            if c.name != 'a':
                print("Invalid")
                print(v)
                break
            mType = c.get('name').lower()
            # print(mType)

            ars = []
            meddraCodeEn = []
            while True:
                c = getNextValidSibling(c)
                if c is None or c.name == 'input':
                    isEnd = True
                    break
                if c.name == 'span':

                    break
                else:
                    ars.append(c)
            if db_flag_stop:
                print(len(ars), ars)
            for i, tag in enumerate(ars):
                if i % 3 == 2:
                    print_db(tag, db_flag_stop)
                    vv = tag.select('span')
                    cd = vv[0].text
                    en = vv[-1].text
                    jw = vv[2].text
                    print_db((mType, cd, jw, en, k), db_flag_stop)
                    if db_flag_stop:
                        print(jw, k, jw == k)
                    if not try_encodeing_compare(jw, k):
                        continue
                    if mType == 'pt':
                        cc += 1
                    meddraCodeEn.append("%s|%s" % (cd, en))
                    print_db(("??", meddraCodeEn, "?"), db_flag_stop)
            if mType == 'pt':

                meddraCodeEn = "#".join(meddraCodeEn)
                meddraAll.append("%s$%s" % (mType, meddraCodeEn))
                if db_flag_stop:
                    print("PT", meddraAll)
            if len(ars) % 3 != 0:
                for ar in ars:
                    print(ar)
                print(len(ars))
            assert len(ars) % 3 == 0

            if isEnd:
                break
        ss = "\t".join(meddraAll)
        if len(ss) < 4:
            ss = 'noMatch'
        fout.write("%s\t%s\n" % (k, ss))
        # fout.flush()
        if db_flag_stop:
            exit(-1)
    print("Total pt: ", cc)

    fout.close()

def try_hypen(inp, target):
    inp = inp.replace('－', '−').replace('-', '−')

    target = target.replace('－', '−').replace('-', '−')

    return inp == target

def try_2(inp, target):
    inp2 = unidecode(inp)
    target2 = unidecode(target)
    # print(inp, inp2)
    # print(target, target2)
    return inp2 == target2
def try_encodeing_compare(inp, target):
    if inp == target:
        return True
    if try_hypen(inp, target):
        return True
    inp = jaconv.z2h(inp, kana=True, digit=True, ascii=True)
    target = jaconv.z2h(target, kana=True, digit=True, ascii=True)
    return inp == target

def parse2(search_map_raw_file, out_text_map):
    dJse2MeddraHTML = utils.load_obj(search_map_raw_file)
    fout = open(out_text_map, "w")
    cc = 0
    db_flag_stop = False

    fout2 = open("%s/CheckMEDDRAExtractMatch.txt" % params.TMP_DIR, "w")
    k_sets = set()
    for k, v in dJse2MeddraHTML.items():
        # print(k)

        vhtml = BeautifulSoup(v, "html.parser")
        c = vhtml.find('span', {"class": "key"})
        isEnd = False

        meddraAll = []
        while True:
            c = getNextValidSibling(c)
            if c is None:
                break
            if c.name != 'a':
                print("Invalid")
                print(v)
                break
            mType = c.get('name').lower()
            # print(mType)

            ars = []
            meddraCodeEn = []

            while True:
                c = getNextValidSibling(c)
                if c is None or c.name == 'input':
                    isEnd = True
                    break
                if c.name == 'span':

                    break
                else:
                    ars.append(c)
            if db_flag_stop:
                print(len(ars), ars)
            for i, tag in enumerate(ars):
                if i % 3 == 2:
                    print_db(tag, db_flag_stop)
                    vv = tag.select('span')
                    cd = vv[0].text
                    en = vv[-1].text
                    jw = vv[2].text
                    print_db((mType, cd, jw, en, k), db_flag_stop)
                    if db_flag_stop:
                        print(jw, k, jw == k)
                    # if jw != k:
                    if not try_encodeing_compare(jw, k) and len(jw) == len(k):
                        if mType == 'pt':
                            fout2.write("%s;%s;%s;%s\n" % (k, cd, jw, en))
                            k_sets.add(k)
                        continue
                    if mType == 'pt':
                        cc += 1
                    meddraCodeEn.append("%s|%s" % (cd, en))
                    print_db(("??", meddraCodeEn, "?"), db_flag_stop)
            if mType == 'pt':

                meddraCodeEn = "#".join(meddraCodeEn)
                meddraAll.append("%s$%s" % (mType, meddraCodeEn))
                if db_flag_stop:
                    print("PT", meddraAll)
            if len(ars) % 3 != 0:
                for ar in ars:
                    print(ar)
                print(len(ars))
            assert len(ars) % 3 == 0

            if isEnd:
                break
        ss = "\t".join(meddraAll)
        if len(ss) < 2:
            ss = 'None_'
        fout.write("%s\t%s\n" % (k, ss))
        # fout.flush()
        if db_flag_stop:
            exit(-1)
    print("Total pt: ", cc)

    fout.close()
    fout2.close()
    fout3 = open("%s/MEddraKeySearchCheck.txt" % params.TMP_DIR, "w")
    for k in sorted(list(k_sets)):
        fout3.write("%s\n" % k)
    fout3.close()


if __name__ == "__main__":
    import params

    parse(search_map_raw_file=params.MEDDRA_SEARCH_RAW_DICT_FILE, out_text_map=params.MEDDRA_TEXT_MAP)
