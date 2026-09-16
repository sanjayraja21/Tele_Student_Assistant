class DatabaseAgent:
    """
    Database Agent

    Responsible for:
    - Student memory
    - Subjects
    - Assignments
    - Exams
    - Progress information
    """

    def __init__(self, database):
        self.database = database

    # -----------------------------
    # Student
    # -----------------------------

    def register_student(
        self,
        name,
        user_id
    ):

        self.database.upsert_student(
            user_id,
            name
        )

        return (
            f"Student profile saved successfully.\n"
            f"Name: {name}"
        )

    # -----------------------------
    # Subjects
    # -----------------------------

    def add_subject(
        self,
        user_id,
        subject
    ):

        if not subject:

            return (
                "Please provide a subject name."
            )

        self.database.add_subject(
            user_id,
            subject
        )

        return (
            f"Subject '{subject}' "
            "added successfully."
        )

    def list_subjects(
        self,
        user_id
    ):

        subjects = self.database.get_subjects(
            user_id
        )

        if not subjects:

            return "No subjects found."

        result = ["📚 Your Subjects:"]

        for index, subject in enumerate(
            subjects,
            start=1
        ):

            result.append(
                f"{index}. {subject['name']}"
            )

        return "\n".join(result)

    # -----------------------------
    # Assignments
    # -----------------------------

    def add_assignment(
        self,
        user_id,
        title,
        due_date
    ):

        try:

            self.database.add_assignment(
                user_id,
                title,
                due_date
            )

        except ValueError as error:

            return str(error)

        return (
            "✅ Assignment added successfully.\n\n"
            f"📌 Title: {title}\n"
            f"📅 Deadline: {due_date}\n"
            "📊 Status: Pending"
        )

    def list_assignments(
        self,
        user_id
    ):

        assignments = self.database.get_assignments(
            user_id
        )

        if not assignments:

            return "No assignments found."

        result = ["📝 Your Assignments:"]

        for index, assignment in enumerate(
            assignments,
            start=1
        ):

            result.append(
                f"{index}. "
                f"{assignment['title']} | "
                f"Due: {assignment['due_date']} | "
                f"Status: {assignment['status']}"
            )

        return "\n".join(result)

    # -----------------------------
    # Exams
    # -----------------------------

    def add_exam(
        self,
        user_id,
        subject,
        exam_date
    ):

        try:

            self.database.add_exam(
                user_id,
                subject,
                exam_date
            )

        except ValueError as error:

            return str(error)

        return (
            "✅ Exam added successfully.\n\n"
            f"📚 Subject: {subject}\n"
            f"📅 Exam Date: {exam_date}"
        )

    def list_exams(
        self,
        user_id
    ):

        exams = self.database.get_exams(
            user_id
        )

        if not exams:

            return "No exams found."

        result = ["📅 Your Exams:"]

        for index, exam in enumerate(
            exams,
            start=1
        ):

            result.append(
                f"{index}. "
                f"{exam['subject']} | "
                f"Date: {exam['exam_date']}"
            )

        return "\n".join(result)

    # -----------------------------
    # Context
    # -----------------------------

    def student_context(
        self,
        user_id
    ):

        return {

            "student":
                self.database.get_student(
                    user_id
                ),

            "subjects":
                self.database.get_subjects(
                    user_id
                ),

            "assignments":
                self.database.get_assignments(
                    user_id
                ),

            "exams":
                self.database.get_exams(
                    user_id
                )
        }

    # -----------------------------
    # Progress
    # -----------------------------

    def progress_data(
        self,
        user_id
    ):

        return self.database.progress_data(
            user_id
        )