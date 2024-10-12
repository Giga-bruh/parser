import YA_SKAZAL_NE_LEZ_SOHRET
import telebot
import json

from selenium import webdriver
from selenium.webdriver.common.by import By

bot=telebot.TeleBot(YA_SKAZAL_NE_LEZ_SOHRET.token)

v=[]
@bot.message_handler(["start"])
def handle_start(message):
    bot.send_message(message.chat.id,"привет прежде чем начать пользоваться нашим ботом прошу написать команду /help чтобы вы знали на что способне наш бот")
@bot.message_handler(["help"])
def handle_start(message):
    bot.send_message(message.chat.id,"у нас есть команды:\n /articles - она выводит вам 10 статей без использования определенных потоков \n /articles_by_flow - позволяет вам выбрать при каком потоке будут выбираться первые 10 статей \n /complaint - позволяет вам написать жалобу на работу бота, сюда также можно написать чего в нем не хватает \n также наш бот может ответить на вопросы например что такое поток (пока что только на этот)")
@bot.message_handler(["articles"])
def handle_articles(message):
    text=message.text
    a=text.split(" ")
    if len(a)!=1:
        bot.send_message(message.chat.id,"нижние подчеркивание при вводе разных команд обязателен!(либо вы просто написали лишние символы в команду прошу ознакомиться с командами с помощью /help)")
    else:
        chrome = webdriver.Chrome()
        chrome.get("https://habr.com/ru/articles/")
        m=""
        k=chrome.find_elements(By.CLASS_NAME,"tm-title_h2")
        h=0
        for i in k:





            if h<10:
                l = i.find_element(By.TAG_NAME, "a")
                n = l.get_attribute("href")
                m+=f"{i.text} \n {n} \n"
            h+=1

        bot.send_message(message.chat.id,f"{m}")

@bot.message_handler(["articles_by_flow"])




def handle_articles(message):

    bot.send_message(message.chat.id,"какой поток вы хотите выбрать?",reply_markup=sozdanie_knopok_top_ili_net())



@bot.message_handler(["complaint"])
def handle_articles(message):
    bot.send_message(message.chat.id,"какая у вас жалоба?")
    bot.register_next_step_handler_by_chat_id(message.chat.id,zhaloba)
def a(message):
    return True
@bot.callback_query_handler(func=a)
def obrabotka_knopok(klick):

    spisok = klick.data.split("_")


    if spisok[0]=="rated":

        bot.edit_message_text(chat_id=klick.message.chat.id, message_id=klick.message.message_id,
                              text="какой порог рейтинга у статей должен быть?",
                              reply_markup=sozdanie_knopok_za_rated())

        v.append(f"{spisok[0]}")
    elif spisok[0] == "top":

        bot.edit_message_text(chat_id=klick.message.chat.id, message_id=klick.message.message_id,
                              text="за какое время вы хотите увидеть?",
                              reply_markup=sozdanie_knopok_za_vrema())
        v.append(f"{spisok[0]}")
    elif spisok[1] == "a":

        bot.edit_message_text(chat_id=klick.message.chat.id, message_id=klick.message.message_id,
                              text="какой уровень сложности вы хотите?",
                              reply_markup=sozdanie_knopok_slozhnost())
        v.append(f"/{spisok[0]}/")
    elif spisok[1]=="b":
        if spisok[0]!="":

            v.append(f"{spisok[0]}/")
        print(v)

        bot.edit_message_text(chat_id=klick.message.chat.id, message_id=klick.message.message_id,
                              text="ваш поток успешно определен ищу для вас статьи"
                              )
        potok(v,klick.message)
        for i in v:

            v.remove(i)
        if len(v)==1:
            v.pop(-1)
    elif spisok[1]=="h":

        bot.edit_message_text(chat_id=klick.message.chat.id, message_id=klick.message.message_id,
                              text="какой уровень сложности вы хотите?",
                              reply_markup=sozdanie_knopok_slozhnost())
        if spisok[0]!="":
            v.append(f"{spisok[0]}/")
        else:
            v.remove("rated")


def a(message):
    return True

@bot.message_handler(func=a)
def handle_soobshenie(message):
            if message.text == "что такое поток?":
                bot.send_message(message.chat.id,
                                 "поток это выбор статей по определенным признакам, например рейтинг сложность насколько новые и т.д")


            else:
                bot.send_message(message.chat.id,
                                 "либо вы задали вопрос на который я не могу ответить либо написали неправильно команду прошу ознакомиться с командой /help")


def zhaloba(message):
    text=message.text
    slovar={"id":message.chat.id,"zhaloba":str(text)}
    fail = open("file.json", "r", encoding="UTF-8")
    slovari = json.load(fail)
    appointmens = slovari["clients"]
    appointmens.append(slovar)

    fail.close()
    fail = open("file.json", "w", encoding="UTF-8")
    json.dump(slovari, fail, ensure_ascii=False, indent=4)
    fail.close()
def sozdanie_knopok_top_ili_net():
    spisok_knopok = telebot.types.InlineKeyboardMarkup()
    minys = telebot.types.InlineKeyboardButton("новые",
                                               callback_data="rated")
    plys = telebot.types.InlineKeyboardButton("лучшие",
                                              callback_data="top")
    spisok_knopok.add(minys,plys)

    return spisok_knopok
def sozdanie_knopok_za_vrema():
    spisok_knopok = telebot.types.InlineKeyboardMarkup()
    day = telebot.types.InlineKeyboardButton("за день",
                                               callback_data="daily_a")
    weekend = telebot.types.InlineKeyboardButton("за неделю",
                                              callback_data="weekly_a")
    month = telebot.types.InlineKeyboardButton("за месяц",
                                               callback_data="monthly_a")
    year = telebot.types.InlineKeyboardButton("за год",
                                              callback_data="yearly_a")
    alltime = telebot.types.InlineKeyboardButton("все время",
                                              callback_data="alltime_a")
    v = []
    spisok_knopok.add(day,weekend,month,year,alltime)
    return spisok_knopok
def sozdanie_knopok_za_rated():
    spisok_knopok = telebot.types.InlineKeyboardMarkup()
    c = telebot.types.InlineKeyboardButton("все",
                                             callback_data="_h")
    day = telebot.types.InlineKeyboardButton("больше 0",
                                               callback_data="0_h")
    weekend = telebot.types.InlineKeyboardButton("больше 10",
                                              callback_data="10_h"
                                                            )
    month = telebot.types.InlineKeyboardButton("больше 25",
                                               callback_data="25_h")
    year = telebot.types.InlineKeyboardButton("больше 50",
                                              callback_data="50_h")
    alltime = telebot.types.InlineKeyboardButton("больше 100",
                                              callback_data="100_h")
    v = []
    spisok_knopok.add(c,day,weekend,month,year,alltime)
    return spisok_knopok
def sozdanie_knopok_slozhnost():
    spisok_knopok = telebot.types.InlineKeyboardMarkup()
    day = telebot.types.InlineKeyboardButton("все",
                                               callback_data="_b")
    weekend = telebot.types.InlineKeyboardButton("легко",
                                              callback_data="easy_b")
    month = telebot.types.InlineKeyboardButton("средне",
                                               callback_data="medium_b")
    year = telebot.types.InlineKeyboardButton("сложно",
                                              callback_data="hard_b")
    v=[]
    spisok_knopok.add(day,weekend,month,year)
    return spisok_knopok
def potok(v,message):
    m=""
    for i in v:
        m+=i
    print(m)
    chrome = webdriver.Chrome()
    chrome.get(f"https://habr.com/ru/articles/{m}")
    m = ""
    k = chrome.find_elements(By.CLASS_NAME, "tm-title_h2")
    h = 0
    for i in k:

        if h < 10:
            l = i.find_element(By.TAG_NAME, "a")
            n = l.get_attribute("href")
            m += f"{i.text} \n {n} \n"
        h += 1

    bot.send_message(message.chat.id, f"{m}")


bot.polling()
