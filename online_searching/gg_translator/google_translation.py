import params
from online_searching.gg_translator.autherntication import auth
import six
from utils import utils


def load_files(input_path, num_segs=20):
    f = open(input_path, encoding="utf-8")
    lines = []
    while True:
        line = f.readline()
        if line == "":
            break
        if len(line) < 2:
            continue
        lines.append(line.strip())
    f.close()
    numLines = len(lines)
    segSize = int(numLines / num_segs)
    segLines = []

    for i in range(num_segs):
        start = i * segSize

        end = (i + 1) * segSize
        if i == num_segs - 1:
            end = numLines
        seg = lines[start:end]
        seg = " <br> ".join(seg)
        segLines.append(seg)
    return segLines


def translate_text(translate_client, text, source="ja", target="en", format="html"):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    result = translate_client.translate(text, source_language=source, target_language=target, format_=format)

    return result["translatedText"]


def google_translate(input_path, output_path):
    translate_client = auth()
    segLines = load_files(input_path=input_path)
    res = []
    for seg in segLines:
        transRe = translate_text(translate_client, seg)
        res.append(transRe)

    fout = open(output_path, "w")
    for ii, re in enumerate(res):
        print("Trans segments: ", ii)
        trans = re
        outs = trans.split("<br>")
        for out in outs:
            fout.write("%s\n" % (out.strip()))
    fout.close()


def translate_drugs():
    google_translate(params.DRUG_ALL_PHRASE_FILE, params.GOOGLE_TRANSLATED_DRUG_FILE)


def load_drug_google_translated_dict():
    # jader_drug_names = utils.read_all_lines(params.DRUG_ALL_PHRASE_FILE)
    jader_drug_names = utils.read_all_lines(params.JADER_4_th_ROUND_INPUT)
    # google_translated_drug_names = utils.read_all_lines(params.GOOGLE_TRANSLATED_DRUG_FILE)
    google_translated_drug_names = utils.read_all_lines(params.JADER_4_th_ROUND_TRANSLATED)
    assert len(jader_drug_names) == len(google_translated_drug_names)
    jader_drug_name_2_eng = {jader_drug_names[i]: google_translated_drug_names[i] for i in range(len(jader_drug_names))}
    return jader_drug_name_2_eng


if __name__ == "__main__":
    # translate_drugs()
    input_path = "/home/petschnerp/PycharmProjects/NISEI/tmp/to_be_translated.txt"
    output_path = "/home/petschnerp/PycharmProjects/NISEI/tmp/to_be_translated_translated.txt"
    google_translate(input_path, output_path)
    # tmp = load_files(input_path=input_path)
    # print(tmp)