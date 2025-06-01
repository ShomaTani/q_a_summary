import streamlit as st

class UI:
    def __init__(self):
        pass
    
st.title("質問分類・要約ダッシュボード")

st.subheader("ID 1: カテゴリA")
st.write("**原文**: これはサンプルの質問です。")
st.write("**要約**: これはサンプルの要約です。")
st.markdown("---")
st.subheader("ID 2: カテゴリB")
st.write("**原文**: これは別のサンプルの質問です。")
st.write("**要約**: これは別のサンプルの要約です。")
st.markdown("---")

if st.button("新しい質問を追加"):
    st.write("新しい質問を追加する機能はまだ実装されていません。")
input = st.chat_input("スプレッドシートのURLを入力してください")
print(input)