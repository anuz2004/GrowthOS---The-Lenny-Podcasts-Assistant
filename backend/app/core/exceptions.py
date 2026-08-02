from typing import Any


class GrowthOSError(Exception):
    """
    Base exception for all user-facing GrowthOS errors.
    """

    def __init__(
        self,
        title: str,
        message: str,
        suggestions: list[str] | None = None,
        technical: str | None = None,
        status_code: int = 500,
    ):
        self.title = title
        self.message = message
        self.suggestions = suggestions or []
        self.technical = technical
        self.status_code = status_code

        super().__init__(message)


class OllamaConnectionError(GrowthOSError):

    def __init__(
        self,
        technical: str = "",
    ):
        super().__init__(
            title="Unable to Connect to Ollama",
            message="GrowthOS could not communicate with your local Ollama server.",
            suggestions=[
                "Make sure Ollama is running.",
                "Run 'ollama serve' in a terminal.",
                "Verify the selected model is installed.",
            ],
            technical=technical,
            status_code=503,
        )


class ModelNotInstalledError(GrowthOSError):

    def __init__(
        self,
        model: str,
    ):
        super().__init__(
            title="Model Not Installed",
            message=f"The model '{model}' is not installed.",
            suggestions=[
                f"Run: ollama pull {model}",
                "Restart Ollama after installation.",
            ],
            status_code=400,
        )


class DatabaseConnectionError(GrowthOSError):

    def __init__(
        self,
        technical: str = "",
    ):
        super().__init__(
            title="Database Connection Failed",
            message="GrowthOS could not connect to PostgreSQL.",
            suggestions=[
                "Verify PostgreSQL is running.",
                "Check your database configuration.",
                "Restart the backend.",
            ],
            technical=technical,
            status_code=500,
        )


class ProviderAPIError(GrowthOSError):

    def __init__(
        self,
        provider: str,
        technical: str = "",
    ):
        super().__init__(
            title=f"{provider} Error",
            message=f"The {provider} API request failed.",
            suggestions=[
                "Verify your API key.",
                "Check your internet connection.",
                "Try again later.",
            ],
            technical=technical,
            status_code=502,
        )


class ChatNotFoundError(GrowthOSError):

    def __init__(self):

        super().__init__(
            title="Chat Not Found",
            message="The selected chat session no longer exists.",
            suggestions=[
                "Refresh the page.",
                "Create a new chat.",
            ],
            status_code=404,
        )


class WorkspaceNotFoundError(GrowthOSError):

    def __init__(self):

        super().__init__(
            title="Workspace Not Found",
            message="The selected workspace no longer exists.",
            suggestions=[
                "Refresh the page.",
                "Create a new workspace.",
            ],
            status_code=404,
        )