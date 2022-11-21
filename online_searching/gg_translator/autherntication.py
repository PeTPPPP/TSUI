import os
from google.cloud import translate_v2 as translate

import params


def auth():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = params.GOOGLE_AUTH_JSON_FILE
    print("Initializing client...")
    translate_client = translate.Client()
    print("Translating...")
    return translate_client


