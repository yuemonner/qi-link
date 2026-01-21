"""
Custom Exceptions
=================

Hierarchical exception classes for clean error handling throughout
the Qi-Link application.
"""

from typing import Optional


class QiLinkError(Exception):
    """Base exception for all Qi-Link errors."""

    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class SensorError(QiLinkError):
    """Errors related to hardware sensor readings."""

    pass


class TemperatureReadError(SensorError):
    """Failed to read CPU temperature."""

    pass


class NetworkProbeError(SensorError):
    """Failed to measure network latency."""

    pass


class AstrologyError(QiLinkError):
    """Errors in astrological calculations."""

    pass


class InvalidBirthDataError(AstrologyError):
    """Birth data is invalid or cannot be processed."""

    pass


class CalendarConversionError(AstrologyError):
    """Failed to convert between calendars."""

    pass


class AlchemyError(QiLinkError):
    """Errors in the metaphysical calculation engine."""

    pass


class ElementImbalanceError(AlchemyError):
    """Unable to determine elemental balance."""

    pass


class ImageGenerationError(QiLinkError):
    """Errors in talisman image generation."""

    pass


class OpenAIError(ImageGenerationError):
    """OpenAI API-specific errors."""

    pass


class APIKeyMissingError(OpenAIError):
    """OpenAI API key not configured."""

    def __init__(self):
        super().__init__(
            message="OpenAI API key not configured",
            details={"env_var": "QILINK_OPENAI_API_KEY"},
        )


class BlockchainError(QiLinkError):
    """Errors in blockchain operations."""

    pass


class HashingError(BlockchainError):
    """Failed to hash metadata."""

    pass

