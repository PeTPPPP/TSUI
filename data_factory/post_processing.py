import params
import re
import csv


def replace_strings(str_to_replace, str_to_replace_with, file_in, file_out):
    with open(file_in, "r") as fin:
        fildat = fin.read()
        fildat = fildat.replace(str_to_replace, str_to_replace_with)
    with open(file_out, "w") as fout:
        fout.write(fildat)


def find_combinations_and_basic_active_substances_KEGG_entries(files):

    KEGG_simple_name_dictionary = dict()
    list_of_combiations = []
    cc = 0
    for file in files:
        fin = open(file, "r")
        while True:
            line = fin.readline()
            if line == "":
                break

            line = line.strip().split("\t")
            KEGG_entries = re.findall(r"'[^']*'", line[1])
            print(KEGG_entries)
            if len(KEGG_entries) > 1:
                if KEGG_entries[1].__contains__(" and "):
                    list_of_combiations.append(KEGG_entries[1].strip("'"))
                    print("Found combination: ", KEGG_entries[1].strip("'"))
                    cc += 1
                else:
                    for i in range(len(KEGG_entries)):
                        KEGG_simple_name_dictionary.update({KEGG_entries[i].strip("'").lower(): KEGG_entries[i].strip("'")})
        fin.close()
    print("Nr of combinations: ", cc)
    print(len(list(set(list_of_combiations))))
    return list(set(list_of_combiations)), KEGG_simple_name_dictionary

def create_combs_active_ingredients_map(list_of_combinations, simple_names_dict):
    error_list = []
    output_dict = dict()
    for comb in list_of_combinations:
        comb_split = re.split(r" and |, ", comb)
        ingredients = []
        for substance in comb_split:
            if substance.lower() not in simple_names_dict.keys():
                print("Basic ingredient %s not found" % substance.lower())
                error_list.append(substance)

            ingredients.append(substance)
        output_dict.update({comb: ingredients})


    return output_dict, error_list

def replace_comb_drug_entries_in_translation(comb_active_ingredient_dict, translated_drug_file, output_file):
    fin = open(translated_drug_file, "r")
    fout = open(output_file, "w")

    while True:
        line = fin.readline()

        if line == "":
            break
        line = line.strip().split("\t")

        if len(line) < 4:
            to_print = ("\t").join(line)
        else:
            drug_names = line[4]
            drug_names = drug_names.split("|")
            for i, drug_name in enumerate(drug_names):
                if drug_name in comb_active_ingredient_dict.keys():
                    drug_names[i] = ("|").join(comb_active_ingredient_dict[drug_name])
            line[4] = "|".join(drug_names)
            to_print = ("\t").join(line)
        fout.write(to_print + "\n")

    fin.close()
    fout.close()


def create_main_salt_synonym_map(file_in):
    fin = open(file_in, "r")
    main_syn_salt_map = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip().split("||")
        main = line[0]
        terms = list(line[6].strip().split("|") + line[7].strip().split("|"))
        terms = list(filter(None, terms))
        for term in terms:
            if term not in main_syn_salt_map.keys():
                main_syn_salt_map.update({term.lower(): main})

    return main_syn_salt_map

def replace_syn_salt_wt_main(syn_salt_map, translated_drug_file, output_file):
    fin = open(translated_drug_file, "r")
    fout = open(output_file, "w")
    not_found = []
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip().split("\t")

        if len(line) < 4:
            to_print = ("\t").join(line)
        else:
            drug_names = line[4].lower()
            # if drug_names.startswith("nomatch"):
            #     line[4] = "noMatch"
            #     to_print = ("\t").join(line)
            #     fout.write(to_print + "\n")
            #     continue

            drug_names = drug_names.split("|")
            for i, drug_name in enumerate(drug_names):
                if drug_name in syn_salt_map.keys():

                    drug_names[i] = syn_salt_map[drug_name]
                else:
                    not_found.append(drug_name)
            line[4] = "|".join(drug_names)
            to_print = ("\t").join(line)
        fout.write(to_print + "\n")
    print(list(set(list(filter(None,not_found)))))
    print("Nr. of drugs not found among salts/synonyms: ", len(list(set(list(filter(None,not_found))))))
    print("FINISHED")
    fin.close()
    fout.close()

def create_contrast_transfusion_dict():
    contrasts_transfusion_dict = dict()
    for term in params.CONTRAST_AGENTS_KEGG:
        contrasts_transfusion_dict.update({term.lower(): "contrast agents"})
    for term in params.TRANSFUSIONS:
        contrasts_transfusion_dict.update({term.lower(): "transfusion"})
    return contrasts_transfusion_dict


def replace_contrast_transfusion(translated_file, output_file):
    fin = open(translated_file, "r")
    fout = open(output_file, "w")
    contrast_transfusion_dict = create_contrast_transfusion_dict()
    while True:
        line = fin.readline()

        if line == "":
            break
        line = line.strip().split("\t")

        if len(line) < 4:
            to_print = ("\t").join(line)
        else:
            drug_names = line[4].lower()
            drug_names = drug_names.split("|")
            for i, drug_name in enumerate(drug_names):
                if drug_name in contrast_transfusion_dict.keys():
                    drug_names[i] = contrast_transfusion_dict[drug_name]
            line[4] = "|".join(drug_names)
            to_print = ("\t").join(line)
        fout.write(to_print + "\n")

    fin.close()
    fout.close()

def checklines(original, new_file):
    fin1 = open(original, "r")
    fin2 = open(new_file, "r")
    cc = 0
    while True:
        line = fin1.readline()
        line2 = fin2.readline()
        if line == "":
            break
        line = line.strip().split(",")
        ID1 = line[0]
        line2 = line2.strip().split("\t")
        ID2 = line2[0]

        if ID1 != ID2 and cc != 0:
            print("ID not matching")
            print("Original:", line)
            print("New file:", line2)
            print("Row number:", cc)
            exit(-1)
        cc += 1
    fin1.close()
    fin2.close()

def write_dict_keys_to_file(dc, file_out):
    with open(file_out, "w") as f:
        for k in dc.keys():
            f.write(k + "\n")

def sort_dict(dd):
    kvs = []
    for key, value in sorted(dd.items(), key=lambda p: (p[1], p[0])):
        kvs.append([key, value])
    return kvs[::-1]

def write_list_to_file(lst, file_out):
    with open(file_out, "w") as f:
        for elem in lst:

            f.write(elem + "\n")

def create_KEGG_terms_dict(files):

    KEGG_simple_name_dictionary = dict()
    for file in files:
        fin = open(file, "r")
        while True:
            line = fin.readline()
            if line == "":
                break

            line = line.strip().split("\t")

            KEGG_entries = re.findall(r"'[^']*'", line[1])
            if len(KEGG_entries) > 1:
                if KEGG_entries[1].__contains__(" and "):
                    KEGG_simple_name_dictionary.update({KEGG_entries[1].strip("'").lower(): KEGG_entries[1].strip("'")})
            else:
                KEGG_entries = line[1].strip("'")
            KEGG_simple_name_dictionary.update({KEGG_entries[1].strip("'").lower(): KEGG_entries[1].strip("'")})
        fin.close()

    sort_dict(KEGG_simple_name_dictionary)
    return KEGG_simple_name_dictionary

def counting_crossmappings(file_in):
    fin = open(file_in, "r")
    ckeg = 0
    cc = 0
    while True:
        line = fin.readline()
        if line == "":
            break
        cc += 1
        line = line.strip().split("||")
        if line[3] != "NoKEGG":
            ckeg += 1
    print("Total drugs: ", cc)
    print("Drugs with valid Kegg ID: ", ckeg)
    print(100*(ckeg/cc))


def run():
    files_list = ["/home/petschnerp/PycharmProjects/NISEI/tmp/JADER_KEGG_ROUND1.txt",
                   "/home/petschnerp/PycharmProjects/NISEI/tmp/JADER_KEGG_ROUND2.txt",
                   "/home/petschnerp/PycharmProjects/NISEI/tmp/JADER_KEGG_ROUND3.txt",
                   "/home/petschnerp/PycharmProjects/NISEI/tmp/JADER_KEGG_ROUND4.txt"]
    list_of_combinations, simple_names_dict = find_combinations_and_basic_active_substances_KEGG_entries(files_list)
    comb_active_ingredient_dict, _ = create_combs_active_ingredients_map(list_of_combinations, simple_names_dict)
    replace_comb_drug_entries_in_translation(comb_active_ingredient_dict, "/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN.csv",
                                "/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN_NISEI.csv")
    print("FINISHED replacing combinations...")
    replace_contrast_transfusion(
        "/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN_NISEI.csv",
        "/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN_NISEI_DM.csv")
    salt_map_file = "/home/petschnerp/PycharmProjects/NISEI/resource/DrugBank/DrugBankNameX.txt"
    # counting_crossmappings(salt_map_file)
    syn_salt_map = create_main_salt_synonym_map(salt_map_file)
    replace_syn_salt_wt_main(syn_salt_map, "/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN_NISEI_DM.csv", "/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN_NISEI_DM_FINAL.csv")
    checklines("/home/petschnerp/PycharmProjects/NISEI/resource/JADERUnicode/drug202104_utf.csv", "/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN_NISEI_DM_FINAL.csv")
    # replace_terms_for_KEGG_drugs("/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN.csv", "/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN_MODDED.csv")

if __name__ == "__main__":
    run()

# def salt_forms(file_in):
#     fin = open(file_in, "r")
#     salt_forms_list = []
#     _list_of_salts_for_one_drug = []
#     _id_list = []
#     names = []
#     DB_ids = []
#     cc = 0
#     while True:
#         line = fin.readline()
#         if line == "":
#             salt_forms_list.append(list(set(_list_of_salts_for_one_drug)))
#             break
#         if cc == 0:
#             _id_list.append("Whatever")
#             cc += 1
#             continue
#         line = line.strip().split("\t")
#         name = line[1]
#         DB_id = line[0]
#
#         if not(name.__contains__(_id_list[-1]) and len(_id_list[-1]) < len(name)):
#             print("TRUE")
#             salt_forms_list.append(_list_of_salts_for_one_drug)
#             _list_of_salts_for_one_drug = []
#             _list_of_salts_for_one_drug.append(name)
#             names.append(name)
#             DB_ids.append(DB_id)
#         else:
#             _list_of_salts_for_one_drug.append(name)
#     for entry in salt_forms_list:
#         if len(entry) >> 1:
#             print(entry)
#     fin.close()

# def replace_terms_for_KEGG_drugs(file_in, file_out):
#     fin = open(file_in, "r")
#     fout = open(file_out, "w")
#     while True:
#         line = fin.readline()
#         if line == "":
#             break
#         line = line.strip().split("\t")
#
#         if len(line) < 6:
#             to_print = ("\t").join(line)
#         else:
#             proprietary_name = line[5]
#             for term in params.FILTERING_TERMS:
#                 if proprietary_name.startswith(term):
#                     line[4] = term
#                     break
#
#             to_print = ("\t").join(line)
#         fout.write(to_print + "\n")
#
#     print("FINISHED")
#     fin.close()
#     fout.close()
#
#     KEGG_dc = create_KEGG_terms_dict(files_list)
#     lst = sort_dict(KEGG_dc)
#     file_out = "/home/petschnerp/PycharmProjects/NISEI/tmp/KEGG_terms_dict.txt"
#     with open(file_out, "w") as fout:
#         for elem in lst:
#             writer = csv.writer(fout)
#             writer.writerow(elem)
