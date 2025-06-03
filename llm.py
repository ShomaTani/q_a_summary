import gspread
from google.oauth2.service_account import Credentials
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# API キーの読み込み
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(
    filename="service_account.json", scopes=SCOPES
)

gc = gspread.authorize(creds)


def fetch_questions(sheet_url):
    """
    Google Sheetsから質問を取得する関数
    """
    sheet = gc.open_by_url(sheet_url).sheet1
    headers = sheet.row_values(1)
    if not headers:
        return []
    if "質問" not in headers:
        return []
    records = sheet.get_all_records()
    questions = []
    if "回答" in headers:
        for rec in records:
            answer = rec.get("回答")
            if answer is None or str(answer).strip() == "":
                q = rec.get("質問")
                if q is not None:
                    questions.append(str(q).strip())

    else:
        for rec in records:
            q = rec.get("質問")
            if q is not None:
                questions.append(str(q).strip())

    return questions


def strip_text(s: str) -> dict:
    """
    レスポンステキストのフォーマットを整える関数
    """
    text = s.strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    elif text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    return text


def classify_and_summarize(question, num, pdf_file_obj=None):
    """
    質問を分類し、要約、評価するメインの関数
    """
    prompt = f"""
    質問を分類して、類似質問を「○○に関する技術的質問」、「ステップ○○でのバグ報告」、「運用相談」などにまとめ、各分類の質問を講師が答えられる、かつ重要な要素を逃さないように一つの質問に要約して以下の評価基準に則って優先度順に{num}個のみを表示してください。
    講師による解答の必要性と講義との関係性を評価するときは、アップロードされていれば、講義資料のPDFを参考にしてください。
    -類似質問の数
    -LLMではなく講師による回答の必要性
    -講義との関連性
    -ある程度の一般性（個人の機器トラブルなど以外）

    
    質問：{question}
    出力形式はそのままJSONとして読み込めるようにJSONのみで、
    {{
        "分類": "分類名",
        "類似質問数": "数字",
        "講師回答の必要性": "高/中/低",
        "講義との関連性": "高/中/低",
        "一般性": "高/中/低",
        "要約": "要約内容"
        "分類される質問": "質問内容1, 質問内容2, ..."
    }}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, pdf_file_obj] if pdf_file_obj else [prompt],
        config=types.GenerateContentConfig(max_output_tokens=10000, temperature=0.1),
    )
    text = strip_text(response.text)
    print(text)
    return json.loads(text)


def load_pdf(lecture_pdf):
    """
    PDFファイルを一時的にローカルに保存して、アップロードする関数
    """
    pdf_file_obj = None
    if lecture_pdf is not None:
        with open("temp_lecture.pdf", "wb") as f:
            f.write(lecture_pdf.getbuffer())
        pdf_file_obj = client.files.upload(file="temp_lecture.pdf")
    return pdf_file_obj
