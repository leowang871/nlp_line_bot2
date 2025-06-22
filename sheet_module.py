import datetime
import os
import json
import base64
import gspread
from google.oauth2.service_account import Credentials

def append_to_sheet(text, analysis, user_id):
    # 解析 base64 JSON 憑證
    creds_json = base64.b64decode(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")).decode()
    creds_dict = json.loads(creds_json)

    # 建立授權憑證
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    # 連接 Google Sheet
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID"))
    worksheet = sheet.worksheet(os.getenv("SHEET_TAB_NAME", "Sheet1"))

    # 組合資料列
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        now,
        user_id,
        text,
        analysis.get("金額", ""),
        analysis.get("類別", ""),
        analysis.get("情緒", "")
    ]

    # 寫入資料
    worksheet.append_row(row, value_input_option="USER_ENTERED")
    print("✅ 寫入 Google Sheet 成功：", row)
