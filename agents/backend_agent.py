import re


class BackendAgent:
    """
    Backend Agent

    Acts as the central coordinator.
    Decides which capability is required.
    """

    def __init__(
        self,
        database_agent,
        response_agent,
        security_agent
    ):
        self.database_agent = database_agent
        self.response_agent = response_agent
        self.security_agent = security_agent

    def process(self, message, user_id=1):

        text = message.strip()
        lower_text = text.lower()

        # -----------------------------
        # Student Registration
        # -----------------------------
        if lower_text.startswith("register "):

            name = text[9:].strip()

            if not name:
                return "Please provide your name."

            return self.database_agent.register_student(
                name,
                user_id
            )

        # -----------------------------
        # Add Subject
        # -----------------------------
        if lower_text.startswith("add subject "):

            subject = text[12:].strip()

            return self.database_agent.add_subject(
                user_id,
                subject
            )

        # -----------------------------
        # Add Assignment
        # -----------------------------
        if lower_text.startswith("add assignment "):

            data = self._extract_quoted_values(
                text[15:]
            )

            if len(data) < 2:

                return (
                    'Correct format:\n'
                    'add assignment '
                    '"Assignment Name" '
                    '"YYYY-MM-DD"'
                )

            title = data[0]
            due_date = data[1]

            return self.database_agent.add_assignment(
                user_id,
                title,
                due_date
            )

        # -----------------------------
        # Add Exam
        # -----------------------------
        if lower_text.startswith("add exam "):

            data = self._extract_quoted_values(
                text[9:]
            )

            if len(data) < 2:

                return (
                    'Correct format:\n'
                    'add exam '
                    '"Subject" '
                    '"YYYY-MM-DD"'
                )

            subject = data[0]
            exam_date = data[1]

            return self.database_agent.add_exam(
                user_id,
                subject,
                exam_date
            )

        # -----------------------------
        # Show Subjects
        # -----------------------------
        if lower_text == "subjects":

            return self.database_agent.list_subjects(
                user_id
            )

        # -----------------------------
        # Show Assignments
        # -----------------------------
        if lower_text == "assignments":

            return self.database_agent.list_assignments(
                user_id
            )

        # -----------------------------
        # Show Exams
        # -----------------------------
        if lower_text == "exams":

            return self.database_agent.list_exams(
                user_id
            )

        # -----------------------------
        # Study Plan
        # -----------------------------
        if (
            "study plan" in lower_text
            or
            "what should i study" in lower_text
        ):

            context = self.database_agent.student_context(
                user_id
            )

            return self.response_agent.study_plan(
                context
            )

        # -----------------------------
        # Quiz
        # -----------------------------
        if lower_text.startswith("quiz"):

            topic = text[4:].strip()

            if not topic:
                topic = "general computer science"

            return self.response_agent.quiz(
                topic
            )

        # -----------------------------
        # Explanation
        # -----------------------------
        if lower_text.startswith("explain "):

            topic = text[8:].strip()

            return self.response_agent.explain(
                topic
            )

        # -----------------------------
        # Progress
        # -----------------------------
        if (
            lower_text == "progress"
            or
            lower_text == "my progress"
        ):

            data = self.database_agent.progress_data(
                user_id
            )

            return self.response_agent.progress(
                data
            )

        # -----------------------------
        # PDF Summary
        # -----------------------------
        if "summarize this pdf" in lower_text:

            if ":" in text:

                pdf_text = text.split(
                    ":",
                    1
                )[1]

            else:

                pdf_text = text

            return self.response_agent.summarize(
                pdf_text
            )

        # -----------------------------
        # General AI Question
        # -----------------------------
        return self.response_agent.general(
            text
        )

    @staticmethod
    def _extract_quoted_values(text):

        return re.findall(
            r'"([^"]+)"',
            text
        )