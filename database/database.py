import sqlite3

from pathlib import Path

from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = (
    BASE_DIR
    / "data"
    / "student.db"
)


class Database:

    def __init__(
        self,
        path=DB_PATH
    ):

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    # -----------------------------
    # Connection
    # -----------------------------

    def connect(self):

        connection = sqlite3.connect(
            self.path
        )

        connection.row_factory = (
            sqlite3.Row
        )

        return connection

    # -----------------------------
    # Initialize Database
    # -----------------------------

    def initialize(self):

        with self.connect() as connection:

            connection.executescript("""

            CREATE TABLE IF NOT EXISTS students (

                user_id INTEGER PRIMARY KEY,

                name TEXT NOT NULL,

                created_at TEXT NOT NULL

            );


            CREATE TABLE IF NOT EXISTS subjects (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                UNIQUE(user_id, name)

            );


            CREATE TABLE IF NOT EXISTS assignments (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                title TEXT NOT NULL,

                due_date TEXT NOT NULL,

                status TEXT NOT NULL
                    DEFAULT 'Pending'

            );


            CREATE TABLE IF NOT EXISTS exams (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                subject TEXT NOT NULL,

                exam_date TEXT NOT NULL

            );


            CREATE TABLE IF NOT EXISTS study_history (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                subject TEXT,

                topic TEXT,

                minutes INTEGER DEFAULT 0,

                studied_at TEXT NOT NULL

            );


            CREATE TABLE IF NOT EXISTS quiz_results (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                topic TEXT,

                score INTEGER,

                total INTEGER,

                created_at TEXT NOT NULL

            );

            """)

    # -----------------------------
    # Student
    # -----------------------------

    def upsert_student(
        self,
        user_id,
        name
    ):

        with self.connect() as connection:

            connection.execute(
                """
                INSERT INTO students
                (user_id, name, created_at)

                VALUES (?, ?, ?)

                ON CONFLICT(user_id)

                DO UPDATE SET
                name = excluded.name
                """,

                (
                    user_id,
                    name,
                    datetime.now().isoformat()
                )
            )

    def get_student(
        self,
        user_id
    ):

        with self.connect() as connection:

            row = connection.execute(
                """
                SELECT *
                FROM students
                WHERE user_id = ?
                """,

                (user_id,)
            ).fetchone()

            if row:

                return dict(row)

            return None

    # -----------------------------
    # Subjects
    # -----------------------------

    def add_subject(
        self,
        user_id,
        name
    ):

        with self.connect() as connection:

            connection.execute(
                """
                INSERT OR IGNORE INTO subjects
                (user_id, name)

                VALUES (?, ?)
                """,

                (
                    user_id,
                    name
                )
            )

    def get_subjects(
        self,
        user_id
    ):

        with self.connect() as connection:

            rows = connection.execute(
                """
                SELECT *
                FROM subjects

                WHERE user_id = ?

                ORDER BY name
                """,

                (user_id,)
            ).fetchall()

            return [
                dict(row)
                for row in rows
            ]

    # -----------------------------
    # Date Validation
    # -----------------------------

    @staticmethod
    def valid_date(
        value
    ):

        try:

            datetime.strptime(
                value,
                "%Y-%m-%d"
            )

            return True

        except ValueError:

            return False

    # -----------------------------
    # Assignments
    # -----------------------------

    def add_assignment(
        self,
        user_id,
        title,
        due_date
    ):

        if not self.valid_date(
            due_date
        ):

            raise ValueError(
                "Use deadline format YYYY-MM-DD."
            )

        with self.connect() as connection:

            connection.execute(
                """
                INSERT INTO assignments
                (user_id, title, due_date)

                VALUES (?, ?, ?)
                """,

                (
                    user_id,
                    title,
                    due_date
                )
            )

    def get_assignments(
        self,
        user_id
    ):

        with self.connect() as connection:

            rows = connection.execute(
                """
                SELECT *
                FROM assignments

                WHERE user_id = ?

                ORDER BY due_date
                """,

                (user_id,)
            ).fetchall()

            return [
                dict(row)
                for row in rows
            ]

    # -----------------------------
    # Exams
    # -----------------------------

    def add_exam(
        self,
        user_id,
        subject,
        exam_date
    ):

        if not self.valid_date(
            exam_date
        ):

            raise ValueError(
                "Use exam date format YYYY-MM-DD."
            )

        with self.connect() as connection:

            connection.execute(
                """
                INSERT INTO exams
                (user_id, subject, exam_date)

                VALUES (?, ?, ?)
                """,

                (
                    user_id,
                    subject,
                    exam_date
                )
            )

    def get_exams(
        self,
        user_id
    ):

        with self.connect() as connection:

            rows = connection.execute(
                """
                SELECT *
                FROM exams

                WHERE user_id = ?

                ORDER BY exam_date
                """,

                (user_id,)
            ).fetchall()

            return [
                dict(row)
                for row in rows
            ]

    # -----------------------------
    # Progress
    # -----------------------------

    def progress_data(
        self,
        user_id
    ):

        with self.connect() as connection:

            assignments = connection.execute(
                """
                SELECT COUNT(*) AS total

                FROM assignments

                WHERE user_id = ?
                """,

                (user_id,)
            ).fetchone()["total"]

            pending = connection.execute(
                """
                SELECT COUNT(*) AS total

                FROM assignments

                WHERE user_id = ?

                AND status = 'Pending'
                """,

                (user_id,)
            ).fetchone()["total"]

            quizzes = connection.execute(
                """
                SELECT

                COUNT(*) AS quiz_count,

                COALESCE(
                    SUM(score),
                    0
                ) AS score,

                COALESCE(
                    SUM(total),
                    0
                ) AS total

                FROM quiz_results

                WHERE user_id = ?
                """,

                (user_id,)
            ).fetchone()

            return {

                "assignments_total":
                    assignments,

                "assignments_pending":
                    pending,

                "quiz_count":
                    quizzes["quiz_count"],

                "quiz_score":
                    quizzes["score"],

                "quiz_total":
                    quizzes["total"]

            }