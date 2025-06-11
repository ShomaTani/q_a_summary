import streamlit as st
import os
from llm import (
    fetch_questions,
    classify_and_summarize,
    load_pdf,
)

st.title("質問分類・要約ダッシュボード")

sheet_url = st.text_input("Google SpreadsheetのURL：")
num = st.number_input("表示するカテゴリーの数：", min_value=1, max_value=100, value=10)

# PDFファイルのアップロード
lecture_pdf = st.file_uploader("講義資料(PDF)をアップロード（推奨）：", type=["pdf"])
if lecture_pdf is not None:
    pdf_file_obj = load_pdf(lecture_pdf)
    st.success("PDFファイルがアップロードされました。")
else:
    pdf_file_obj = None
    st.warning(
        "PDFファイルがアップロードされていません。講義資料をアップロードしてください。"
    )

if st.button("実行"):
    if not sheet_url:
        st.error("URLを入力してください。")
    else:
        try:
            questions = fetch_questions(sheet_url)
            with st.spinner("処理中..."):
                total_rows = len(questions)
                st.success(f"{total_rows}件のデータを取得しました。")
                if pdf_file_obj:
                    response = classify_and_summarize(questions, num, pdf_file_obj)
                else:
                    response = classify_and_summarize(questions, num)
            # レスポンスの表示
            for item in response:
                st.markdown(f"### {item.get('分類', '-')}")
                st.write(f"- 類似質問数: {item.get('類似質問数', '-')}")
                st.write(f"- 講師回答の必要性: {item.get('講師回答の必要性', '-')}")
                st.write(f"- 講義との関連性: {item.get('講義との関連性', '-')}")
                st.write(f"- 一般性: {item.get('一般性', '-')}")
                st.write(f"- **要約**: {item.get('要約', '-')}")

                raw_questions = item.get("分類される質問", "")
                questions_list = [
                    q.strip() for q in raw_questions.split(",") if q.strip()
                ]

                with st.expander("このカテゴリーに分類される質問を表示"):
                    if questions_list:
                        for index, question in enumerate(questions_list, start=1):
                            st.write(f"{index}. {question}")
            # ローカルに保存したPDFファイルを削除
            if os.path.exists("temp_lecture.pdf"):
                os.remove("temp_lecture.pdf")
                st.markdown("---")

        except Exception as e:
            st.error(f"エラーが発生しました {e}")

st.markdown("""
---
<div style="text-align: center; padding: 20px 0;">
    <p> 2024 Powered by Google Gemini API </p>
</div>
""", unsafe_allow_html=True)