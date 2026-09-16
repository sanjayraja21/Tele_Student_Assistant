class FrontendAgent:
    """
    Frontend Agent

    Responsibilities:
    - Receive student input
    - Perform initial security validation
    - Send request to Backend Agent
    - Return final response
    """

    def __init__(self, backend_agent, security_agent):
        self.backend_agent = backend_agent
        self.security_agent = security_agent

    def handle(self, message, user_id=1):
        security_result = self.security_agent.validate_input(
            message,
            user_id
        )

        if not security_result["allowed"]:
            return security_result["reason"]

        response = self.backend_agent.process(
            message,
            user_id
        )

        return self.security_agent.validate_output(response)