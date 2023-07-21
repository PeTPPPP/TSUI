import os
from params import JADER_TRANS_COMB_FILE, TSUI_FILE, DATA_DIR, DRUGBANK_FILE

C_DIR = os.path.abspath(os.path.dirname(__file__))

TSUI_DIR= "%s/out" % C_DIR
TMP_DIR = "%s/tmp" % C_DIR
TMP_STATS_DIR = "%s/stats" % TMP_DIR


QUEUE_SIZE = 10
N_DATA_WORKER = 5
P_THRESHOLD = 0.05
MIN_COMB_COUNT = 3
MIN_SE_COUNT = 20
