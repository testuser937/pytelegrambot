import telebot
import config
import time
import requests
import lxml.html

bot = telebot.TeleBot(config.token)
URL = config.URL


formdata = {
    'inp:Login': '',
    'inp:Password': '',
    'btn:Enter' : 'Enter'
}

@bot.message_handler(commands=['start'])
def bkwork(message):
    if formdata['inp:Login']=='' or formdata['inp:Password']=='':
        bot.send_message(message.chat.id, 'Сначала введите логин/пароль')
    else:
        bot.send_message(message.chat.id, 'Вы начали мониторинг')
        while True:
            session = requests.session()
            r = session.post(URL, data=formdata)

            text = r.text
            doc = lxml.html.document_fromstring(text)
            res = []
            for item in doc.xpath("//td"):
                if not (item.text is None):
                    s = ""
                    for i in item.text:
                        if i not in [' ', '\t', '\n']:
                            s += i
                    res.append((s))

            if "Ждетпроверки" not in res:
                for item in doc.xpath("//td/textarea"):
                    bot.send_message(message.chat.id, item.text)
                return
            else:
                bot.send_message(message.chat.id, 'Пока нету')
            time.sleep(5)



@bot.message_handler(commands=['setlogin'])
def set_login(message):
    sent = bot.send_message(message.chat.id, 'Введите свой логин')
    bot.register_next_step_handler(sent, login)
def login(message):
    if len(message.text) == 6 and message.text.isdigit():
        formdata['inp:Login'] = message.text
        bot.send_message(message.chat.id, 'Логин установлен')
    else:
        bot.send_message(message.chat.id,'Попробуйте еще раз')

@bot.message_handler(commands=['setpassword'])
def set_password(message):
    sent = bot.send_message(message.chat.id, 'Введите свой пароль')
    bot.register_next_step_handler(sent, password)
def password(message):
    if not(message is None):
        formdata['inp:Password'] = message.text
        bot.send_message(message.chat.id, 'Пароль установлен')
    else:
        bot.send_message(message.chat.id, 'Попробуйте еще раз')


if __name__ == '__main__':
    bot.polling(none_stop=True)


