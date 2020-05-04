# -*- coding: utf-8 -*-

import telebot
import config
import dbworker

bot = telebot.TeleBot('Token')


# algus
@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_NAME.value:
        bot.send_message(message.chat.id, "Keegi lubas kirjutada mulle oma nime. :( Ootan...")
    elif state == config.States.S_ENTER_AGE.value:
        bot.send_message(message.chat.id, "Keegi lubas mulle saata oma vanust :( Ootan...")
    elif state == config.States.S_SEND_PIC.value:
        bot.send_message(message.chat.id, "Keegi lubas mulle saata pildi :( Ootan...")
    else:  
        bot.send_message(message.chat.id, "Tere, kuidas mina sinu poole pöördun?")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)


# Reset käsuga toimub reset
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Ok, alustame uuesti siis?")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_name(message):
    # Nimega ei toimu kontrollimist
    bot.send_message(message.chat.id, "Super! Jätan meelde, nüüd ütle mulle palun oma vanus?.")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_AGE.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_AGE.value)
def user_entering_age(message):
    # Vanuse kontroll
    if not message.text.isdigit():
        # Olekut ei muuda, ainult edastae, et vanusega on midagi valesti
        bot.send_message(message.chat.id, "Midagi on valesti vanusega, siseta uuesti!")
        return
    # Saame aru, et tegemist on siiski arvuga
    if int(message.text) < 5 or int(message.text) > 100:
        bot.send_message(message.chat.id, "Imelik vanus sul. Ei usu. Kirjuta palun aus vanus.")
        return
    else:
        # Vanus mis jääb vahemikku
        bot.send_message(message.chat.id, "Kunagi olin ka mina sama vana. Tore liigume edasi siis. "
                                          "Saada mulle palun suvaline pilt.")
        dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)


@bot.message_handler(content_types=["photo"],
                     func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SEND_PIC.value)
def user_sending_photo(message):
    # Kui saame aru, et tegemist on fotoga.
    bot.send_message(message.chat.id, "Tore, rohkem mina sinu käest midagi ei küsi, kui soovid alustada otsastpeale - "
                     "saada käsk /start.")
    dbworker.set_state(message.chat.id, config.States.S_START.value)


if __name__ == "__main__":
    bot.infinity_polling()