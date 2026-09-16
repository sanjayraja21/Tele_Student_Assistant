class ResponseAgent:
    """
    Response Agent

    Uses Ollama/local LLM to generate
    personalized student responses.
    """

    def __init__(self, ai_client):
        self.ai_client = ai_client

    def _ask(
        self,
        prompt,
        fallback
    ):

        try:

            response = self.ai_client.generate(
                prompt
            )

            if response:

                return response.strip()

            return fallback

        except Exception as error:

            return (
                f"{fallback}\n\n"
                f"Local AI status: {error}"
            )

    # -----------------------------
    # Explanation
    # -----------------------------

    def explain(
        self,
        topic
    ):

        prompt = f"""
You are a friendly AI tutor.

Explain the following topic to a beginner student:

Topic:
{topic}

Requirements:
1. Use simple English.
2. Give a clear definition.
3. Give a small real-world example.
4. Explain the important points.
5. End with 3 quick revision points.
"""

        return self._ask(
            prompt,
            "Ollama is not available. Please start Ollama and try again."
        )

    # -----------------------------
    # General Question
    # -----------------------------

    def general(
        self,
        question
    ):

        prompt = f"""
You are TeleStudentAssistant,
a helpful AI academic assistant.

Answer the student's question:

{question}

Rules:
- Use simple English.
- Be accurate.
- Be concise.
- Use examples when useful.
"""

        return self._ask(
            prompt,
            "I could not generate the AI response."
        )

    # -----------------------------
    # Study Plan
    # -----------------------------

    def study_plan(
        self,
        context
    ):

        prompt = f"""
You are an AI academic planner.

Create a realistic study plan for this student.

Student information:
{context}

Requirements:
- Prioritize upcoming exams.
- Consider pending assignments.
- Include subjects.
- Use realistic study durations.
- Give a simple daily plan.
- Avoid overloading the student.
"""

        return self._ask(
            prompt,
            "Please add your subjects and exams first."
        )

    # -----------------------------
    # Quiz
    # -----------------------------

    def quiz(
        self,
        topic
    ):

        prompt = f"""
Create a beginner-friendly quiz about:

{topic}

Create exactly 5 multiple-choice questions.

Format:

Q1. Question
A. Option
B. Option
C. Option
D. Option

At the end provide:

Answer Key:
1. A
2. B
3. C
4. D
5. A

Do not make the questions unnecessarily difficult.
"""

        return self._ask(
            prompt,
            "Quiz generation requires Ollama."
        )

    # -----------------------------
    # Progress
    # -----------------------------

    def progress(
        self,
        data
    ):

        prompt = f"""
You are an AI student progress coach.

Analyze this student data:

{data}

Create a short progress report containing:

1. Current status
2. Pending work
3. Positive progress
4. Recommended next steps

Use encouraging and simple English.
"""

        return self._ask(
            prompt,
            "Progress data is available, but Ollama is not running."
        )

    # -----------------------------
    # PDF Summary
    # -----------------------------

    def summarize(
        self,
        text
    ):

        prompt = f"""
You are an AI study assistant.

Analyze these study notes:

{text}

Provide:

1. Short summary
2. Important concepts
3. Key terms
4. Important points
5. 5 revision questions

Use simple English.
"""

        return self._ask(
            prompt,
            "The PDF was processed, but Ollama is unavailable."
        )