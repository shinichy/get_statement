# 履歴自動取得スクリプト

各サービスから先月の利用明細を自動ダウンロードします。
自己責任でご利用下さい。

# セットアップ

ここからChromeDriverをインストール
https://sites.google.com/a/chromium.org/chromedriver/downloads

get_receipt.pyのchromedriver_pathを書き換える


```
git clone https://github.com/shinichy/get_receipt.git
cd get_receipt
pip install -r requirements.txt

# モバイルSuica
python get_receipt.py suica <JR EAST ID> <パスワード>

# 住信SBIネット銀行
python get_receipt.py sbi <id> <パスワード>

# ジャパンネット銀行
python get_receipt.py jpnetbk <ログインID> <パスワード> --branch <店番号> --account <口座番号>

# 三菱東京UFJ銀行
python get_receipt.py ufj <契約番号> <パスワード>

# 楽天e-navi
python get_receipt.py enavi <ID> <パスワード>
```
