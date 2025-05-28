import streamlit as st
import json

# データ読み込み
with open('results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

st.title("質問分類・要約ダッシュボード")

for item in data:
    st.subheader(f"ID {item['id']}: {item['category']}")
    st.write("**原文**: " + item['original'])
    st.write("**要約**: " + item['summary'])
    st.markdown("---")

# enable user to evaluate the results
# upload the pdf file of the lecture powerpoint
# realtime update as more questions come through
# 
