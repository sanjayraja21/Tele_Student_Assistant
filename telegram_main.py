from main import build_application

from bot.telegram_bot import (
    run_telegram
)


def main():

    (
        frontend_agent,
        backend_agent,
        database
    ) = build_application()

    run_telegram(
        frontend_agent
    )


if __name__ == "__main__":

    main()