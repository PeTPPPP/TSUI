from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import params
from utils import utils
import inspect

def getCurrentLineNo():
    return inspect.currentframe().f_back.f_lineno


def load_meddra_account():
    fin = open(params.MEDDRA_ACCOUNT_FILE)
    user_name = fin.readline().strip()
    pass_word = fin.readline().strip()
    fin.close()
    return user_name, pass_word


def init_browser():
    browser = webdriver.Firefox()
    browser.get('https://www.jmo.pmrj.jp/login')

    uname = browser.find_element(By.NAME, 'v_user')
    upass = browser.find_element(By.NAME,'v_pass')
    ok = browser.find_element(By.NAME,'v_ok')
    username, password = load_meddra_account()
    uname.send_keys(username)
    upass.send_keys(password)
    ok.click()

    time.sleep(1)

    searchBtn = browser.find_element(By.XPATH, '//a[@href="javascript:go(\'./MDRSearch\');"]')
    searchBtn.click()
    time.sleep(1)
    return browser



def loadExist(path):
    try:
        d = utils.load_obj(path)
    except:
        d = dict()

    return d


def loadSes(path, start=0, end=-1):
    lines = open(path).readlines()
    if end > len(lines):
        end = len(lines)
    lines = lines[start: end]

    # seLists = [line.strip().split('\t')[0] for line in lines]
    seLists = [line.strip() for line in lines]
    # print(seLists)
    return seLists


def run_search(input_path, raw_search_dict):
    browser = init_browser()
    d = loadExist(raw_search_dict)
    start = 1
    end = -1
    ses = loadSes(input_path, start, end)
    cc = start

    for jse in ses:

        if jse in d:
            print("Skip ",jse)
            continue
        try:
            print(cc, jse)
            cc += 1
            browser.switch_to.default_content()
            browser.switch_to.frame('main')
            inpE = browser.find_element(By.NAME, 'v_srh1')
            ok = browser.find_element(By.XPATH, '//a/img[@alt="検索"]')

            inpE.send_keys(jse)
            ok.click()

            time.sleep(3)
            browser.switch_to.default_content()
            browser.switch_to.frame('main')

            browser.switch_to.frame('result2')

            html = browser.find_element(By.TAG_NAME, 'body')
            html = html.get_attribute('innerHTML')

            d[jse] = html
            browser.switch_to.default_content()
            browser.switch_to.frame('menu')

            backBtn = browser.find_element(By.XPATH, '//a/img[@alt="検索条件"]')
            backBtn.click()
            time.sleep(2)
            if cc % 10 == 0:
                utils.save_obj(d, raw_search_dict)

        except Exception as e:
            print(e)
            utils.save_obj(d, raw_search_dict)
            exit(-1)

    utils.save_obj(d, raw_search_dict)




if __name__ == "__main__":
    run_search()
    pass