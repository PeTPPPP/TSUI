from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import params
from utils import utils
import inspect
from jaconv import jaconv


def getCurrentLineNo():
    return inspect.currentframe().f_back.f_lineno




def loadExist(path=None):
    try:
        d = utils.load_obj(path)
        print("loaded")
    except:
        d = dict()
        print("exception")

    return d

def loadSes(start=0, end=-1):
    lines = open(params.DRUG_ALL_PHRASE_FILE).readlines()
    if end > len(lines):
        end = len(lines)
    lines = lines[start: end]

    # seLists = [line.strip().split('\t')[0] for line in lines]
    seLists = [line.strip() for line in lines]
    # print(seLists)
    return seLists


def run_round1(d=None, ses=None, path=params.JADERDRUG_KEGG_SEARCH_RAW_FILE1):

    browser = webdriver.Firefox()
    browser.get('https://www.genome.jp/kegg/drug/drug_ja.html')

    time.sleep(1)

    search_Box = browser.find_element(By.XPATH, '//html/body/div[4]/div[1]/div[1]/form/input[1]')
    # browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
    search_Box.clear()
    search_Box.send_keys("tretinoin")
    ok = browser.find_element(By.XPATH, '//html/body/div[4]/div[1]/div[1]/form/input[5]')
    time.sleep(1)
    ok.click()
    time.sleep(1)

    if d is None:
        d = loadExist(path)

    start = 0
    end = -1
    if ses is None:
        ses = loadSes(start, end)
    cc = start

    for jse in ses:

        if jse in d:
            print("Skip ",jse)
            continue
        try:
            print(cc, jse, type(d.keys()), len(d), list(d.keys()))
            cc += 1
            search_Box = browser.find_element(By.XPATH, '//html/body/div[1]/form/input[1]')
            # browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
            search_Box.clear()
            jse2 = jaconv.z2h(jse, kana=False, digit=True, ascii=True)
            # print(jse, jse2)
            if jse2.isdigit():
                d[jse] = "None"
                # print(jse2.isdigit())
                continue
            search_Box.send_keys(jse2)
            time.sleep(1)
            # ヴォリブリス
            ## browser.switch_to.default_content()
            ## browser.switch_to.frame('main')
            ## inpE = browser.find_element_by_name('v_srh1')
            ok = browser.find_element(By.XPATH, '//html/body/div[1]/form/input[2]')

            ## inpE.send_keys(jse)
            ok.click()

            time.sleep(3)
            ## browser.switch_to.default_content()
            ## browser.switch_to.frame('main')

            ## browser.switch_to.frame('result2')

            html = browser.find_element(By.XPATH, '/html/body/div[3]/table')
            html = html.get_attribute('innerHTML')
            # print(html)
            # if mod=True:
            #     for key, value in dc.items():
            #         if jse == value:
            #             jse == key
            #         else
            #             exit(-1)
            #             print("Key is missing!")
            d[jse] = html
            ## browser.switch_to.default_content()
            ## browser.switch_to.frame('menu')

            ## backBtn = browser.find_element_by_xpath('//a/img[@alt="検索条件"]')
            ## backBtn.click()
            ## time.sleep(1)
            if cc % 20 == 0:
                utils.save_obj(d, path)

        except Exception as e:
            # try:
            #     jse = jaconv.z2h(jse, kana=True, digit=True, ascii=True)
            #     search_Box = browser.find_element_by_xpath('//html/body/div[1]/form/input[1]')
            #     search_Box.clear()
            #     search_Box.send_keys(jse)
            #     ok = browser.find_element_by_xpath('//html/body/div[1]/form/input[2]')
            #
            #     ok.click()
            #
            #     time.sleep(1)
            #     html = browser.find_element_by_xpath('/html/body/div[3]/table')
            #     html = html.get_attribute('innerHTML')
            #     print(html)
            #     d[jse] = html
            # except:
            #     continue
            d[jse] = "None"
            # print(e)
            utils.save_obj(d, path)
            ## exit(-1)
    # print(d.keys)
    utils.save_obj(d, path)


if __name__ == "__main__":
    run_round1()
    pass