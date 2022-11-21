from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import params
from params import TEXT_MAP_R1_FILE, TEXT_MAP_R2_FILE_PREF
from utils import utils
import re
from jaconv import jaconv

from online_searching.kegg.kegg_parser import parser, rm_parentheses

JADERDRUG_KEGGSEARCH_RAW_FILE_ROUND2 = "%s/JADERSecondRoundMap.dict" % params.TMP_DIR


# Parse files from KEGG dictionary to obtain exact matches
def flatten(l):
    out = []
    for item in l:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


def selecting_nf(f_in):
    fin = open(f_in, "r")
    dc = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.split('\t')
        try:
            a = eval(line[1])
        except:
            a = line[1]
        # print(line[1]+"\n")
        # print(a)

        if not a:
            dc.update({line[0]: a})

        del (a)
    return (dc)


# def selecting_nf2(f_in, out_name):
#     fin = open(f_in, "r")
#     dc_out = dict()
#     while True:
#         if line == "":
#             break
#         line = fin.readline()
#         line = line.split("\t")
#         if line[1] == "":
#             dc_out.update({line[0]: line[1]}0)
#         else:
#             continue
#     dc_out = {k: v for k,v in dc.items() if v == ""}
#     sortedD = utils.sort_dict(dc_out)
#     fout = open(out_name, "w")
#     for kv in sortedD:
#         k, v = kv
#         fout.write("%s\t%s\n" % (k, v))
#
#     fout.close()

def extract_mixed_expressions(text_r1_file=TEXT_MAP_R1_FILE):
    dc = selecting_nf(text_r1_file)
    # print(dc)
    for key in dc.keys():
        value = jaconv.z2h(key, kana=False, digit=True, ascii=True)
        value = re.split(r'[/\[{(（「〔＜<]', value)

        value = [elem for elem in value if
                 ")" not in elem and "）" not in elem and "＞" not in elem and "」" not in elem and "〕" not in elem and ">" not in elem and "}" not in elem and "\]" not in elem and "/" not in elem]
        # print(key)
        value = map(str.strip, value)
        value = " ".join(value).lower().capitalize()
        dc.update({key: value})
    # print(dc)
    return dc


def initialize():
    browser = webdriver.Firefox()
    browser.get('https://www.genome.jp/kegg/drug/drug_ja.html')

    time.sleep(1)

    search_Box = browser.find_element(By.XPATH, '//html/body/div[4]/div[1]/div[1]/form/input[1]')
    # browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
    search_Box.clear()
    search_Box.send_keys("tretinoin")
    ok = browser.find_element(By.XPATH, '//html/body/div[4]/div[1]/div[1]/form/input[5]')
    time.sleep(1)
    ok.click()
    return browser


def loadExist(path=None):
    try:
        d = utils.load_obj(path)
        print("loaded")
    except:
        d = dict()
        print("exception")

    return d


def run_second(path_first_map, search_dict_out_path):
    # from KEGG_drugs_web import run
    browser = initialize()
    dc = extract_mixed_expressions()
    # time.sleep(1)
    # ses = list(dc.values())
    # print(dc)
    d = loadExist(path_first_map)

    cc = 0

    for key in dc.keys():
        jse = dc[key]
        if key in d:
            print("Skip ", key)
            continue
        try:

            cc += 1
            search_Box = browser.find_element(By.XPATH, '//html/body/div[1]/form/input[1]')
            # browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
            search_Box.clear()
            jse2 = jaconv.z2h(jse, kana=False, digit=True, ascii=True)
            # print(jse, jse2)
            if jse2.isdigit():
                d[key] = "None"
                # print(jse2.isdigit())
                continue
            search_Box.send_keys(jse2)
            time.sleep(1)
            # ヴォリブリス
            ## browser.switch_to.default_content()
            ## browser.switch_to.frame('main')
            ## inpE = browser.find_element_by_name('v_srh1')
            ok = browser.find_element(By.XPATH, '//html/body/div[1]/form/input[2]')

            ## inpE.send_keys(jse)
            ok.click()

            time.sleep(3)
            ## browser.switch_to.default_content()
            ## browser.switch_to.frame('main')

            ## browser.switch_to.frame('result2')

            html = browser.find_element(By.XPATH, '/html/body/div[3]/table')
            html = html.get_attribute('innerHTML')
            # print(html)
            # if mod=True:
            #     for key, value in dc.items():
            #         if jse == value:
            #             jse == key
            #         else
            #             exit(-1)
            #             print("Key is missing!")
            d[key] = html
            ## browser.switch_to.default_content()
            ## browser.switch_to.frame('menu')

            ## backBtn = browser.find_element_by_xpath('//a/img[@alt="検索条件"]')
            ## backBtn.click()
            ## time.sleep(1)
            if cc % 20 == 0:
                utils.save_obj(d, search_dict_out_path)

        except Exception as e:
            # try:
            #     jse = jaconv.z2h(jse, kana=True, digit=True, ascii=True)
            #     search_Box = browser.find_element_by_xpath('//html/body/div[1]/form/input[1]')
            #     search_Box.clear()
            #     search_Box.send_keys(jse)
            #     ok = browser.find_element_by_xpath('//html/body/div[1]/form/input[2]')
            #
            #     ok.click()
            #
            #     time.sleep(1)
            #     html = browser.find_element_by_xpath('/html/body/div[3]/table')
            #     html = html.get_attribute('innerHTML')
            #     print(html)
            #     d[jse] = html
            # except:
            #     continue
            d[key] = "None"
            # print(e)
            utils.save_obj(d, search_dict_out_path)
            ## exit(-1)
        print(cc, key, d[key])
    # print(d.keys)
    utils.save_obj(d, search_dict_out_path)

    # print(ses)
    # run(None,ses,path,mod=True)



def run_transl_X(f_in, fout):
    # from os import path
    # import sys
    from online_searching.gg_translator.autherntication import auth
    from online_searching.gg_translator.google_translation import translate_text
    translate_client = auth()
    ## list to translate
    dc = selecting_nf(f_in)
    for key in dc.keys():
        key2 = rm_parentheses(key)
        if key2.isascii() == True:
            trans = key2
        else:
            trans = translate_text(translate_client, key)
        dc[key] = trans
    sortedD = utils.sort_dict(dc)
    f_out = open(fout, "w")
    for kv in sortedD:
        k, v = kv
        f_out.write("%s\t%s\n" % (k, v))

    f_out.close()
    # return dc


def correct(f_in, fout):
    fin = open(f_in, "r")
    dc = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.split('\t')
        line2 = rm_parentheses(line[1])
        if line2.isascii() == True:
            value = line2
        else:
            value = line[1].strip()
        dc.update({line[0]: value})
    # print(dc)
    sortedD = utils.sort_dict(dc)
    f_out = open(fout, "w")
    for kv in sortedD:
        k, v = kv
        f_out.write("%s\t%s\n" % (k, v))

    f_out.close()
    return (dc)


def update_perfectmatch_drugbank_flag(f_intomatch, fout):
    def load_drug_to_match(p=f_intomatch):
        f = open(p)
        drug_names = []
        while True:
            line = f.readline()
            if line == "":
                break
            parts = line.strip().split("\t")
            drug_names.append(parts[1])
        f.close()
        return drug_names


    drug_names = load_drug_to_match(f_intomatch)
    from data_factory.drugname_matching import match_drug_bank
    matching_set, _ = match_drug_bank(drug_names)

    fin_tomatch = open(f_intomatch, "r")
    f_out = open(fout, "w")

    while True:
        line = fin_tomatch.readline()
        if line == "":
            break
        word = line.split("\t")[1].strip()
        print(word)
        if word in matching_set:
            value = "PerfectMatch"
        else:
            value = ""
        line = line.strip() + "\t" + value + "\n"
        print(line)
        f_out.write(line)

    f_out.close()

def run2():
    parser(path=params.JADERDRUG_KEGG_SEARCH_RAW_FILE1, out_name=TEXT_MAP_R1_FILE)
    run_second(path_first_map=TEXT_MAP_R1_FILE, search_dict_out_path=JADERDRUG_KEGGSEARCH_RAW_FILE_ROUND2)
    parser(mod=True, path=JADERDRUG_KEGGSEARCH_RAW_FILE_ROUND2, out_name="%s.txt" % TEXT_MAP_R2_FILE_PREF)
    run_transl_X("%s.txt" % TEXT_MAP_R2_FILE_PREF, "%s_translated.txt" % TEXT_MAP_R2_FILE_PREF)
    correct("%s_translated.txt" % TEXT_MAP_R2_FILE_PREF, "%s_translated_corrected.txt" % TEXT_MAP_R2_FILE_PREF)
    update_perfectmatch_drugbank_flag( "%s_translated_corrected.txt" % TEXT_MAP_R2_FILE_PREF, "%s_translated_corrected_matchingFlag.txt" % TEXT_MAP_R2_FILE_PREF)
if __name__ == "__main__":
    run2()


