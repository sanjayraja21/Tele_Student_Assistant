import re


class SecurityAgent:
    """
    Application-level security and validation agent.

    This is a project-level security layer,
    not enterprise cybersecurity.
    """

    BLOCKED_PATTERNS = [

        r"ignore\s+(all\s+)?previous\s+instructions",

        r"ignore\s+your\s+instructions",

        r"reveal\s+(the\s+)?system\s+prompt",

        r"show\s+(me\s+)?(the\s+)?api\s+key",

        r"give\s+me\s+(the\s+)?password",

        r"delete\s+all\s+database",

    ]

    MAX_INPUT_LENGTH = 30000

    MAX_OUTPUT_LENGTH = 10000

    # -----------------------------
    # Input Validation
    # -----------------------------

    def validate_input(
        self,
        message,
        user_id=1
    ):

        if not isinstance(
            message,
            str
        ):

            return {
                "allowed": False,
                "reason": "Invalid input."
            }

        message = message.strip()

        if not message:

            return {
                "allowed": False,
                "reason": "Empty input is not allowed."
            }

        if len(message) > self.MAX_INPUT_LENGTH:

            return {
                "allowed": False,
                "reason":
                    "Input is too large."
            }

        for pattern in self.BLOCKED_PATTERNS:

            if re.search(
                pattern,
                message,
                re.IGNORECASE
            ):

                return {
                    "allowed": False,
                    "reason":
                        "⚠️ Request blocked by the Security Agent."
                }

        return {
            "allowed": True
        }

    # -----------------------------
    # Output Validation
    # -----------------------------

    def validate_output(
        self,
        response
    ):

        if response is None:

            return (
                "No response was generated."
            )

        response = str(response)

        if len(response) > self.MAX_OUTPUT_LENGTH:

            response = response[
                :self.MAX_OUTPUT_LENGTH
            ]

        return response