from apscheduler.schedulers.blocking import (
    BlockingScheduler
)


class StudentScheduler:
    """
    Proactive automation infrastructure.

    This is NOT an additional AI agent.
    """

    def __init__(
        self,
        backend_agent,
        user_id=1
    ):

        self.backend_agent = (
            backend_agent
        )

        self.user_id = user_id

        self.scheduler = (
            BlockingScheduler()
        )

    # -----------------------------
    # Start Scheduler
    # -----------------------------

    def start(self):

        self.scheduler.add_job(
            self.daily_study_content,
            "cron",
            hour=8,
            minute=0
        )

        self.scheduler.add_job(
            self.assignment_reminder,
            "cron",
            hour=13,
            minute=0
        )

        self.scheduler.add_job(
            self.daily_quiz,
            "cron",
            hour=19,
            minute=0
        )

        self.scheduler.add_job(
            self.daily_progress,
            "cron",
            hour=21,
            minute=0
        )

        print(
            "Scheduler started."
        )

        print(
            "08:00 - Study content"
        )

        print(
            "13:00 - Assignment reminder"
        )

        print(
            "19:00 - Daily quiz"
        )

        print(
            "21:00 - Progress report"
        )

        self.scheduler.start()

    # -----------------------------
    # Study Content
    # -----------------------------

    def daily_study_content(
        self
    ):

        result = self.backend_agent.process(
            "study plan",
            self.user_id
        )

        print(
            "\n[DAILY STUDY CONTENT]"
        )

        print(result)

    # -----------------------------
    # Assignment Reminder
    # -----------------------------

    def assignment_reminder(
        self
    ):

        result = self.backend_agent.process(
            "assignments",
            self.user_id
        )

        print(
            "\n[ASSIGNMENT REMINDER]"
        )

        print(result)

    # -----------------------------
    # Quiz
    # -----------------------------

    def daily_quiz(
        self
    ):

        result = self.backend_agent.process(
            "quiz general computer science",
            self.user_id
        )

        print(
            "\n[DAILY QUIZ]"
        )

        print(result)

    # -----------------------------
    # Progress
    # -----------------------------

    def daily_progress(
        self
    ):

        result = self.backend_agent.process(
            "progress",
            self.user_id
        )

        print(
            "\n[DAILY PROGRESS]"
        )

        print(result)