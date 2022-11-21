import os

C_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = "%s/resource" % C_DIR

ACC_DIR = "%s/Acc" % RES_DIR

# GOOGLE_AUTH_JSON_FILE = "/home/petschnerp/Documents/SOTE/Mamitsuka/DDI/JDDI/Data/pmdacasereport202104/melodic-gamma-313605-66b01efa7136.json"
GOOGLE_AUTH_JSON_FILE = "%s/google.json" % ACC_DIR
MEDDRA_ACCOUNT_FILE = "%s/Meddra.txt" % ACC_DIR


JADER_ORIGIN_DIR = "%s/JADEROrigin" % RES_DIR
JADER_UNICODE_DIR = "%s/JADERUnicode" % RES_DIR
JADER_TRANSLATION_DIR = "%s/JADERTranslation" % RES_DIR
TMP_DIR = "%s/tmp" % C_DIR
PRERUN_DIR = "%s/prerun" % RES_DIR
JADER_DRUG_FILES = ["%s/drug_utf.csv" % JADER_UNICODE_DIR]
JADER_DRUG_SKIP_COLUMNS = [{0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}]

JADER_MEDRRA_FILES = ["%s/drug_utf.csv" % JADER_UNICODE_DIR, "%s/hist_utf.csv" % JADER_UNICODE_DIR,
                      "%s/reac_utf.csv" % JADER_UNICODE_DIR]

JADER_MEDDRA_SKIP_COLUMNS = [{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15}, {0, 1, 2}, {0, 1, 2, 4, 5}]

JADER_TRANS_FILES = ["%s/drug_utf.csv" % JADER_UNICODE_DIR, "%s/hist_utf.csv" % JADER_UNICODE_DIR,
                     "%s/reac_utf.csv" % JADER_UNICODE_DIR, "%s/demo_utf.csv" % JADER_UNICODE_DIR]
JADER_TRANS_SKIP_COLUMS = [[{0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 13, 15}, {0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 14}], [{0, 1, 2}, {-1}], [{0, 1, 2, 4, 5},{0, 1, 2, 3, 5} ], [{-1}, {0, 1, 10}] ]
# -1 means skip all columns

JADER_LEFTOVER_FILES = ["%s/demo_utf.csv" % JADER_UNICODE_DIR, "%s/drug_utf.csv" % JADER_UNICODE_DIR,
                        "%s/reac_utf.csv" % JADER_UNICODE_DIR]
JADER_LEFTOVER_SKIP_COLUMNS = [{0, 1, 10}, {0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 14}, {0, 1, 2, 3, 5}]

DRUG_ALL_PHRASE_FILE = "%s/AllDrugPhrases.txt" % TMP_DIR
MEDDRA_ALL_PHRASE_FILE = "%s/AllMEDDRAPhrases.txt" % TMP_DIR
LELFOVER_ALL_PHRASE_FILE = "%s/AllLeftOverPhrases.txt" % TMP_DIR
LELFOVER_ALL_PHRASE_TRANSLATED_FILE = "%s/AllLeftOverPhrases_google.txt" % TMP_DIR


GOOGLE_TRANSLATED_DRUG_FILE = "%s/AllPhrases_DRUGNAMES_google.txt" % TMP_DIR
DRUGBANK_FILE = "%s/DrugBank/DrugBankNames.txt" % RES_DIR

## 4th round
JADER_4_th_ROUND_INPUT = "/home/petschnerp/PycharmProjects/NISEI/tmp/to_be_translated.txt"
JADER_4_th_ROUND_TRANSLATED =  "/home/petschnerp/PycharmProjects/NISEI/tmp/to_be_translated_translated.txt"
JADER_4_th_ROUND_PERFECT_MATCH_FILE = "/home/petschnerp/PycharmProjects/NISEI/tmp/JADER_4th_perfMatch.txt"
JADER_4_th_ROUND_NO_MATCH_FILE = "/home/petschnerp/PycharmProjects/NISEI/tmp/JADER_4th_noMatch.txt"


JADER_DRUG_PERFECT_MATCH_FILE = "%s/JADERDrugBank.txt" % TMP_DIR
JADER_DRUG_NO_MATCH_FILE = "%s/JADERNoneDrugBank.txt" % TMP_DIR
JADERDRUG_KEGG_SEARCH_RAW_FILE1 = "%s/KEGGMAP.dict" % TMP_DIR
JADER_MANUAL_MAP_FILE = "%s/JADERDrugManualFinal.txt" % TMP_DIR
JADER_MANUAL_MAP_FILE_2 = "%s/FixR4.txt" % TMP_DIR
MEDDRA_SEARCH_RAW_DICT_FILE = "%s/MeddraSearchRaw.dict" % TMP_DIR
MEDDRA_TEXT_MAP = "%s/MeddraMap.txt" % TMP_DIR
MEDDRA_MANUAL_MAP = "%s/MeddraManual.txt" % TMP_DIR

MEDDRA_MISSING_TERMS = "%s/MeddraMissing.txt" % TMP_DIR
TEXT_MAP_R1_FILE = "%s/JADER_KEGG_ROUND1.txt" % TMP_DIR
TEXT_MAP_R2_FILE_PREF = "%s/JADER_KEGG_ROUND2" % TMP_DIR
TEXT_MAP_R3_FILE = "%s/JADER_KEGG_ROUND3.txt" % TMP_DIR
JADER_ALL_HEADER_FILE = "%s/AllHeader.txt" % TMP_DIR
JADER_ALL_HEADER_TRANSLATION_FILE = "%s/AllHeaderTranslation.txt" % TMP_DIR
JADER_TRANS_COMB_FILE = "%s/JADERTransComb.txt" % TMP_DIR

MISSING_FILE = "%s/Missing.txt" % TMP_DIR
MISSING_TRANS_FIX_FILE = "%s/FixMissing.txt" % TMP_DIR

MISSING_INNER_PHRASES = "%s/MissingInnerTokens.txt" % TMP_DIR
MISSING_INNER_PHRASES_TRANS = "%s/TransMissingInnerTokens.txt" % TMP_DIR
MEDDRA_USE_NOMATCH = True
SKIP_TRANS_NO_MAP_DRUG_COL = True

## FILTERING
DO_APPLY_FILTERING = True
FILTERING_TERMS = ["noMatch", "others", "nutrition", "infusion", "contrast agents","dialysis solution","transfusion","vaccine"]
CONTRAST_AGENTS_KEGG = ["Iohexol","technetium tc 99m tetrofosmin","technetium tc 99m medronate","technetium tc 99m succimer","strontium chloride sr 89","67ga) citrate","thallous chloride tl 201","technetium","technetium tc 99m exametazime","galactosyl human serum albumin diethylenetriamine pentaacetic acid technetium",
                        "sodium pertechnetate tc 99m","iofetamine hydrochloride i 123","iopamidol","barium sulfate","xenon xe 133","ioflupane i 123","125i)","indium in 111 pentetreotide","iodine i 124 girentuximab","urea c13","radium ra 223 dichloride","sodium phosphate p 32", "iomeprol", "meglumine gadopentetate", "ioxilan", "gadoteridol",
                        "gadoteric acid", "ioversol", "gadobutrol"]
TRANSFUSIONS = ["washed human red blood cells","concentrated human red blood cells","fresh-frozen human plasma","synthetic blood","concentrated human blood platelet","whole human blood","human serum albumin","albumin human"]

