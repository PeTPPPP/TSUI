import os

C_DIR = os.path.dirname(os.path.abspath(__file__))

OUT_DATA_DIR = "%s/data" % C_DIR
IN_DATA_DIR = "%s/resource" % C_DIR
DRUGBANK_FILE = "%s/DrugBank/DrugBankNameX.txt" % IN_DATA_DIR
JADER_TRANS_COMB_FILE = "%s/JADERTransComb.txt" % IN_DATA_DIR
TSUI_FILE = "%s/TSUI_ML.txt" % OUT_DATA_DIR

