from main import build_application

from scheduler.scheduler import (
    StudentScheduler
)


def main():

    (
        frontend_agent,
        backend_agent,
        database
    ) = build_application()

    scheduler = StudentScheduler(
        backend_agent,
        user_id=1
    )

    scheduler.start()


if __name__ == "__main__":

    main()