from Saiga_7b_model import quest_answer
import telebot
BOT_CODE=''
bot = telebot.TeleBot(BOT_CODE)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Hello!')

@bot.message_handler(content_types=['text'])  #реагирует на любые сообщения
def aswering(message):
      bot.send_message(message.chat.id, ans)
      print(message.from_user.username,':',message.text)
      print('===========================')
      ans=quest_answer(message.text)
      print(ans)
      print()
      print()
@bot.message_handler(content_types=['photo'])
def photo_id(message):
    photo = max(message.photo, key=lambda x: x.height)
    print(photo.file_id)
    bot.send_message(message.chat.id, "Вы отправили картинку")


bot.polling(none_stop=True)
