import params
import csv

def extract_ids_drugs_or_reactions(file_in, reaction = False):
    id_list, drugs_or_reactions_list, _drugs_or_reactions_list_per_id = [], [], []
    if reaction == False:
        ## then its drugs
        print("Extraction of drugs...")
        column = 4
    else:
        print("Extraction of reactions...")
        column = 3
    fin = open(file_in, "r")
    cc = 0
    while True:
        line = fin.readline()
        if line == "":
            drugs_or_reactions_list.append(list(set(_drugs_or_reactions_list_per_id)))
            break
        if cc == 0:
            id_list.append("Whatever")
            cc += 1
            continue
        line = line.strip().split("\t")
        ID = str(line[0]) + str(line[1])

        if ID != id_list[-1]:

            drugs_or_reactions_list.append(list(set(_drugs_or_reactions_list_per_id)))

            _drugs_or_reactions_list_per_id = []
            if line[column].__contains__("|"):
                _ls = line[column].split("|")
                for it in _ls:
                    _drugs_or_reactions_list_per_id.append(it)
            else:
                _drugs_or_reactions_list_per_id.append(line[column])
            id_list.append(ID)
        else:
            if line[column].__contains__("|"):
                _ls = line[column].split("|")
                for it in _ls:
                    _drugs_or_reactions_list_per_id.append(it)
            else:
                _drugs_or_reactions_list_per_id.append(line[column])

    fin.close()
    print("FINISHED")
    return id_list[1:], drugs_or_reactions_list[1:]

def filtering_terms(id_list, drugs_list, reactions_list):
    terms_to_filter = params.FILTERING_TERMS
    _msk = [1] * len(id_list)
    for term in terms_to_filter:
        print(term)
        cc = 0
        for i in range(len(id_list)):
            # print(i)
            if drugs_list[i].__contains__(term) or reactions_list[i].__contains__(term):
                cc += 1
                _msk[i] == 0
        print(term, cc)
    # print(_msk)
    filtered_ids = [i for (i, v) in zip(id_list, _msk) if v]
    filtered_drugs = [i for (i, v) in zip(drugs_list, _msk) if v]
    filtered_reactions = [i for (i, v) in zip(reactions_list, _msk) if v]

    return filtered_ids, filtered_drugs, filtered_reactions


def printing_to_file(file_out, id_list, drugs_list, reactions_list):
    with open(file_out, "w") as fout:
        for i,_ in enumerate(id_list):
            line = id_list[i] + "\t" + ",".join(drugs_list[i]) + "\t" + ",".join(reactions_list[i])
            fout.write(line + "\n")

# def drugcheck():
#     fin = open("/home/petschnerp/PycharmProjects/NISEI/resource/JADERTranslation/drug202104_utf_EN.csv")
#     while True:
#         line = fin.readline()
#         if line == "":
#             break
#         line = line.strip().split("\t")
#         if line[5] != "":
#             try:
#                 if line[4] != line[5]:
#                     print("Case ID: " + line[0] + "Active ingredient: " + line[4] + "Proprietary name: " + line[5])
#             except:
#                 pass
def remove_needless_lines(twosides_file, file_out):
    fin = open(twosides_file, "r")
    fout = open(file_out, "w")
    cc = 0
    while True:
        line = fin.readline()
        if line == "":
            break
        if line.__contains__("nutrition") or line.__contains__("infusion") or line.__contains__("contrast agents") or line.__contains__("transfusion") or line.__contains__("others") or line.__contains__("nomatch") or line.__contains__("vaccine") or line.__contains__("noMatch"):
            continue
        else:
            cc += 1
            fout.write(line)
    print("Valid cases without summary terms or noMatch: ", cc)
    fin.close()
    fout.close()

def extract_oral_ids(file_in):
    fin = open(file_in, "r")
    id__oral_dict = dict()
    cc = 0
    while True:
        line = fin.readline()
        if line == "":
            break
        if cc == 0:
            cc += 1
            continue
        line = line.strip().split("\t")
        ID = str(line[0]) + str(line[1])
        if len(line) < 7:
            id__oral_dict.update({ID: 0})
            continue

        administration_route = line[6].strip().lower()


        if administration_route.startswith("oral") and ID not in id__oral_dict.keys():
            id__oral_dict.update({ID: 1})
        elif administration_route.startswith("oral") and ID in id__oral_dict.keys():
            pass
        elif not (administration_route.startswith("oral") and ID in id__oral_dict.keys()):
            id__oral_dict.update({ID: 0})
        else:
            id__oral_dict[ID] = 0

    output_dict = dict()
    for key in id__oral_dict.keys():
        if id__oral_dict[key] == 1:
            output_dict.update({key: id__oral_dict[key]})

    return output_dict

def restrict_output_to_oral(file_in, file_out, dc_oral_ids, twosides_format = False):
    fin = open(file_in, "r")
    fout = open(file_out, "w")
    cc = 0
    while True:
        line = fin.readline()
        if cc == 0 and not twosides_format:
            fout.write(line)
            cc += 1
            continue

        if line == "":
            break
        line = line.strip().split("\t")
        if twosides_format == True:
            ID = line[0]
        else:
            ID = line[0] + line[1]
        if ID in dc_oral_ids:
            to_print = ("\t").join(line)
            fout.write(to_print + "\n")



def run(filtering = params.DO_APPLY_FILTERING):
    id_list_from_drugs_file, drugs_list = extract_ids_drugs_or_reactions("%s/drug202104_utf_EN_NISEI_DM_FINAL.csv" % params.JADER_TRANSLATION_DIR)
    id_list_from_reactions_file, reactions_list = extract_ids_drugs_or_reactions("%s/reac202104_utf_EN.csv" % params.JADER_TRANSLATION_DIR, reaction=True)
    oral_id_dict = extract_oral_ids("%s/drug202104_utf_EN_NISEI_DM_FINAL.csv" % params.JADER_TRANSLATION_DIR)
    assert(id_list_from_drugs_file == id_list_from_reactions_file)
    if filtering == True:
        print(filtering)
        id_list_from_drugs_file, drugs_list, reactions_list = filtering_terms(id_list_from_drugs_file, drugs_list, reactions_list)
    twosides_file = "%s/NISEI_DM_TWOSIDES_FORMAT_FINAL_34.csv" % params.TMP_DIR
    printing_to_file(twosides_file, id_list_from_drugs_file, drugs_list, reactions_list)
    print("################################")
    print("Nr. of cases: ", len(id_list_from_drugs_file))
    _flat_drugs = set([item for ls in drugs_list for item in ls])
    print("Total nr. of unique drugs: ", len(_flat_drugs)-1) ## -1 for noMatch
    _flat_reactions = set([item for ls in reactions_list for item in ls])
    print("Total nr. of unique reactions: ", len(_flat_reactions)-1) ## -1 for noMatch
    nr_of_drug_noMatches = 0
    nr_of_reactions_noMatches = 0
    for drugs in drugs_list:
        if drugs.__contains__("nomatch"):
            nr_of_drug_noMatches += 1
    for reaction in reactions_list:
        if reaction.__contains__("noMatch"):
            nr_of_reactions_noMatches += 1
    print("Percentage lost due to noMatch drugs: ", (100*nr_of_drug_noMatches)/len(id_list_from_drugs_file))
    print(nr_of_drug_noMatches)
    print("Percentage lost due to noMatch reactions: ", (100*nr_of_reactions_noMatches)/len(id_list_from_drugs_file))
    filtered_output_file = "%s/NISEI_DM_TWOSIDES_FORMAT_FINAL_34.csv" % params.TMP_DIR
    remove_needless_lines(twosides_file=twosides_file, file_out=filtered_output_file)
    print("Nr. of cases with only per os administration: ",len(oral_id_dict.keys()))
    peroral_file = "%s/NISEI_DM_TWOSIDES_FORMAT_FINAL_peros_only.csv" % params.TMP_DIR
    restrict_output_to_oral("%s/NISEI_DM_TWOSIDES_FORMAT_FINAL_34.csv" % params.TMP_DIR, peroral_file, oral_id_dict, twosides_format=True)


if __name__ == "__main__":
    run()
    # drugcheck()



