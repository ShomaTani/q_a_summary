import streamlit as st
from main import fetch_sheet


class UI:
    def __init__(self):
        pass


st.title("質問分類・要約ダッシュボード")

sheet_url = st.text_input("Google SpreadsheetのURLを入力してください：")
if st.button("実行"):
    if not sheet_url:
        st.error("URLを入力してください。")
    else:
        try:
            records = fetch_sheet(sheet_url)
            st.success(f"{len(records)}件のデータを取得しました。")
            results = []

            for rec in records[:5]:
                pass
        except Exception as e:
            st.error(f"エラーが発生しました {e}")
