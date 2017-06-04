# 明細自動取得スクリプト

各サービスから先月の利用明細を自動ダウンロードします。
自己責任でご利用下さい。

```
git clone https://github.com/shinichy/get_statement.git
cd get_statement
pip install -r requirements.txt
brew install chromedriver

# get_statement.pyのchromedriver_pathを書き換える
vi get_statement.py

# モバイルSuica (画像認証を入力する必要あり)
python get_statement.py suica <JR EAST ID> <パスワード>

# 住信SBIネット銀行
python get_statement.py sbi <id> <パスワード>

# ジャパンネット銀行
python get_statement.py jpnetbk <ログインID> <パスワード> --branch <店番号> --account <口座番号>

# 三菱東京UFJ銀行
python get_statement.py ufj <契約番号> <パスワード>

# 楽天e-navi
python get_statement.py enavi <ID> <パスワード>
```
