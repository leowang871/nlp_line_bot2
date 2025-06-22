def extract_expense_data(text):
    # 簡易模擬的關鍵字分類與情緒分析
    if any(word in text for word in ["咖啡", "蛋糕", "珍奶", "鹽酥雞", "午餐"]):
        category = "飲食"
    elif any(word in text for word in ["鞋子", "衣服", "逛街", "網購"]):
        category = "購物"
    else:
        category = "其他"

    if any(word in text for word in ["開心", "放鬆", "療癒", "舒服"]):
        emotion = "開心"
    elif any(word in text for word in ["焦慮", "壓力", "煩", "難過"]):
        emotion = "焦慮"
    elif any(word in text for word in ["生氣", "衝動", "爆買"]):
        emotion = "憤怒"
    else:
        emotion = "中性"

    amount = "未知"
    for word in text.split():
        if word.isdigit():
            amount = int(word)

    return {
        "金額": amount,
        "類別": category,
        "情緒": emotion
    }
