import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import telebot
from kora_database import *
from fastapi import FastAPI

app = FastAPI()
# إعداد البوت
bot_token = '1981790629:AAGXe9sBFiWWhzsUaeK-8ie7AhgRnYtKV_E'
chat_id = '@test829435'  
bot = telebot.TeleBot(bot_token)

def send_message(msg):
    bot.send_message(chat_id, msg)

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_request(match_type):
    today = datetime.now().strftime("%m/%d/%Y")
    url = f"https://www.yallakora.com/match-center/مركز-المباريات?date={today}#days"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    match_cards = soup.find_all("div", class_=lambda c: c and "matchCard" in c)
    matches_divs=[]
    for card in match_cards:
        title_tag = card.find("div", class_="title")
        league_name = title_tag.h2.get_text(strip=True) if title_tag and title_tag.h2 else ""
        excluded_keywords = ['كرة السلة', 'سيدات', 'لكرة اليد']
        if any(keyword in league_name for keyword in excluded_keywords):
            pass

        else:
            matches_divs += card.find_all("div", class_=f"item {match_type} liItem")
    return matches_divs


def extract_match_data(match_div):
    team_a = match_div.find('div', class_='teams teamA').find('p').text.strip()
    team_b = match_div.find('div', class_='teams teamB').find('p').text.strip()
    match_status = match_div.find('div', class_='matchStatus').find('span').text.strip()
    scores = match_div.find('div', class_='MResult').find_all('span', class_='score')
    score_a = scores[0].text.strip()
    score_b = scores[1].text.strip()
    match_time = match_div.find('div', class_='MResult').find('span', class_='time').text.strip()
    print(team_a, team_b, score_a, score_b, match_time, match_status)
    return team_a, team_b, score_a, score_b, match_time, match_status


def format_match_info(team_a, team_b, score_a, score_b, match_time):
    print(f"{team_a} Vs {team_b}\n🕓 الوقت: {match_time}\n📊 النتيجة: {score_a} - {score_b}")
    return f"{team_a} Vs {team_b}\n🕓 الوقت: {match_time}\n📊 النتيجة: {score_a} - {score_b}"


def send_today_matches():
    try:
        delete_all_data()
    except:pass
    send_message("📅 جدول مباريات اليوم:")
    match_divs = get_request('future')
    for match_div in match_divs:
        team_a, team_b, score_a, score_b, match_time, status = extract_match_data(match_div)
        match_key = f"{team_a},{team_b}"  # إنشاء مفتاح فريد للمباراة
        addData(match_key, team_a, team_b, score_a, score_b, status, match_time)  # حفظ المباراة في قاعدة البيانات
        msg = format_match_info(team_a, team_b, score_a, score_b, match_time)
        send_message(msg)
        time.sleep(1)

def monitor_matches():
    match_divs = get_request('now')
    for match_div in match_divs:
        team_a, team_b, score_a, score_b, match_time, status = extract_match_data(match_div)
        match_key = f"{team_a},{team_b}"
        data = getData(match_key)

        if data:
            old_score_a = int(data[3])  # النتيجة القديمة لفريق A
            old_score_b = int(data[4])  # النتيجة القديمة لفريق B
            old_status = data[5]  # حالة المباراة

            # إشعار ببداية المباراة إذا كانت الحالة تغيرت
            if old_status != status and status in ['انطلقت', 'جارية']:
                send_message(f"🚨 بدأت المباراة!\n{team_a} 🆚 {team_b}")

            # مقارنة الأهداف
            if int(score_a) != old_score_a or int(score_b) != old_score_b:
                # تم تسجيل هدف جديد، إرسال إشعار
                if int(score_a) > old_score_a:
                    send_message(f"🎯 جوووول! {team_a} يسجل هدفًا!")
                if int(score_b) > old_score_b:
                    send_message(f"🎯 جوووول! {team_b} يسجل هدفًا!")

                # إرسال النتيجة المحدثة
                send_message(format_match_info(team_a, team_b, score_a, score_b, match_time))

                # تحديث البيانات في قاعدة البيانات
                updateData(score_a, score_b, status, match_key)

        else:
            # إذا كانت المباراة جديدة في قاعدة البيانات
            addData(match_key, team_a, team_b, score_a, score_b, status, match_time)


# دالة لتحقق من الوقت الساعة 8 صباحًا وإرسال المباريات
def check_and_send_matches():
    current_time = datetime.now()
    if current_time.hour == 23 and current_time.minute == 30:  
        send_today_matches()
        time.sleep(60)


@app.get("/")
def root():
    return {"message": "Service is running!"}

@app.get("/start")
def start_bot():
    check_and_send_matches()
    monitor_matches()
        
    return {"status": "✅ matches checked and sent"}
