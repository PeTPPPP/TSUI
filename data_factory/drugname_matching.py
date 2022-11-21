import params
from utils import utils
from online_searching.gg_translator.google_translation import load_drug_google_translated_dict


def load_drugbank_names(sName=None):
    path = params.DRUGBANK_FILE
    fin = open(path)
    dHardDrug = dict()
    dSyn = dict()
    allNames = set()
    while True:
        line = fin.readline()
        if line == "":
            break
        name = line.strip().lower()
        parts = name.split("||")
        assert len(parts) == 2
        syns = parts[1].split("|")
        hardDrug = parts[0]
        if len(hardDrug) < 2:
            continue
        rsyns = set()
        for syn in syns:
            if len(syn) < 5:
                continue
            syn = syn.strip()
            rsyns.add(syn)
            allNames.add(syn)
            dHardDrug[syn] = hardDrug

        dSyn[hardDrug] = rsyns
        dHardDrug[hardDrug] = hardDrug

        allNames.add(hardDrug)

        # if sName is not None:
        #     if name == sName:
        #         print("Found %s"%sName)
        #         exit(-1)
    fin.close()
    # print(allNames)
    return dHardDrug, dSyn, allNames


def load_jader_translated_names():
    d = load_drug_google_translated_dict()
    d_translated_2_jader_names = dict()
    translated_names = set()
    for jader_name, en_translated_name in d.items():
        jader_name = jader_name.lower()
        en_translated_name = en_translated_name.lower()
        back_l = utils.get_insert_dict(d_translated_2_jader_names, en_translated_name, [])
        back_l.append(jader_name)
        translated_names.add(en_translated_name)
    return d_translated_2_jader_names, list(translated_names)

def is_valid_match(core_tokens, all_tokens):
    if all_tokens.__contains__(","):
        return False

    idx = all_tokens.find(core_tokens)
    if idx == -1:
        return False
    if idx > 0:
        if all_tokens[idx - 1].isalpha():
            return False
    return True



def producer(queue, datum):
    segdrugJader, drugBank = datum
    for drugJader in segdrugJader:
        for drugBankName in drugBank:
            if is_valid_match(drugBankName, drugJader):  # drugJader.__contains__(drugBankName):
                queue.put([drugJader, drugBankName])


def consumer(queue, counter, counter2, fout=None):
    while True:
        data = queue.get()
        if data is None:
            print("Receive terminate signal")
            with counter.get_lock():
                counter.value = 1
            fout.flush()
            break
        drugJader, drugBankName = data
        with counter2.get_lock():
            counter2.value += 1

        # print(drugJader,">>", drugBankName)
        if fout is not None:
            fout.write("%s||%s\n" % (drugJader, drugBankName))


def match():
    dHardDrug, dSyns, all_drugbank_names = load_drugbank_names()
    d_translated_name_2_jadername, translated_names = load_jader_translated_names()
    # print(d_translated_name_2_jadername)
    nMatch1 = 0
    jader_translated_matching_drugnames = set()
    jader_translated_no_matching_drugnames = set()
    for translated_name in translated_names:
        if translated_name in all_drugbank_names:
            nMatch1 += 1
            jader_translated_matching_drugnames.add(translated_name)
        else:
            jader_translated_no_matching_drugnames.add(translated_name)

    # f = open(params.JADER_DRUG_PERFECT_MATCH_FILE, "w")
    f = open(params.JADER_4_th_ROUND_PERFECT_MATCH_FILE, "w")
    for drug in sorted(jader_translated_matching_drugnames):
        jader_names = d_translated_name_2_jadername[drug]
        for jader_name in jader_names:
            f.write("%s||%s||%s\n" % (jader_name, drug, dHardDrug[drug]))
    f.close()
    # f = open(params.JADER_DRUG_NO_MATCH_FILE, "w")
    f = open(params.JADER_4_th_ROUND_NO_MATCH_FILE, "w")
    for translated_no_matching_name in jader_translated_no_matching_drugnames:
        jader_names = d_translated_name_2_jadername[translated_no_matching_name]
        for jader_name in jader_names:
            f.write("%s||%s\n" % (jader_name, translated_no_matching_name))
    f.close()

def match_drug_bank(drug_inputs):
    perfect_match = set()
    matching_re = []
    dHardDrug, dSyns, all_drugbank_names = load_drugbank_names()

    for drug in drug_inputs:
        if drug.lower in all_drugbank_names:
            perfect_match.add(drug)
            matching_re.append([drug, dHardDrug[drug]])
    return perfect_match, matching_re


if __name__ == "__main__":
    match()