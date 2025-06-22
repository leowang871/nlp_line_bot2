import datetime

def append_to_sheet(text, analysis, user_id):
    # 假設未來串接 gspread 或其他 Google Sheet API
    # 現階段模擬寫入一筆標準化格式資料
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        now,
        user_id,
        text,
        analysis.get("金額", ""),
        analysis.get("類別", ""),
        analysis.get("情緒", "")
    ]
    print("👉 寫入一筆資料：")
    print("| 日期時間 | 使用者ID | 原始輸入 | 金額 | 類別 | 情緒 |")
    print("|----------|-----------|-----------|------|------|------|")
    print("| " + " | ".join(str(cell) for cell in row) + " |")
