<heading>質疑応答まとめ機能</heading>

pip install -r requirements.txt<br>
で必要なライブラリをインストール<br>

GeminiAPI<br>
API Keyを取得し、.envにペーストする<br>

スプレッドシートAPI<br>
Googleでサービスアカウントを作成
スプレッドシートのアクセスを生成されるサービスアカウントのメールアドレスに与える<br>
service_account.jsonをダウンロードしてディレクトリにコピー<br>

実装<br>
python -m streamlit main.py<br>
でローカルにアクセスできるようになる<br>



分類
要約
優先度順に表示
講義資料参照
回答していないもののみ分類＆要約
（質問の更新ができる）
（コストを最小限にするため、PDFは最初のみ、質問も追加のもののみ）