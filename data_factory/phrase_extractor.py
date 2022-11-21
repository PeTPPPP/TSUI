import codecs
import io
import csv
import os
import params


def read_n_lines(f, n_line):
    """Reads in nLine lines from input (f)
    f - filename
    nLine - number of lines to read in
    replace - logical value indicating replacement of semicolon in output
    """
    lines = []
    cc = 0
    while True:
        line = f.readline()
        if line == "":
            break
        cc += 1
        lines.append(line)
        if cc == n_line:
            break

    return lines


def extract_phrases_from_file(jader_file, skip_columns=set(), separator=None, partitioner=None):
    """Exports phrases from file fName with skipIds column ids skipped
    fName - name of file to export phrases from
    skipIds - which columns to omit"""
    print("Extracting... %s" % jader_file)

    f = codecs.open(jader_file, "r", "utf-8")
    phrases = set()
    cc = 0
    while True:
        lines = read_n_lines(f, 10000)
        if len(lines) == 0:
            break
        for line in lines:
            if line == "\n":
                break
            cc += 1

            if cc > 0:
                if not line[0].isalpha():
                    continue

            if cc % 100 == 0:
                print("\r%s" % cc, end="")

            ios = io.StringIO(line.strip())
            token_list = list(csv.reader(ios))

            if len(token_list) == 0:
                continue
            token_list = token_list[0]

            for i in range(len(token_list)):
                if i in skip_columns:
                    continue
                token = token_list[i]
                if separator is not None:
                    token = token.split(separator)[0]
                if partitioner is not None and separator is None:
                    print("Separation of strings occurs only in columns containing multiple entries")
                    print("Add a separator too and re-run!")
                    break
                if partitioner and separator is not None:
                    token = token.partition(partitioner)[0]

                # if name == "経口;経口;経口;経口;経口;経口;経口;経口;経口;不明":
                #      print(fName)
                #      print(cc, i)
                #      exit()

                phrases.add(token)
    f.close()
    print("\nFound: %s phrases" % len(phrases))
    return phrases


def get_phrases(separator=None, partitioner=None, filename_out_path=None, filename_in_paths=None, skip_colums=None):
    """Using the export function getPhrases() command exports all phrases from the file list with the given column
    ids omitted.
    F_Names - list of file names to use with path
    F_SKIPS - list of columns to omit in every files of F_Names"""
    if filename_out_path is None:
        filename_out_path = input("Please, give a filename to contain extracted phrases: ")
    if filename_in_paths is None:
        filename_in_paths = input("Please enter valid filename to extract phrases from: ")
    names = set()
    for i in range(len(filename_in_paths)):
        ni = extract_phrases_from_file(filename_in_paths[i], skip_colums[i], separator=separator,
                                       partitioner=partitioner)
        print(ni)
        for n in ni:
            if n != "":
                names.add(n)

    print("\nTotal: %s phrases" % len(names))
    fOut = codecs.open(filename_out_path, "w", "utf-8")
    
    for n in names:

        fOut.write("%s\n" % n)
    fOut.close()

def get_header_line(path):
    f = codecs.open(path, "r", "utf-8")
    header = f.readline().strip()
    f.close()
    return header

def extract_all_header():
    paths = params.JADER_TRANS_FILES
    fout = open(params.JADER_ALL_HEADER_FILE, "w")
    for path in paths:
        header = get_header_line(path)
        fout.write("%s\n"%header)
    fout.close()




def extract_all_drug_phrases():
    get_phrases(filename_out_path=params.DRUG_ALL_PHRASE_FILE, filename_in_paths=params.JADER_DRUG_FILES,
                skip_colums=params.JADER_DRUG_SKIP_COLUMNS)
    os.system("sed 's/\"//' \"%s\"" % params.DRUG_ALL_PHRASE_FILE)


def extract_all_meddra_phrases():
    get_phrases(filename_out_path=params.MEDDRA_ALL_PHRASE_FILE, separator=";", partitioner="(", filename_in_paths=params.JADER_MEDRRA_FILES,
                skip_colums=params.JADER_MEDDRA_SKIP_COLUMNS)


def extract_all_leftover_phrases():
    get_phrases(filename_out_path=params.LELFOVER_ALL_PHRASE_FILE,  separator=";", partitioner="(", filename_in_paths=params.JADER_LEFTOVER_FILES,
                skip_colums=params.JADER_LEFTOVER_SKIP_COLUMNS)


def extract_all_phrases():
    extract_all_drug_phrases()
    extract_all_meddra_phrases()
    extract_all_leftover_phrases()
    extract_all_header()

if __name__ == "__main__":
    # extract_all_phrases()
    extract_all_header()
