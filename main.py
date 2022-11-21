import optparse

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


if __name__ == '__main__':
    ensure_dirs()
    # run_auto_search()
    # Wait for manual map

    run_translate()
