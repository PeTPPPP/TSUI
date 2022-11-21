from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import inspect

import params
from utils import utils
import re
from bs4 import BeautifulSoup
from jaconv import jaconv


# Parse files from KEGG dictionary to obtain exact matches
def flatten(l):
    out = []
    for item in l:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


def rm_parentheses(value):
    key = jaconv.z2h(value, kana=False, digit=True, ascii=True)
    key = re.split(r'[/\[{(（「〔＜<]', key)

    key = [elem for elem in key if
           ")" not in elem and "）" not in elem and "＞" not in elem and "」" not in elem and "〕" not in elem and ">" not in elem and "}" not in elem and "\]" not in elem and "/" not in elem]
    # re.split(r'[/\[{(（「〔＜<]', value)
    key = map(str.strip, key)
    key = " ".join(key).lower().capitalize()
    return key


def getCurrentLineNo():
    return inspect.currentframe().f_back.f_lineno


def loadExist(path=None):
    try:
        d = utils.load_obj(path)
        print("loaded")
    except:
        d = dict()
        print("exception")

    return d


def extract_text_map_line(line, first_drug_only=True, to_string=True):
    parts = line.strip().split("\t")
    jader_drug_name = parts[0]
    try:
        target_name = eval(parts[1])
    except:
        target_name = []

    if len(target_name) > 0:

        if first_drug_only:
            target_name = [target_name[1]]
    if to_string:
        target_name = ",".join(target_name)
    return jader_drug_name, target_name


def parser(path, out_name, mod=False):
    # Load dictionary of terms and corresponding html documents from KEGG searches:
    try:
        d = utils.load_obj(path)
    except:
        print("Dictionary not found!")
        exit(-1)
    # if mod == False:
    #     valuelist = d.keys()
    # else:
    #     valuelist = [rm_parentheses(val) for val in d.keys()]
    # print(valuelist)
    # For all keys in dictionary search the corresponding html code for exact matches:
    dict_out = dict()
    cc = 0
    kegg_set = set()

    for value in d.keys():

        output = list()
        soup = BeautifulSoup(d[value], 'html.parser')
        print(soup)
        # print(soup)
        # it = iter(soup.find_all('tr'))
        trs = soup.find_all('tr')[1:]
        #  next(it, None)
        if mod == True:
            value_converted = rm_parentheses(value)
        else:
            value_converted = jaconv.z2h(value, kana=False, digit=True, ascii=True)
        print(value_converted)
        highest_value_list = list()
        # row_index = 1
        for row_index, row in enumerate(trs):

            ## Data1 columns
            columns_data = row.find_all('td', class_="data1")
            kegg_id = columns_data[0].text.strip()
            active_ingredient_names = columns_data[1].text.strip()
            active_ingredient_names_list = re.split(r'[\n;(]', active_ingredient_names)
            active_ingredient_names_list = [elem.strip() for elem in active_ingredient_names_list]
            active_ingredient_names_list = list(filter(None, active_ingredient_names_list))
            # print(active_ingredient_names_list)
            ## Data1_mw columns
            columns_mw400_data = row.find_all('td', class_="data1 mw400")
            brand_names = columns_mw400_data[0].text.strip()
            brand_names_list = re.split(r'[\n;(]', brand_names)
            brand_names_list = [elem.strip() for elem in brand_names_list]
            brand_names_list = list(filter(None, brand_names_list))
            diseases = columns_mw400_data[1].text.strip()

            for idx, v in enumerate(active_ingredient_names_list):

                if re.search(r'(.*?)INN(.*?)', v) is not None:
                    id_international = idx - 1
                    inn_value = True
                    # print(re.search(r'(.*?)INN(.*?)', v) is not None)
                    break
                else:
                    inn_value = False
            # print(inn_value)
            if any(elem.lower() == value_converted.lower() for elem in active_ingredient_names_list):
                dum = True
            else:
                dum = False
            if any(elem.lower() == value_converted.lower() for elem in brand_names_list):
                dum2 = True
            else:
                dum2 = False
            #
            # if (re.search(rf'\b{value_converted}\b', active_ingredient_names, re.IGNORECASE)) is None:
            #     dum = False
            # else:
            #     dum = True
            # if (re.search(rf'\b{value_converted}\b', brand_names, re.IGNORECASE)) is None:
            #     dum2 = False
            # else:
            #     dum2 = True
            exact_value = dum or dum2
            # print(exact_value, inn_value)
            # if (exact_value == True):
            #     cc += 1
            #     kegg_set.add(kegg_id)
            if ((exact_value == True) and (inn_value == True)):
                highest_value_list.append(2)

            if ((exact_value == True) and (inn_value == False)):
                highest_value_list.append(1)
            else:
                highest_value_list.append(0)
            ## print(highest_value_list)
        try:
            largest_value = max(highest_value_list)
            ## Test for multi maximums
            dy_lst = [val for val in highest_value_list if val == largest_value]
            if ((len(dy_lst) > 1) and (largest_value != 0)):
                print("Multiple maximums found at", value, "!")
            max_index = highest_value_list.index(largest_value)
            columns_data = trs[max_index].find_all('td', class_="data1")
            kegg_id = columns_data[0].text.strip()
            active_ingredient_names = columns_data[1].text.strip()
            active_ingredient_names_list = re.split(r'[\n;(]', active_ingredient_names)
            active_ingredient_names_list = [elem.strip() for elem in active_ingredient_names_list]
            active_ingredient_names_list = list(filter(None, active_ingredient_names_list))
            ## print(active_ingredient_names_list)
            ## Data1_mw columns
            columns_mw400_data = row.find_all('td', class_="data1 mw400")
            brand_names = columns_mw400_data[0].text.strip()
            brand_names_list = re.split(r'[\n;(]', brand_names)
            brand_names_list = [elem.strip() for elem in brand_names_list]
            brand_names_list = list(filter(None, brand_names_list))
            diseases = columns_mw400_data[1].text.strip()
            if largest_value == 2:

                for idx, v in enumerate(active_ingredient_names_list):
                    if re.search(r'(.*?)INN(.*?)', v) is not None:
                        id_international = idx - 1
                output = [kegg_id, active_ingredient_names_list[id_international].strip()]
                kegg_set.add(kegg_id)

            else:
                if largest_value == 1:
                    active_ingredient_names_list = [elem for elem in active_ingredient_names_list if ")" not in elem]
                    active_ingredient_names_list = [elem for elem in active_ingredient_names_list if elem.isascii()]

                    output = [kegg_id, active_ingredient_names_list]
                    output = flatten(output)
                    kegg_set.add(kegg_id)

                else:
                    pass
        except:
            output = []
        ## print(output)
        ## Extract data at highest value for match in KEGG
        # if largest_value == 1:
        #     output = [kegg_id, active_ingredient_names_list]
        #     break
        # else:
        #     pass
        #
        #     if ((exact_value == True) and (inn_value == True)):
        #         output = [kegg_id, active_ingredient_names_list[id_international].strip()]
        #         # print(exact_value, inn_value, output)
        #         break
        #         print(val)
        #
        #     else:
        #         if ((exact_value == True) and (inn_value == False)):
        #             active_ingredient_names_list = [elem for elem in active_ingredient_names_list if ")" not in elem]
        #             active_ingredient_names_list = [elem for elem in active_ingredient_names_list if elem.isascii()]
        #
        #             output = [kegg_id, active_ingredient_names_list]
        #             break
        #         else:
        #             pass
        # if bool(output) is not False:
        #     cc += 1
        # else:
        #     pass

        dict_out.update({value: output})
    # print(dict_out)
    # print([a for a in dict_out.values() if len(a) > 1])

    sortedD = utils.sort_dict(dict_out)
    fout = open(out_name, "w")
    for kv in sortedD:
        k, v = kv
        fout.write("%s\t%s\n" % (k, v))

    fout.close()
    print(cc)
    print(len(kegg_set))
    return kegg_set

def tmp_extraction(file_in, file_out):
    fin = open(file_in, "r")
    to_be_translated = []
    output = []
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip().split("\t")
        if line[1] != "[]":
            print(line)
            print(line[1])
            print(line[1] != "")
            continue
        else:
            phrase = line[0]
            print(phrase)
            to_be_translated.append(phrase)
    for phrase in to_be_translated:
        # phrase = jaconv.z2h(phrase, kana=False, ascii=True, digit=True)
        output.append(phrase)

    with open(file_out, "w") as fout:
        for elem in output:
            fout.write(elem + "\n")

if __name__ == "__main__":
    # dict_file = "%s/KEGG3.dict" % params.TMP_DIR
    out_file = "%s/JADER_KEGG_ROUND3.txt" % params.TMP_DIR
    # parser(dict_file, out_file, mod = True)
    to_be_translated_file = "/home/petschnerp/PycharmProjects/NISEI/tmp/to_be_translated_origin.txt"
    tmp_extraction(out_file, to_be_translated_file)
