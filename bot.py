import telebot # библиотека telebot
from config import token # импорт токена
import random
bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")
@bot.message_handler(func=lambda message: True)
def check_link_and_ban_user(message):
    if "https://" in message.text or "http://" in message.text:
        try:
            user_id = message.from_user.id
            bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
            bot.send_message(chat_id=message.chat.id,text=f"Пользователь {message.from_user.first_name} ({user_id}) забанен за публикацию ссылки.")
        except Exception as e:
            print(f"Ошибка при попытке забанить пользователя:  {e}")
@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_member(message):
    for member in message.new_chat_members:
        bot.send_message(message.chat.id, f'Приветствуем нового участника: {member.first_name}')
        bot.approve_chat_join_request(message.chat.id, member.id)

@bot.message_handler(commands=['quote'])
def quote_handler(message):
    quotes = random.choice(['«Обстоятельства часто можно изменить, изменив своё отношение к ним» — Элеонора Рузвельт. ',

    '«Мы не можем решить проблемы тем же мышлением, которое использовали, когда их создавали» — Альберт Эйнштейн.',
    '«Учись так, будто будешь жить вечно, живи так, будто умрёшь завтра» — Махатма Ганди. ',
    '«Когда ты даришь радость другим людям, ты получаешь больше радости взамен. Ты должен хорошо подумать о счастье, которое можешь дарить» — Элеонора Рузвельт.', 
    '«Когда меняешь свои мысли, не забудь также изменить свой мир» — Норман Винсент Пил. '
    '«Более полная жизнь не у того, кто прожил дольше, а у того, кто больше узнал» — Жан-Жак Руссо',
    '«Счастье не в том, чтобы делать всегда, что хочешь, а в том, чтобы всегда хотеть того, что делаешь» — Лев Толстой. ',
    '«Выживает не самый сильный из видов и не самый умный, а тот, кто лучше других реагирует на изменения» — Леон Меггинсон. '])
    bot.reply_to(message, quotes)


@bot.message_handler(commands=['coin'])
def coin_handler(message):
    coin = random.choice(["ОРЕЛ", "РЕШКА"])
    bot.reply_to(message, coin)

# Handle '/start' and '/help'
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message,'Здравтвуте это телеграм бот сделанный на курсе Kodland PythonLVL3')

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.infinity_polling(none_stop=True)
