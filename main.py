from agents.frontend_agent import (
    FrontendAgent
)

from agents.backend_agent import (
    BackendAgent
)

from agents.database_agent import (
    DatabaseAgent
)

from agents.response_agent import (
    ResponseAgent
)

from agents.security_agent import (
    SecurityAgent
)

from ai.ollama_client import (
    OllamaClient
)

from database.database import (
    Database
)

from utils.pdf_processor import (
    extract_text_from_pdf
)


def build_application():

    # Database

    database = Database()

    database.initialize()

    # Local AI

    ai_client = OllamaClient()

    # Agents

    database_agent = (
        DatabaseAgent(
            database
        )
    )

    response_agent = (
        ResponseAgent(
            ai_client
        )
    )

    security_agent = (
        SecurityAgent()
    )

    backend_agent = (
        BackendAgent(
            database_agent,
            response_agent,
            security_agent
        )
    )

    frontend_agent = (
        FrontendAgent(
            backend_agent,
            security_agent
        )
    )

    return (
        frontend_agent,
        backend_agent,
        database
    )


def print_help():

    print(
        """
================================================
          TeleStudentAssistant v1.0
================================================

LOCAL MODE

Commands:

register Sanjay

add subject Python

add subject DBMS

add assignment "Python Project" "2026-09-20"

add exam "DBMS" "2026-09-25"

subjects

assignments

exams

study plan

explain normalization

quiz Python

progress

summarize_pdf "C:\\path\\notes.pdf"

help

exit

================================================
"""
    )


def main():

    (
        frontend_agent,
        backend_agent,
        database
    ) = build_application()

    print(
        "\nTeleStudentAssistant started."
    )

    print(
        "Local testing mode is active."
    )

    print_help()

    while True:

        try:

            command = input(
                "\nYou: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError
        ):

            print(
                "\nApplication stopped."
            )

            break

        if not command:

            continue

        if command.lower() in {
            "exit",
            "quit"
        }:

            print(
                "Goodbye!"
            )

            break

        if command.lower() == "help":

            print_help()

            continue

        # PDF command

        if command.lower().startswith(
            "summarize_pdf "
        ):

            path = (
                command[
                    len("summarize_pdf "):
                ]
                .strip()
                .strip('"')
            )

            try:

                pdf_text = (
                    extract_text_from_pdf(
                        path
                    )
                )

                result = (
                    backend_agent.process(
                        "Summarize this PDF:\n"
                        + pdf_text[:30000]
                    )
                )

            except Exception as error:

                result = (
                    f"PDF error: {error}"
                )

        else:

            result = (
                frontend_agent.handle(
                    command,
                    user_id=1
                )
            )

        print(
            f"\nAssistant:\n{result}"
        )


if __name__ == "__main__":

    main()