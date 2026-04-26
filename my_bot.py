import os
import requests
import time
import random

TOKEN = os.environ.get("TOKEN")

URL = f"https://api.telegram.org/bot{TOKEN}/"

last_update_id = None

# 📚 المعلومات حسب الأقسام
facts = {
    "📿 دين": [
        "📿 أول من بنى الكعبة هو سيدنا إبراهيم عليه السلام",
        "🕌 الصلاة عماد الدين",
        "📖 القرآن الكريم نزل على النبي محمد ﷺ"
    ],
    "🚀 فضاء": [
        "🚀 الشمس نجم وليس كوكب",
        "🌙 القمر يعكس ضوء الشمس",
        "🪐 زحل لديه حلقات مميزة"
    ],
    "🔬 علوم": [
        "🔬 الماء يتكون من الهيدروجين والأكسجين",
        "🧠 الدماغ يتحكم في جميع وظائف الجسم",
        "⚡ الكهرباء هي تدفق الإلكترونات"
    ],
    "⚽ رياضة": [
        "⚽ كرة القدم هي الرياضة الأكثر شعبية في العالم",
        "🏆 كأس العالم أقيم أول مرة عام 1930",
        "🇦🇷 ميسي فاز بكأس العالم 2022 مع الأرجنتين"
    ]
}

stats_counter = {}

def get_keyboard():
    return {
        "keyboard": [
            [{"text": "📿 دين"}, {"text": "🚀 فضاء"}, {"text": "🔬 علوم"}],
            [{"text": "⚽ رياضة"}, {"text": "🎲 عشوائي"}, {"text": "📊 إحصائيات"}],
            [{"text": "ℹ️ معلومات البوت"}]
        ],
        "resize_keyboard": True
    }

def send_message(chat_id, text):
    url = URL + "sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": get_keyboard()
    }
    try:
        requests.post(url, json=data, timeout=10)
    except Exception as e:
        print(f"خطأ: {e}")

def show_stats(chat_id):
    global stats_counter
    if not stats_counter:
        send_message(chat_id, "📊 لا توجد إحصائيات بعد")
    else:
        sorted_stats = sorted(stats_counter.items(), key=lambda x: x[1], reverse=True)
        text = "📊 الأكثر طلباً:\n\n"
        for i, (cat, count) in enumerate(sorted_stats[:3], 1):
            text += f"{i}. {cat}: {count} مرة\n"
        send_message(chat_id, text)

def show_bot_info(chat_id):
    info = """🤖 معلومات البوت

📚 بوت معلومات ثقافي رياضي
⭐ يحتوي على 4 أقسام

من تطوير رضـوان
انستقرام: @rad_ben.99

🎯 الأوامر:
• اختر قسماً من الأزرار
• 🎲 عشوائي
• 📊 إحصائيات

📅 إصدار 0.9"""
    send_message(chat_id, info)

def get_updates():
    global last_update_id
    url = URL + "getUpdates"
    params = {"timeout": 100, "offset": last_update_id}
    try:
        response = requests.get(url, params=params, timeout=110)
        return response.json()
    except Exception as e:
        print(f"خطأ: {e}")
        return {"result": []}

while True:
    updates = get_updates()
    
    if "result" in updates:
        for update in updates["result"]:
            if last_update_id is None or update["update_id"] > last_update_id:
                last_update_id = update["update_id"]
            
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")
                    
                    try:
                        if text == "/start":
                            send_message(chat_id, "✨ مرحباً! اختر قسم 👇")
                        
                        elif text == "🎲 عشوائي":
                            cat = random.choice(list(facts.keys()))
                            fact = random.choice(facts[cat])
                            stats_counter[cat] = stats_counter.get(cat, 0) + 1
                            send_message(chat_id, f"🎲 {cat}:\n\n{fact}")
                        
                        elif text == "📊 إحصائيات":
                            show_stats(chat_id)
                        
                        elif text == "ℹ️ معلومات البوت":
                            show_bot_info(chat_id)
                        
                        elif text in facts:
                            fact = random.choice(facts[text])
                            stats_counter[text] = stats_counter.get(text, 0) + 1
                            send_message(chat_id, f"📚 {text}\n\n{fact}")
                        
                        else:
                            send_message(chat_id, "❌ اختر من الأزرار")
                    
                    except Exception as e:
                        print(f"خطأ: {e}")
    
    time.sleep(1)
