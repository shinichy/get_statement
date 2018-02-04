#!/usr/bin/python
# coding=utf-8

# Get the statement of last month

import argparse
import time
from datetime import datetime, date, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

chromedriver_path = '/usr/local/bin/chromedriver'

today = date.today()
last_day = datetime(today.year, today.month, 1) - timedelta(days=1)


class Sites:
    suica = 'suica'
    sbi = 'sbi'
    jpnetbk = 'jpnetbk'
    ufj = 'ufj'
    enavi = 'enavi'
    smbc = 'smbc'

    @staticmethod
    def list():
        return [Sites.suica, Sites.sbi, Sites.jpnetbk, Sites.ufj, Sites.enavi, Sites.smbc]


def get_enavi_history(driver, username, password):
    # ログイン
    driver.get('https://www.rakuten-card.co.jp/e-navi/')
    driver.find_element_by_id('u').send_keys(username)
    driver.find_element_by_id('p').send_keys(password)
    driver.find_element_by_id('loginButton').click()

    # ご利用明細
    driver.get('https://www.rakuten-card.co.jp/e-navi/members/statement/index.xhtml?tabNo=1')
    driver.get('https://www.rakuten-card.co.jp/e-navi/members/statement/index.xhtml?downloadAsCsv=1')
    driver.get('https://www.rakuten-card.co.jp/e-navi/logout.xhtml?l-id=enavi_prelogout_cwd_logout')


def get_ufj_history(driver, username, password):
    # ログイン
    driver.get('https://entry11.bk.mufg.jp/ibg/dfw/APLIN/loginib/login?_TRANID=AA000_001')
    driver.find_element_by_id('account_id').send_keys(username)
    driver.find_element_by_id('ib_password').send_keys(password)
    driver.find_element_by_xpath(
        '//img[@src="https://directg.s.bk.mufg.jp/refresh/imgs/_DIRECT_IMAGE/LOGINOUT/btn_login_off.gif"]').click()

    # トップ
    driver.find_element_by_xpath(
        '//img[@src="https://directg.s.bk.mufg.jp/refresh/imgs/_DIRECT_IMAGE/LOGINOUT/btn_account_01_off.gif"]').click()

    # 入出金明細
    driver.find_element_by_xpath(
        '//img[@src="https://directg.s.bk.mufg.jp/refresh/imgs/_DIRECT_IMAGE/YEN/btn_meisai_download_off.gif"]').click()
    driver.find_element_by_id('last_month').click()
    driver.find_element_by_xpath(
        '//img[@src="https://directg.s.bk.mufg.jp/refresh/imgs/_DIRECT_IMAGE/COMMON/btn_download_off.jpg"]').click()
    driver.find_element_by_xpath('//li[@class="logout"]/a').click()


def get_smbc_history(driver, password, branch_no, account_no):
    # ログイン
    driver.get('https://direct.smbc.co.jp/aib/aibgsjsw5001.jsp')
    time.sleep(3)
    driver.find_element_by_id('S_BRANCH_CD').send_keys(branch_no)
    driver.find_element_by_id('S_ACCNT_NO').send_keys(account_no)
    driver.find_element_by_id('PASSWORD').send_keys(password)
    driver.find_element_by_name('bLogon.y').click()

    # トップ
    driver.find_element_by_xpath('//a[@title="明細照会"]').click()

    # 入出金明細
    driver.find_element_by_name('web_zengetu').click()
    driver.find_element_by_id('DownloadCSV').click()
    driver.find_element_by_xpath('//a[text()="ログアウト"]').click()


def get_jpnetbk_history(driver, username, password, branch_no, account_no):
    # ログイン
    driver.get('https://login.japannetbank.co.jp/wctx/LoginAction.do?loginIdFlg=1')
    driver.find_element_by_id('idTenNo').send_keys(branch_no)
    driver.find_element_by_id('idKozaNo').send_keys(account_no)
    driver.find_element_by_id('idLoginId').send_keys(username)
    driver.find_element_by_id('idPw').send_keys(password)
    driver.find_element_by_name('login').click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, 'centerContents')))
    driver.find_element_by_id('chk01').click()

    # ポップアップチェック
    popup = driver.find_element_by_xpath('//a[@href="javascript:infoFadeOut()"]')
    if popup:
        popup.click()

    wait.until(EC.invisibility_of_element_located((By.ID, 'seqInfo')))

    driver.find_element_by_xpath("//a[@href=\"javascript:commonSubmit('a0001')\"]").click()

    # 入出金明細
    Select(driver.find_element_by_name('ShokaiStartDateNenIn')).select_by_value(str(last_day.year))
    Select(driver.find_element_by_name('ShokaiStartDateTsukiIn')).select_by_value(str(last_day.month))
    Select(driver.find_element_by_name('ShokaiStartDateHiIn')).select_by_value('1')
    Select(driver.find_element_by_name('ShokaiEndDateNenIn')).select_by_value(str(last_day.year))
    Select(driver.find_element_by_name('ShokaiEndDateTsukiIn')).select_by_value(str(last_day.month))
    Select(driver.find_element_by_name('ShokaiEndDateHiIn')).select_by_value(str(last_day.day))
    driver.find_element_by_xpath('//input[@onclick="searchPeriod(this.form)"]').click()
    driver.find_element_by_xpath('//input[@type="button" and @value="PDF"]').click()

    # PDFダウンロードが別タブで開始されるので、終わるまで待つ
    time.sleep(10)

    driver.find_element_by_xpath('//a[@class="logout"]').click()

    # ポップアップが出現するまで待機
    wait.until(EC.alert_is_present())

    alert = driver.switch_to_alert()
    alert.accept()

    wait.until(EC.visibility_of_element_located((By.ID, 'title')))

    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


def get_sbi_history(driver, username, password):
    # ログイン
    driver.get('https://www.netbk.co.jp/wpl/NBGate')
    driver.find_element_by_name('userName').send_keys(username)
    driver.find_element_by_name('loginPwdSet').send_keys(password)
    driver.find_element_by_xpath('//input[@alt="ログイン"]').click()

    # 入出金明細
    driver.get('https://www.netbk.co.jp/wpl/NBGate/i020201CT')
    driver.find_element_by_id('CD020202VALUE03').click()
    driver.find_element_by_name('ACT_doShow').click()
    driver.find_element_by_xpath('//a[@href="javascript:submitForm(\'form0202_01_100\')"]').click()


def get_suica_history(driver, jreast_id, password):
    driver.get('https://www.mobilesuica.com/')

    # ログインページ
    driver.find_element_by_name('CommonID').send_keys(jreast_id)
    driver.find_element_by_xpath('//input[@name="Password" and @size=24]').send_keys(password)
    driver.find_element_by_xpath('//input[@src="/img/btn_login_myjr.gif" and @name="MYLOGIN"]').click()

    # 画像認証
    captcha = input('画像に表示されている文字を入力して下さい> ')
    driver.find_element_by_id('MainContent_upImageStringsTextBox').send_keys(captcha)
    driver.find_element_by_id('MainContent_passwordTextBox').send_keys(password)
    driver.find_element_by_id('MainContent_okRadioButton').click()
    driver.find_element_by_id('MainContent_nextButton').click()

    # Suica一覧
    driver.find_element_by_xpath('//input[@alt="次へ"]').click()

    # 会員メニュー
    driver.find_element_by_xpath('//img[@src="/img/btn_riyourireki_off.gif"]').click()

    # 履歴ページ
    Select(driver.find_element_by_name('specifyYearMonth')).select_by_value(
        '%s/%02d' % (last_day.year, last_day.month))
    Select(driver.find_element_by_name('specifyDay')).select_by_value(str(last_day.day))
    driver.find_element_by_id('Submit1').click()
    driver.find_element_by_name('PRINT').click()
    # html = driver.page_source.encode('shift_jis', 'ignore')
    # print(html.decode('shift-jis'))


parser = argparse.ArgumentParser(description='Get bank histories')
parser.add_argument('site', choices=Sites.list())
parser.add_argument('id')
parser.add_argument('password')
parser.add_argument('--branch')
parser.add_argument('--account')
args = parser.parse_args()
driver = webdriver.Chrome(chromedriver_path)
if args.site == Sites.suica:
    get_suica_history(driver, args.id, args.password)
elif args.site == Sites.sbi:
    get_sbi_history(driver, args.id, args.password)
elif args.site == Sites.jpnetbk:
    if args.branch and args.account:
        get_jpnetbk_history(driver, args.id, args.password, args.branch, args.account)
    else:
        print('Enter your branch and account numbers')
elif args.site == Sites.smbc:
    if args.branch and args.account:
        get_smbc_history(driver, args.password, args.branch, args.account)
    else:
        print('Enter your branch and account numbers')
elif args.site == Sites.ufj:
    get_ufj_history(driver, args.id, args.password)
elif args.site == Sites.enavi:
    get_enavi_history(driver, args.id, args.password)
else:
    print('%s is not supported' % args.site)

driver.close()
driver.quit()
