import streamlit as st
import os
from llm import fetch_questions, classify_and_summarize, parse_json, build_dataframe, load_pdf

# if "pdf_file_obj" not in st.session_state:
#     st.session_state.pdf_file_obj = None

# if "processed_count" not in st.session_state:
#     st.session_state.processed_count = 0

# if "all_results" not in st.session_state:
#     st.session_state.all_results = []

st.title("質問分類・要約ダッシュボード")

sheet_url = st.text_input("Google SpreadsheetのURLを入力してください：")
num = st.number_input("表示するカテゴリーの数を入力してください：", min_value=1, max_value=100, value=10)
lecture_pdf = st.file_uploader("講義資料(PDF)をアップロードしてください：", type=["pdf"])
if lecture_pdf is not None:
    pdf_file_obj = load_pdf(lecture_pdf)
    st.success("PDFファイルがアップロードされました。")
else:
    pdf_file_obj = None
    st.warning("PDFファイルがアップロードされていません。講義資料をアップロードしてください。")

if st.button("実行"):
    if not sheet_url:
        st.error("URLを入力してください。")
    else:
        try:
            questions = fetch_questions(sheet_url)
            with st.spinner("処理中..."):
                total_rows = len(questions)
                st.success(f"{total_rows}件のデータを取得しました。")
                # st.write(f"総行数： {total_rows}行（前回処理済み：{st.session_state.processed_count}行）")
                # if total_rows <= st.session_state.processed_count:
                #     st.info("新しい質問はありません。")
                # else:
                #     new_records = records[st.session_state.processed_count:total_rows]
                #     st.write(f"新着質問 {len(new_records)}件を処理します。")
                if pdf_file_obj:
                    response = classify_and_summarize(questions, num, pdf_file_obj)
                else:
                    response = classify_and_summarize(questions, num)
                    
            #     df = build_dataframe(response)
            # st.dataframe(df)
            
            for item in response:
                st.markdown(f"### {item.get('分類', '-')}")
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
            
                        
        except Exception as e:
            st.error(f"エラーが発生しました {e}")
        
        

        
