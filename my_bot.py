import os
import requests
import time
import random
import sqlite3
from datetime import datetime

TOKEN = os.environ.get("TOKEN")

URL = f"https://api.telegram.org/bot{TOKEN}/"

last_update_id = None

# 📚 المعلومات حسب الأقسام
facts = {
    "📿 دين": [
        "📿 أول من بنى الكعبة هو سيدنا إبراهيم عليه السلام",
        "🕌 الصلاة عماد الدين",
        "📖 القرآن الكريم نزل على النبي محمد ﷺ",
        "🤲 من صام رمضان إيماناً واحتساباً غفر له ما تقدم من ذنبه",
        "🕋 الحج المبرور ليس له جزاء إلا الجنة"
    ],
    "🚀 فضاء": [
        "🚀 الشمس نجم وليس كوكب",
        "🌙 القمر يعكس ضوء الشمس",
        "🪐 زحل لديه حلقات مميزة",
        "🌍 الأرض تدور حول الشمس في 365 يوم",
        "⭐ النجوم تنتج الضوء والحرارة من الاندماج النووي"
    ],
    "🔬 علوم": [
        "🔬 الماء يتكون من الهيدروجين والأكسجين",
        "🧠 الدماغ يتحكم في جميع وظائف الجسم",
        "⚡ الكهرباء هي تدفق الإلكترونات",
        "🌿 النباتات تصنع غذائها بالبناء الضوئي",
        "🦴 الهيكل العظمي يتكون من 206 عظمة"
    ],
    "⚛️ فيزياء": [
        "⚛️ الجاذبية تجذب الأجسام نحو الأرض",
        "💡 الضوء يسير بسرعة 300 ألف كم/ث",
        "🧲 المغناطيس يجذب الحديد",
        "🔊 الصوت يحتاج إلى وسط لينتقل",
        "📏 الطاقة لا تفنى ولا تستحدث من العدم"
    ],
    "🧪 كيمياء": [
        "🧪 الذهب عنصر كيميائي",
        "🔥 الاحتراق تفاعل كيميائي",
        "💧 الماء مركب وليس عنصر",
        "🧂 ملح الطعام هو كلوريد الصوديوم",
        "🎈 غاز الهيليوم أخف من الهواء"
    ],
    "🌍 جغرافيا": [
        "🌍 أفريقيا أكبر قارة من حيث عدد الدول",
        "🏜️ الصحراء الكبرى أكبر صحراء حارة",
        "🌊 المحيط الهادئ أكبر محيط",
        "🗻 جبل إفرست أعلى قمة في العالم",
        "🏝️ أستراليا أصغر قارة"
    ],
    "💻 تكنولوجيا": [
        "💻 الإنترنت شبكة عالمية",
        "📱 الهواتف الذكية هي حواسيب صغيرة",
        "🤖 الذكاء الاصطناعي يتطور بسرعة",
        "🔒 التشفير يحمي بياناتك",
        "☁️ الحوسبة السحابية تخزن بياناتك عن بُعد"
    ],
    "🏛️ تاريخ": [
        "🏛️ الأهرامات بنيت منذ 4500 سنة",
        "⚔️ الحرب العالمية الثانية انتهت 1945",
        "📜 أول اختراع للكتابة كان في بلاد الرافدين"
    ],
    "🐧 حيوانات": [
        "🐧 طائر البطريق لا يستطيع الطيران",
        "🐘 الفيل أكبر حيوان بري",
        "🦒 الزرافة أطول حيوان بري"
    ]
}

# إحصائيات الاستخدام
stats_counter = {}

# 🔘 لوحة الأزرار
def get_keyboard():
    return {
        "keyboard": [
            [{"text": "📿 دين"}, {"text": "🚀 فضاء"}, {"text": "🔬 علوم"}],
            [{"text": "⚛️ فيزياء"}, {"text": "🧪 كيمياء"}, {"text": "🌍 جغرافيا"}],
            [{"text": "💻 تكنولوجيا"}, {"text": "🏛️ تاريخ"}, {"text": "🐧 حيوانات"}],
            [{"text": "🎲 عشوائي"}, {"text": "📊 إحصائيات"}, {"text": "ℹ️ معلومات البوت"}]
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
        print(f"خطأ في الإرسال: {e}")

def show_stats(chat_id):
    global stats_counter
    if not stats_counter:
        send_message(chat_id, "📊 لا توجد إحصائيات بعد، استخدم البوت أولاً")
    else:
        sorted_stats = sorted(stats_counter.items(), key=lambda x: x[1], reverse=True)
        text = "📊 **أكثر الأقسام طلباً:**\n\n"
        for i, (cat, count) in enumerate(sorted_stats[:3], 1):
            text += f"{i}. {cat}: {count} مرة\n"
        send_message(chat_id, text)

def show_bot_info(chat_id):
    info = """🤖 **معلومات البوت**

📚 بوت معلومات ثقافي وتعليمي
⭐ يحتوي على 9 أقسام متنوعة

🎯 **الأوامر المتاحة:**
• اختر قسماً من الأزرار
• 🎲 عشوائي: معلومة عشوائية
• 📊 إحصائيات: الأقسام الأكثر طلباً

📅 تم التحديث: إصدار متطور"""
    send_message(chat_id, info)

def get_updates():
    global last_update_id
    url = URL + "getUpdates"
    params = {"timeout": 100, "offset": last_update_id}
    try:
        response = requests.get(url, params=params, timeout=110)
        return response.json()
    except Exception as e:
        print(f"خطأ في جلب التحديثات: {e}")
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
                            welcome = "✨ مرحباً بك في بوت المعلومات المتطور!\n\nاختر قسم من الأزرار 👇\n\n🎲 زر عشوائي: يعطيك معلومة من أي قسم\n📊 إحصائيات: يعرض الأقسام الأكثر طلباً"
                            send_message(chat_id, welcome)
                        
                        elif text == "🎲 عشوائي":
                            random_category = random.choice(list(facts.keys()))
                            fact = random.choice(facts[random_category])
                            stats_counter[random_category] = stats_counter.get(random_category, 0) + 1
                            send_message(chat_id, f"🎲 من قسم {random_category}:\n\n{fact}")
                        
                        elif text == "📊 إحصائيات":
                            show_stats(chat_id)
                        
                        elif text == "ℹ️ معلومات البوت":
                            show_bot_info(chat_id)
                        
                        elif text in facts:
                            fact = random.choice(facts[text])
                            stats_counter[text] = stats_counter.get(text, 0) + 1
                            send_message(chat_id, f"📚 **{text}**\n\n{fact}")
                        
                        else:
                            send_message(chat_id, "❌ اختر قسم من الأزرار 👇")
                    
                    except Exception as e:
                        print(f"خطأ في معالجة الرسالة: {e}")
                        send_message(chat_id, "⚠️ حدث خطأ، حاول مرة أخرى")
    
    time.sleep(1)
