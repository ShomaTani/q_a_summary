import streamlit as st
from main import fetch_sheet, classify_and_summarize, parse_json, build_dataframe


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
                raw = rec.get("質問")
                response = classify_and_summarize(raw)
                parsed = parse_json(response)
                parsed["original"] = raw
                results.append(parsed)
            df = build_dataframe(results)
            st.dataframe(df)

        except Exception as e:
            st.error(f"エラーが発生しました {e}")
