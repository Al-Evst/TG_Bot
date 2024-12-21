import ptbot, os
from pytimeparse import parse
from dotenv import load_dotenv


load_dotenv()
TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELG_CHAT_ID = os.getenv('TG_CHAT_ID')
bot = ptbot.Bot(TG_TOKEN)
bot.send_message(TELG_CHAT_ID, "Бот запущен")


def tmr(author_id, message):
    time = parse(message)
    message_id = bot.send_message(author_id, 'Запуск таймера')
    if time is None:
        bot.send_message(author_id, 'Ошибка!')
    else:
        bot.create_countdown(time, notify, message_id=message_id, chat_id=author_id, time=time)


def notify(secs_left, message_id, chat_id, time):
    if secs_left == 0:
        bot.send_message(chat_id, 'Время вышло!')
    else:
        new_message= "Осталось {} секунд!".format(secs_left) + '\n' + render_progressbar(time, time-secs_left+1)
        bot.update_message(chat_id, message_id, new_message)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


if __name__ == '__main__':
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(tmr)
    bot.run_bot()
