from optparse import OptionParser

import params
from utils import utils


def ensure_dirs():
    utils.ensure_dir(params.TMP_DIR)
    utils.ensure_dir(params.JADER_TRANSLATION_DIR)


def run_auto_search():
    from online_searching.meddra.meddra import run_auto_meddra_search
    from online_searching.kegg.kegg import run_auto_kegg_search
    run_auto_kegg_search()
    run_auto_meddra_search()


def run_translate():
    from translator.db_translator import run_translation_1, extract_missing_inner_tokens
    run_translation_1()
    # extract_missing_inner_tokens()


def create_jader_translation_combination():
    # Write to params.JADER_TRANS_COMP
    pass

def convert():
    import os
    data_names = ["drug", "hist", "reac", "demo"]
    # JADER_ORIGIN_DIR = "%s/JADEROrigin" % RES_DIR
    for name in data_names:
        cmd = "iconv -f EUC-JP -t UTF-8 \"%s/%s*\" > %s/%s_utf.csv" % (
        params.JADER_ORIGIN_DIR, name, params.JADER_UNICODE_DIR, name)
        os.system(cmd)


if __name__ == '__main__':
    ensure_dirs()
    parser = OptionParser()
    parser.add_option("-c", dest="c", type="store_true", help="convert format")
    parser.add_option("-p", dest="p", type="store_true", help="extracting phrases")
    parser.add_option("-a", dest="a", type="store_true", help="auto search")
    parser.add_option("-t", dest="t", type="store_true", help="translate")
    parser.add_option("-x", dest="x", type="store_true", help="extracting TSUI")

    (options, args) = parser.parse_args()
    if options.c:
        convert()
    if options.p:
        # Extracting all JADER phrases
        from data_factory.phrase_extractor import extract_all_phrases

        extract_all_phrases()
    elif options.a:
        # Search mapping from JADER phrases to corresponding English terms
        run_auto_search()
    elif options.t:
        # Run translation
        run_translate()
    elif options.x:
        from tsui_exporter.fisher_stats import run_fisher_all
        create_jader_translation_combination()
        run_fisher_all()

