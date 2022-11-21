import utilss as utils
import paramss as params

import numpy as np
from scipy.stats import fisher_exact
from multiprocessing import Process, Value, Queue
import time

P_THRESHOLD = 0.05
MIN_COMB_COUNT = 2
MIN_SE_COUNT = 20
_exact = fisher_exact



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

def filterTSUI():
    d = loadValidDrugBankMap()
    print("Total DB names", len(d))
    fin = open(params.JADER_TRANS_COMB_FILE)
    fout = open("%s/JADERFiltered.txt" % params.TMP_DIR, "w")
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

def statsCommonSes():
    fin = open("%s/JADERFiltered.txt" % (params.TMP_DIR))
    dSeCout = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.lower()
        parts = line.strip().split("$")
        ses = parts[-1].split(",")
        for se in ses:
            utils.add_dict_counter(dSeCout, se)
    kvs = utils.sort_dict(dSeCout)
    ks = []
    for kv in kvs:
        k, v = kv
        if v <= MIN_SE_COUNT:
            continue
        ks.append(k)
    utils.save_obj(ks, "%s/SeTopList.txt" % params.TMP_DIR)


def exportAllSesG2():
    seList = utils.load_obj("%s/SeTopList.txt" % params.TMP_DIR)
    print(seList[:20])
    # seList = ['product dose omission']
    nSize = 100
    import os
    p = params.TMP_STATS_DIR
    cmd = "rm %s" % p
    try:
        os.system(cmd)
    except:
        pass
    pathIn1 = "%s/JADERFiltered.txt" % (params.TMP_DIR)
    pathInfo1 = "%s/StatsFileMap.txt" % params.TMP_STATS_DIR
    dirOut1 = params.TMP_STATS_DIR
    fFileNameMap = open(pathInfo1, "w")
    fFileNameMap.close()

    nSeg = max(int(len(seList) / nSize), 1)

    for i in range(nSeg):
        start = i * nSize
        end = min((i + 1) * nSize, len(seList))
        exportBySE(seList[start:end], pathIn1, dirOut1, pathInfo1)


def producer(queue, arrs):
    for comAr in arrs:
        com, ar = comAr
        p = _exact(ar, 'greater')

        queue.put([com, ar[0, 0], p])


def consumer(queue, counter, counter2, fout=None, caches=None):
    while True:
        data = queue.get()
        if data is None:
            print("Receive terminate signal")
            with counter.get_lock():
                counter.value = 1
            if caches is not None:
                for line in caches:
                    fout.write("%s" % line)

            fout.flush()
            break
        com, cc, p = data
        with counter2.get_lock():
            counter2.value += 1

        # print(drugJader,">>", drugBankName)
        if fout is not None:
            ord, pv = p
            if pv <= P_THRESHOLD:
                if caches is None:
                    fout.write("%s\t%s\t%s\t%s\n" % (com, cc, ord, pv))
                else:
                    caches.append("%s\t%s\t%s\t%s\n" % (com, cc, ord, pv))


def exportBySE(seNames, pathIn, dirOut, pathInfo):
    fin = open(pathIn)
    dCombCount = dict()
    dCombSe = dict()
    dSe = dict()
    nA = 0
    print("Reading...")
    oSeNames = seNames
    if not type(seNames) == set:
        seNames = set(seNames)
    print(oSeNames)
    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split("$")
        drugCmb = parts[0]
        ses = parts[-1]
        ses = set(ses.split(","))
        drugs = sorted(drugCmb.split(","))
        if len(drugs) > 20:
            continue

        nA += 1

        for se in oSeNames:

            drugPars = []

            if 2 <= len(drugs) <= 20:
                for i in range(len(drugs)):
                    for j in range(i + 1, len(drugs)):
                        d1 = drugs[i]
                        d2 = drugs[j]
                        pair = "%s,%s" % (d1, d2)
                        drugPars.append(pair)
                        dCombCountx = utils.get_insert_key_dict(dCombCount, se, dict())

                        utils.add_dict_counter(dCombCountx, pair)

            if se in sorted(list(ses)):
                utils.add_dict_counter(dSe, se)
                for pair in drugPars:
                    dComSEx = utils.get_insert_key_dict(dCombSe, se, dict())
                    utils.add_dict_counter(dComSEx, pair)

    fin.close()

    print("Cal Contingency table...")
    dContigenTable = dict()

    for se in oSeNames:
        dCombCountx = dCombCount[se]
        dComSEx = utils.get_dict(dCombSe, se, dict())
        nSe = utils.get_dict(dSe, se, 0)
        if nSe == 0:
            continue
        for drugComb, nComb in dCombCountx.items():
            ar = np.zeros((2, 2))
            nCombSe = utils.get_dict(dComSEx, drugComb, 0)
            if nCombSe == 0:
                # print("SKIP")
                continue
            ar[0, 0] = nCombSe
            ar[1, 0] = nComb - nCombSe
            ar[0, 1] = nSe - nCombSe
            ar[1, 1] = nA - (nComb + nSe - nCombSe)
            nName = "%s_%s" % (drugComb, se)
            dContigenTable[nName] = ar

    producers = []
    consumers = []
    queue = Queue(params.K_FOLD)
    counter = Value('i', 0)
    counter2 = Value('i', 0)

    inputList = list(dContigenTable.items())
    nInputList = len(inputList)
    nDPerWorker = int(nInputList / params.N_DATA_WORKER)
    # assert 'g-csf' in allDrugNames
    for i in range(params.N_DATA_WORKER):
        startInd = i * nDPerWorker
        endInd = (i + 1) * nDPerWorker
        endInd = min(endInd, nInputList)
        if i == params.N_DATA_WORKER - 1:
            endInd = nInputList
        data = inputList[startInd:endInd]
        producers.append(Process(target=producer, args=(queue, data)))

    sname = "__".join(list(seNames))
    seNameString = "%s" % hash(sname)

    fFileNameMap = open(pathInfo, "a")
    fFileNameMap.write("%s\t%s\n" % (seNameString, sname))
    fFileNameMap.close()
    fout = open("%s/%s" % (dirOut, seNameString), "w")
    p = Process(target=consumer, args=(queue, counter, counter2, fout, []))
    p.daemon = True
    consumers.append(p)

    print("Start Producers...")
    for p in producers:
        p.start()
    print("Start Consumers...")
    for p in consumers:
        p.start()

    for p in producers:
        p.join()
    print("Finish Producers")

    queue.put(None)

    while True:
        if counter.value == 0:
            time.sleep(0.01)
            continue
        else:
            break
    fout.flush()
    fout.close()


def mergeG2():
    fin = open("%s/StatsFileMap.txt" % params.TMP_STATS_DIR)
    fout = open("%s/FisherAll.txt" % params.TMP_STATS_DIR, "w")
    dDrug2Se = dict()

    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip()
        parts = line.split("\t")
        hashFile = parts[0]
        f = open("%s/%s" % (params.TMP_STATS_DIR, hashFile))
        while True:
            l = f.readline()
            if l == "":
                break
            parts = l.strip().split("_")

            drug = parts[0]
            p2 = parts[1].split("\t")
            se = p2[0]
            if se.__contains__('death'):
                continue
            n = float(p2[1])
            ord = float(p2[2])
            if n <= MIN_COMB_COUNT:
                continue
            ses = utils.get_insert_key_dict(dDrug2Se, drug, [])
            ses.append(se)
            # print(drug, ses)

        f.close()
    for k, v in dDrug2Se.items():
        fout.write("%s\t%s\n" % (k, ",".join(v)))
    fout.close()


def ensureDIR():
    utils.ensure_dir(params.TMP_DIR)
    utils.ensure_dir(params.TMP_STATS_DIR)
    utils.ensure_dir(params.TSUI_DIR)


def exportPolyGJADER():
    fin = open("%s/Data/DrugBank/DrugBankNameX.txt" % params.C_DIR)
    dName2Inchi = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        line = line.strip()
        parts = line.split("||")
        drugName = parts[0]
        inchi = parts[4]
        dName2Inchi[drugName] = inchi
    fin.close()

    fin = open("%s/FisherAll.txt" % params.TMP_STATS_DIR)
    fout = open("%s/TSUI_%s.txt" % (params.TSUI_DIR, MIN_COMB_COUNT), "w")

    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split("\t")
        d1, d2 = parts[0].split(",")
        ses = parts[1].split(",")

        se_filtered = ",".join(ses)
        i1, i2 = utils.get_dict(dName2Inchi, d1, -1), utils.get_dict(dName2Inchi, d2, -1)
        if i1 == -1 or i2 == -1:
            continue
        if len(i1) < 2 or len(i2) < 2:
            continue
        if len(se_filtered) < 2:
            continue
        line = "%s|%s|%s|%s|%s\n" % (d1, d2, i1, i2, se_filtered)
        # if not line.__contains__("death"):
        fout.write("%s" % line)
    fout.close()
    fin.close()

def clean_dir():
    import os
    os.system("rm -rf \"%s\"" % params.TMP_DIR)

def run_fisher_all():
    ensureDIR()

    filterTSUI()

    statsCommonSes()
    exportAllSesG2()
    mergeG2()
    exportPolyGJADER()
    clean_dir()


if __name__ == "__main__":
    run_fisher_all()
    pass
