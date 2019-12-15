import telegram
#import pandas as pd
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters, ConversationHandler
from ruamel.yaml import YAML

'''
from chatterbot import ChatBotpip3
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.response_selection import get_most_frequent_response
from fuzzywuzzy.process import extractOne
from haversine import haversine
import traceback
'''

import os
import server

if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')


'''
chatbot = ChatBot("RareHacks", response_selection_method = get_most_frequent_response)
db = pd.read_csv("data/keywords.csv")
db.columns = ['keyword','general answer','diffuse leptomeningeal melanocytosis',
    'familial melanoma','uveal melanoma']
places = pd.read_csv('data/places.csv')
places.columns = ['keyword','diffuse leptomeningeal melanocytosis',
    'familial melanoma','uveal melanoma']
'''

locations = {"GERMANY":         (50, 10),
             "BELGIUM":         (50, 4),
             "AUSTRIA":         (47, 14),
             "SPAIN":           (41.5, 2),
             "CANADA":          (58, -106),
             "ESTONIA":         (58, 26),
             "FRANCE":          (46, 3),
             "ITALY":           (41, 13),
             "HUNGARY":         (47, 19),
             "ISRAEL":          (31, 34),
             "JAPAN":           (36, 138),
             "THE NETHERLANDS": (52, 6),
             "POLAND":          (52, 19),
             "PORTUGAL":        (39, -8),
             "UNITED KINGDOM":  (53, -1),
             "SWITZERLAND":     (62, 15),
             "TURKEY":          (39, 35),
             "LETONIA":         (56, 25)}

PATH_TO_TRANSLATION_FILE = "language/translations.yml"

'''
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
trainer.train("chatterbot.corpus.english.greetings")
trainer.train("chatterbot.corpus.english.conversations")
trainer.train("data/preguntasrespuestas.yml")
trainer.train("data/preguntasrespuestas.yml")
'''

NAME, AGE, GENDER, LOCATION, SAVE_USER = range(5)

translator = {}
codigoLenguaje = "en"
userId = -1

def translate(tag):
    translatedTag = translator.get(codigoLenguaje).get(tag)
    if(translatedTag):
        return translatedTag
    return tag
    

def log_in_out(f):
    def g(*args, **kwargs):
        print(f.__name__)
        ret = f(*args,**kwargs)
        print(ret)
        return ret
    return g


@log_in_out
def start(bot, update):
    try:
        global codigoLenguaje
        codigoLenguaje = update.effective_user.language_code
        global userId
        userId = update.effective_user.id

        supportedLanguages = translator.get("supportedLanguages").split(",")
        if(not codigoLenguaje in supportedLanguages):
            codigoLenguaje = "en"
            bot.send_message(chat_id=update.message.chat_id, text=translate("languageNotSupported"))
        bot.send_message(chat_id=update.message.chat_id, text=translate("initialGreetings"))
        bot.send_message(chat_id=update.message.chat_id, text=translate("askForName"))
        return NAME
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))

    '''
    try:

        markUp = telegram.InlineKeyboardMarkup([[help_button]])

        chat_id = update.message.from_user.id
        bot.send_message(
            chat_id=chat_id,
            text='Hello ...',
            reply_markup=markUp,
        )
        bot.send_message(chat_id=update.message.chat_id, text=translate("saludoInicial"))
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))
        '''


def name(bot, update, user_data):
    try:
        name = update.message.text
        user_data["name"] = name
        bot.send_message(chat_id=update.message.chat_id, text=translate("askForAge"))
        return AGE
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))

@log_in_out
def age(bot, update, user_data):
    try:
        age = update.message.text
        user_data["age"] = age
        
        kb = [
            [telegram.KeyboardButton("1. " + translate("Others"))],
            [telegram.KeyboardButton("2. " + translate("Woman"))],
            [telegram.KeyboardButton("3. " + translate("Man"))]
        ]
        kb_markup = telegram.ReplyKeyboardMarkup(kb)
        bot.send_message(chat_id=update.message.chat_id, text=translate("askForGender"), reply_markup=kb_markup)

        return GENDER
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))

@log_in_out
def gender(bot, update, user_data):
    try:
        answer = update.message.text
        if(answer.startswith("3.")):
            gender = "Man"
        elif(answer.startswith("2.")):
            gender = "Woman"
        else:
            gender = "Others"
        user_data["gender"] = gender

        kb = [[telegram.KeyboardButton("1. "+translate("yes"), request_location=True)], [telegram.KeyboardButton("2. "+translate("no"))]]
        kb_markup = telegram.ReplyKeyboardMarkup(kb)
        bot.send_message(chat_id=update.message.chat_id, text=translate("askForLocation"), reply_markup=kb_markup)
        return LOCATION
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))

@log_in_out
def location(bot, update, user_data):
    try:
        if(update.message.location):
            user_data['longitude'] = update.message.location.latitude
            user_data['latitude'] = update.message.location.longitude


        kb = [[telegram.KeyboardButton("1. "+translate("yes"))], [telegram.KeyboardButton("2. "+translate("no"))]]
        kb_markup = telegram.ReplyKeyboardMarkup(kb)
        bot.send_message(chat_id=update.message.chat_id, text=translate("askForSaveUser"), reply_markup=kb_markup)
        return SAVE_USER
        
        '''
        lat, lon = update.message.location.latitude, update.message.location.longitude
        user_data['location'] = (lat, lon)
        message = db[db['keyword'] == 'Hello'][user_data["melanoma"]].values[0]
        message = reduce(apply_replace, [("{NOM}", lambda x: user_data['name']),], message)
        bot.send_message(chat_id=update.message.chat_id, text=message)
        bot.send_message(chat_id=update.message.chat_id, text="Otherwise, tell me how can I help you")
        '''

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))

    return ConversationHandler.END

@log_in_out
def saveUser(bot, update, user_data):
    try:
        answer = update.message.text
        if(answer.startswith("1.")):
            #crear Usuario con los datos de user_data, si existe ya updatearlo (la logica de si insert o update la pondria en el archivo server)
            server.create(userID, user_data.get("name"), user_data.get("age"), user_data.get("sex"), user_data.get("latitude"), user_data.get("longitude"))
            bot.send_message(chat_id=update.message.chat_id, text=translate("userSaved"))
        return SAVE_USER

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))

    return ConversationHandler.END


@log_in_out
def cancel(bot, update):
    print("me llega cancel")
    bot.send_message(chat_id=update.message.chat_id, 
                     text="Funcion cancel")

    return ConversationHandler.END

from functools import reduce

@log_in_out
def answers(bot, update, user_data, _early_response=[None]):
    print("me llega ansers")
    bot.send_message(chat_id=update.message.chat_id, text="Funcion answer")
    '''
    try

        if response.confidence < 0.1:
            bot.send_message(chat_id=update.message.chat_id, text="Sorry 🤔, I couldn't understand your question")
            return 

        def apply_replace(string, pair):
            token, f = pair
            return string.replace(token, f(user_data))
    
        keyword = response.text.split("/")[0]

        if keyword == "Centers":
            nearest_location_name = min(locations.keys(), key=lambda x: haversine(locations[x], user_data['location']))
            query = places[places['keyword'] == nearest_location_name]
            info = query[user_data["melanoma"]].values[0]
            info = reduce(apply_replace, [("{NOM}", lambda x: user_data['name']),], info)
            message = "{}:{}.".format(info.split(':')[0], ', '.join(info.split(':')[1].split(', ')[:5]))
            bot.send_message(chat_id=update.message.chat_id, text=message)
        elif keyword == 'more' and 'Centers' in _early_response:
            nearest_location_name = min(locations.keys(), key=lambda x: haversine(locations[x], user_data['location']))
            query = places[places['keyword'] == nearest_location_name]
            info = query[user_data["melanoma"]].values[0]
            info = reduce(apply_replace, [("{NOM}", lambda x: user_data['name']),], info)
            message = "{}:{}.".format(message.split(':')[0], ', '.join(message.split(':')[1].split(', ')[5:]))
            bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            query = db[db['keyword'] == keyword]
            print(keyword)
            print(query)
            print(user_data["melanoma"])
            if not query.empty:
                info = query[user_data["melanoma"]].values[0]
                info = reduce(apply_replace, [("{NOM}", lambda x: user_data['name']),], info)
                for message in filter(lambda x: len(x.replace(" ","")) > 0 , info.split('. ')):
                    bot.send_message(chat_id=update.message.chat_id, text=message)
            else:
                bot.send_message(chat_id=update.message.chat_id, text=response.text)
        _early_response = [keyword]
    except Exception as e:
        print(e)
        traceback.print_exc()
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))
        '''
def main():
    #949321682:AAECbZCBtEFHbLDYELQ2OHuFNfpnQcmp5J8 POL
    token = "942283486:AAGVxx31KxtIzMGgZkBZBRWoC5POwcrtRUw" #open('../token.txt').read().strip()
    print("el token es" + token)
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    translatorFile = open(PATH_TO_TRANSLATION_FILE, "r").read()
    yaml = YAML()
    global translator
    translator = yaml.load(translatorFile)#load translation file

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states = {
            NAME: [MessageHandler(Filters.text, name, pass_user_data=True)],
            AGE: [MessageHandler(Filters.text, age, pass_user_data=True)],
            GENDER: [MessageHandler(Filters.text, gender, pass_user_data=True)],
            LOCATION: [MessageHandler(Filters.location | Filters.text, location, pass_user_data=True)],
            SAVE_USER: [MessageHandler(Filters.text, saveUser, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(MessageHandler(Filters.text, answers, pass_user_data=True))

    print("Bot iniciado")

    updater.start_polling()

if __name__ == '__main__':
    main()