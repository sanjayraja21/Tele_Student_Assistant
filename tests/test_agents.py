from agents.frontend_agent import (
    FrontendAgent
)


class FakeBackend:

    def process(
        self,
        message,
        user_id
    ):

        return (
            "Backend received: "
            + message
        )


class FakeSecurity:

    def validate_input(
        self,
        message,
        user_id
    ):

        return {
            "allowed": True
        }

    def validate_output(
        self,
        response
    ):

        return response


def test_frontend_agent():

    agent = FrontendAgent(
        FakeBackend(),
        FakeSecurity()
    )

    result = agent.handle(
        "Hello"
    )

    assert (
        result
        == "Backend received: Hello"
    )