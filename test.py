import streamlit as st
import os
from main import fetch_sheet, classify_and_summarize, parse_json, build_dataframe, load_pdf

st.title("質問分類・要約ダッシュボード")

sheet_url = st.text_input("Google SpreadsheetのURLを入力してください：")
lecture_pdf = st.file_uploader("講義資料（PDF)をアップロードしてください：", type=["pdf"])
num = st.number_input("表示するカテゴリーの数を入力してください：", min_value=1, max_value=100, value=10)
if st.button("実行"):
    if not sheet_url:
        st.error("URLを入力してください。")
    else:
        try:
            records = fetch_sheet(sheet_url)
            with st.spinner("処理中..."):
                st.success(f"{len(records)}件のデータを取得しました。")
                pdf_file_obj = load_pdf(lecture_pdf)
                if pdf_file_obj:
                    response = classify_and_summarize(records, num, pdf_file_obj)
                else:
                    response = classify_and_summarize(records, num)
                    
                df = build_dataframe(response)
            st.dataframe(df)
        except Exception as e:
            st.error(f"エラーが発生しました {e}")
        
        for item in response:
            st.markdown(f"### 分類: {item.get('分類', '-')}")
            st.write(f"- 類似質問数: {item.get('類似質問数', '-')}")
            st.write(f"- 講師回答の必要性: {item.get('講師回答の必要性', '-')}")
            st.write(f"- 講義との関連性: {item.get('講義との関連性', '-')}")
            st.write(f"- 一般性: {item.get('一般性', '-')}")
            st.write(f"- **要約**: {item.get('要約', '-')}")
            
            raw_questions = item.get("分類される質問", "")
            questions_list = [q.strip() for q in raw_questions.split(",") if q.strip()]
            
            with st.expander("このカテゴリーに分類される質問を表示"):
                if questions_list:
                    for index, question in enumerate(questions_list, start=1):
                        st.write(f"{index}. {question}")

        if os.path.exists("temp_lecture.pdf"):
            os.remove("temp_lecture.pdf")
            st.markdown("---")
            
