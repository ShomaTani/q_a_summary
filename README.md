q_a_summary

pip install -r requirements.txt
で必要なライブラリをインストール

GeminiAPI
API Keyを取得し、.envにペーストする

スプレッドシートAPI
Googleでサービスアカウントを作成
スプレッドシートのアクセスを生成されるサービスアカウントのメールアドレスに与える
service_account.jsonをダウンロードしてディレクトリにコピー

実装
python -m streamlit main.py
でローカルにアクセスできるようになる



分類
要約
優先度順に表示
講義資料参照
回答していないもののみ分類＆要約
（質問の更新ができる）
（コストを最小限にするため、PDFは最初のみ、質問も追加のもののみ）