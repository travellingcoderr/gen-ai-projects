class AppError(Exception):
    """Base application exception."""


class UpstreamServiceError(AppError):
    """Raised when upstream client requests fail."""
