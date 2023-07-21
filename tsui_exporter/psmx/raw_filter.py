import utilss as utils
import paramss as params
import glob
import os




# def loadValidDrugMap():
#     path = "%s/finalMap/DrugFMap.txt" % params.OUTPUT_DIR
#     d = dict()
#     if os.path.isfile(path):
#         lines = open(path).readlines()
#         for line in lines:
#             line = line.strip()
#             parts = line.split("||")
#             d[parts[0]] = parts[1]
#     return d

def loadValidDrugBankMap():
    path = "%s/DrugBank/DrugBankNameX.txt" % params.DATA_DIR
    d = {}
    f = open(path)
    while True:
        line = f.readline()
        if line == "":
            break
        line = line.strip().lower()
        parts = line.split("||")
        hardName = parts[0]
        synonyms = parts[-2].split("|")
        salts = parts[-1].split("|")
        if len(synonyms) == 1 and synonyms[0] == "":
            synonyms = []
        if len(salts) == 1 and salts[0] == "":
            salts = []
        d[hardName] = hardName
        for s in synonyms:
            d[s] = hardName
        for s in salts:
            d[s] = hardName
    return d

def statTSUI():
    fin = open("%s/FinalTSUI.txt" % params.DATA_DIR)
    dSeCount = dict()
    dDrugCount = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.lower().strip().split("\t")
        drugs = parts[1].split(",")
        ses = parts[-1].split(",")
        for drug in drugs:
            utils.add_dict_counter(dDrugCount, drug.strip())
        for se in ses:
            utils.add_dict_counter(dSeCount, se.strip())
    drugCounts = utils.sort_dict(dDrugCount)
    seCounts = utils.sort_dict(dSeCount)
    foutDrugCount = open("%s/DrugStats.txt" % params.TMP_DIR, "w")
    for k, v in drugCounts:
        foutDrugCount.write("%s\t%s\n" % (k, v))
    foutDrugCount.close()

    foutSECount = open("%s/SEStats.txt" % params.TMP_DIR, "w")
    for k, v in seCounts:
        foutSECount.write("%s\t%s\n" % (k, v))
    foutSECount.close()



def filterTSUI():
    d = loadValidDrugBankMap()
    print("Total DB names", len(d))
    fin = open("%s/FinalTSUI.txt" % params.DATA_DIR)
    fout = open("%s/TSUI.txt" % params.TMP_DIR, "w")
    validDrugs = set()
    invalidDrugs  = set()
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.lower()
        parts = line.strip().split("\t")
        drugs = parts[1].split(",")
        isValid = True

        for drug in drugs:
            if drug not in d:
                invalidDrugs.add(drug)
                isValid = False

                break
            validDrugs.add(drug)
        if isValid:
            fout.write("%s$%s\n" % (parts[1], parts[-1]))
    fout.close()
    fInvalid = open("%s/InvalidDrugs.txt" % params.TMP_DIR, "w")
    fInvalid.write("\n".join(sorted(list(invalidDrugs))))
    fInvalid.close()
    fValid = open("%s/ValidDrug.txt" % params.TMP_DIR, "w")
    fValid.write("\n".join(sorted(list(validDrugs))))
    fValid.close()
def exportTSUI2():
    d = loadValidDrugBankMap()
    fin = open("%s/FinalTSUI.txt" % params.DATA_DIR)
    fout = open("%s/TSUIInd.txt" % params.TMP_DIR, "w")
    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split("\t")
        drugs = parts[1].split(",")
        # indicates = parts[2].split(",")
        isValid = True
        for drug in drugs:
            if drug not in d:
                isValid = False
                break
        if isValid:
            fout.write("%s$%s$%s$%s\n" % (parts[1], parts[2], "NoGender","NoIndication"))
    fout.close()

def exportTSUIPair():
    fin = open("%s/TSUIInd.txt" % params.TMP_DIR)
    # fout = open("%s/TSUIIndPair.txt" % params.TSUI_OUT, "w")
    validDrugs = dict()
    validPairs = dict()
    validIndicates = dict()
    validSes = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip()
        parts = line.split("$")
        drugComb = parts[0]
        indications = parts[2]
        ses = parts[3]
        drugs = drugComb.split(",")
        for drug in drugs:
            utils.add_dict_counter(validDrugs, drug)
        for ind in indications.split(","):
            utils.add_dict_counter(validIndicates, ind)
        for se in ses.split(","):
            utils.add_dict_counter(validSes, se)
        if len(drugs) >= 2 and len(drugs) <= 20:
            drugs = sorted(drugs)
            for i in range(len(drugs)):
                for j in range(i + 1, len(drugs)):
                    d1, d2 = drugs[i], drugs[j]
                    pair = "%s,%s" % (d1, d2)
                    utils.add_dict_counter(validPairs, pair)


    cDrug = utils.sort_dict(validDrugs)
    cInd = utils.sort_dict(validIndicates)
    cSe = utils.sort_dict(validSes)
    cPair = utils.sort_dict(validPairs)
    writeSortedDictC(cDrug, "%s/STSUIADrugs.txt" % params.TMP_DIR)
    writeSortedDictC(cInd, "%s/STSUIAInd.txt" % params.TMP_DIR)
    writeSortedDictC(cSe, "%s/STSUIASe.txt" % params.TMP_DIR)
    writeSortedDictC(cPair, "%s/STSUIPairs.txt" % params.TMP_DIR)

def writeSortedDictC(dl, p):
     f = open(p, "w")
     for kv in dl:
         k, v = kv
         f.write("%s\t%s\n" % (k, v))
     f.close()


if __name__ == "__main__":
    # statTSUI()
    # filterTSUI()
    #exportTSUI2()
    #exportTSUIPair()
    pass