import ptbot, os
from pytimeparse import parse
from dotenv import load_dotenv


def tmr(author_id, message, bot_instance):
    time = parse(message)
    message_id = bot_instance.send_message(author_id, 'Запуск таймера')
    if time is None:
        bot_instance.send_message(author_id, 'Ошибка!')
    else:
        bot_instance.create_countdown(time, notify, message_id=message_id, chat_id=author_id, 
                                      time=time, bot_instance=bot_instance)


def notify(secs_left, message_id, chat_id, time, bot_instance):
    if secs_left == 0:
        bot_instance.send_message(chat_id, 'Время вышло!')
    else:
        new_message= "Осталось {} секунд!".format(secs_left) + '\n' + render_progressbar(time, time-secs_left+1)
        bot_instance.update_message(chat_id, message_id, new_message)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

    
def main():
    load_dotenv()
    tg_token = os.getenv('TELEGRAM_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    bot = ptbot.Bot(tg_token)
    bot.send_message(tg_chat_id, "Бот запущен")
    bot.reply_on_message(tmr, bot_instance=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
   
    

