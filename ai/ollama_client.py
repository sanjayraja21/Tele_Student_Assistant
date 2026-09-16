import os

try:
    import ollama

except ImportError:

    ollama = None


class OllamaClient:
    """
    Local AI client.

    Uses Ollama running on the user's computer.
    """

    def __init__(
        self,
        model=None
    ):

        self.model = (
            model
            or os.getenv(
                "OLLAMA_MODEL",
                "llama3.2"
            )
        )

    def generate(
        self,
        prompt
    ):

        if ollama is None:

            raise RuntimeError(
                "Python package 'ollama' is not installed."
            )

        result = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return result[
            "message"
        ][
            "content"
        ]