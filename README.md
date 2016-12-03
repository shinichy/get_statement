# 履歴自動取得スクリプト

自己責任でご利用下さい。

ここからChromeDriverをインストール
https://sites.google.com/a/chromium.org/chromedriver/downloads

get_receipts.pyのchromedriver_pathを書き換える


```
https://github.com/shinichy/get_receipts.git
pip install -r requirements.txt

# Mobile Suica
python get_receipts.py suica <JR EAST ID> <password>

# 住信SBI
python get_receipts.py sbi <id> <password>
```
