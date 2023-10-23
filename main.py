import telebot

bot = telebot.TeleBot('6573749748:AAHkgu9YEZrSoO4azALlhsJBOTpuQaciMwA')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     '<b>Добро пожаловать в horoscope Bot 007! Здесь вы найдете всю необходимую информацию о своем знаке зодиака, предсказания на день, неделю, месяц и год, а также сможете узнать свою совместимость с другими ЗЗ и натальную карту. Узнайте, что ждет вас в ближайшем будущем и какие события повлияют на вашу жизнь. Верим, что наш бот поможет сделать вашу жизнь ярче и интереснее. Приятного чтения и удачи во всех начинаниях!</b>',
                     parse_mode='html')


bot.polling(none_stop=True)
