#!/usr/bin/python
# coding=utf-8

# Get receipts last month

import argparse
from datetime import datetime, date, timedelta

from selenium import webdriver
from selenium.webdriver.support.ui import Select

chromedriver_path = '/usr/local/bin/chromedriver'


class Sites:
    suica = 'suica'
    sbi = 'sbi'

    @staticmethod
    def list():
        return [Sites.suica, Sites.sbi]


def get_sbi_history(driver, username, password):
    # ログイン
    driver.get('https://www.netbk.co.jp/wpl/NBGate')
    driver.find_element_by_name('userName').send_keys(username)
    driver.find_element_by_name('loginPwdSet').send_keys(password)
    driver.find_element_by_xpath('//input[@src="https://contents-cache.netbk.co.jp/pc/img_cmn/b_login_01.gif"]').click()

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
    string = input()
    driver.find_element_by_id('MainContent_upImageStringsTextBox').send_keys(string)
    driver.find_element_by_id('MainContent_passwordTextBox').send_keys(password)
    driver.find_element_by_id('MainContent_okRadioButton').click()
    driver.find_element_by_id('MainContent_nextButton').click()

    # 会員メニュー
    driver.find_element_by_xpath('//img[@src="/img/btn_riyourireki_off.gif"]').click()

    # 履歴ページ
    today = date.today()
    last_day = datetime(today.year, today.month, 1) - timedelta(days=1)
    Select(driver.find_element_by_name('specifyYearMonth')).select_by_value(
        '%s/%s' % (last_day.year, last_day.month))
    Select(driver.find_element_by_name('specifyDay')).select_by_value(str(last_day.day))
    driver.find_element_by_id('Submit1').click()
    driver.find_element_by_name('PRINT').click()
    # html = driver.page_source.encode('shift_jis', 'ignore')
    # print(html.decode('shift-jis'))


parser = argparse.ArgumentParser(description='Get bank histories')
parser.add_argument('site', choices=Sites.list())
parser.add_argument('id')
parser.add_argument('password')
args = parser.parse_args()
driver = webdriver.Chrome(chromedriver_path)
if args.site == Sites.suica:
    get_suica_history(driver, args.id, args.password)
elif args.site == Sites.sbi:
    get_sbi_history(driver, args.id, args.password)
else:
    print('%s is not supported' % args.site)
driver.close()

