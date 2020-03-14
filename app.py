from bot import Bot
import config


def main():
    bot = Bot(config.BOT_TOKEN)
    bot.start()


if __name__ == '__main__':
    main()
